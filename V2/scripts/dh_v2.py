#!/usr/bin/env python3
"""Command-line entry point for the DH VR/V2 project.

This dependency-light CLI is the project's stable maintenance interface. It is
not a replacement for humanistic interpretation. Its purpose is to keep raw-text
registration, metadata, segments, lexicons, evidence tables, case files, and
release manifests reproducible.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent

DEFAULT_DOCUMENTS = "data/metadata/documents_seed.csv"
DEFAULT_RAW_MANIFEST = "data/raw/RAW_SOURCE_MANIFEST.csv"
DEFAULT_SAMPLE_SEGMENTS = "data/processed/sample_segments.jsonl"
DEFAULT_FULL_SEGMENTS = "data/processed/full_segments.jsonl"
DEFAULT_LEXICON = "config/domain_lexicon_seed.csv"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def resolve_repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    project_candidate = PROJECT_ROOT / path
    if project_candidate.exists():
        return project_candidate
    return REPO_ROOT / path


def safe_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc
            if not isinstance(item, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")
            rows.append(item)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False))
            f.write("\n")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_documents(args: argparse.Namespace) -> None:
    metadata_path = resolve_project_path(args.metadata)
    rows = read_csv(metadata_path)
    required = [
        "document_id",
        "title_original",
        "title_normalized",
        "year_standard",
        "source_status",
        "ocr_status",
        "rights_status",
    ]
    allowed_status = {
        "source_status": {"verified", "candidate", "missing", "unclear"},
        "ocr_status": {"not_started", "raw_ocr", "sample_checked", "collated", "unclear"},
        "rights_status": {"open", "restricted", "unknown", "do_not_publish_raw"},
    }
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    if not rows:
        errors.append("metadata file has no rows")

    for i, row in enumerate(rows, start=2):
        for field in required:
            if not row.get(field, "").strip():
                errors.append(f"line {i}: missing required field {field}")
        doc_id = row.get("document_id", "").strip()
        if doc_id in seen:
            errors.append(f"line {i}: duplicate document_id {doc_id}")
        seen.add(doc_id)
        for field, allowed in allowed_status.items():
            value = row.get(field, "").strip()
            if value and value not in allowed:
                errors.append(f"line {i}: invalid {field}={value!r}")
        if row.get("source_status") != "verified":
            warnings.append(f"line {i}: source not yet verified for {doc_id}")
        if row.get("rights_status") == "unknown":
            warnings.append(f"line {i}: rights status unknown for {doc_id}")

    report = {
        "check": "validate-documents",
        "metadata": safe_relative(metadata_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "generated_at": now_iso(),
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, report)

    if errors:
        print(f"Validation failed: {len(errors)} error(s). See {output_path}")
        raise SystemExit(1)
    print(f"Validation passed: {len(rows)} document record(s). Report: {output_path}")


def validate_raw_sources(args: argparse.Namespace) -> None:
    manifest_path = resolve_project_path(args.manifest)
    rows = read_csv(manifest_path)
    required = ["document_id", "raw_source_path", "source_role", "source_status"]
    errors: list[str] = []
    checked: list[dict[str, object]] = []

    for i, row in enumerate(rows, start=2):
        for field in required:
            if not row.get(field, "").strip():
                errors.append(f"line {i}: missing required field {field}")
        raw_path = resolve_repo_path(row.get("raw_source_path", ""))
        exists = raw_path.exists()
        if not exists:
            errors.append(f"line {i}: raw source does not exist: {raw_path}")
        checked.append({
            "document_id": row.get("document_id", ""),
            "raw_source_path": safe_relative(raw_path),
            "exists": exists,
            "size_bytes": raw_path.stat().st_size if exists else 0,
            "sha256": sha256_file(raw_path) if exists else "",
        })

    report = {
        "check": "validate-raw-sources",
        "manifest": safe_relative(manifest_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "errors": errors,
        "checked": checked,
        "generated_at": now_iso(),
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, report)
    if errors:
        print(f"Raw source validation failed: {len(errors)} error(s). See {output_path}")
        raise SystemExit(1)
    print(f"Raw source validation passed: {len(rows)} source(s). Report: {output_path}")


def validate_segments(args: argparse.Namespace) -> None:
    segments_path = resolve_project_path(args.segments)
    metadata_path = resolve_project_path(args.metadata)
    metadata_rows = read_csv(metadata_path)
    allowed_doc_ids = {row.get("document_id", "") for row in metadata_rows}
    rows = read_jsonl(segments_path)
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()

    for i, row in enumerate(rows, start=1):
        segment_id = str(row.get("segment_id", "")).strip()
        document_id = str(row.get("document_id", "")).strip()
        text = str(row.get("text", ""))
        if not segment_id:
            errors.append(f"line {i}: missing segment_id")
        elif segment_id in seen:
            errors.append(f"line {i}: duplicate segment_id {segment_id}")
        seen.add(segment_id)
        if document_id not in allowed_doc_ids:
            errors.append(f"line {i}: unknown document_id {document_id}")
        if not text.strip():
            errors.append(f"line {i}: empty text")
        if "placeholder" in str(row.get("notes", "")).lower() or "样本" in text:
            warnings.append(f"line {i}: possible sample or placeholder segment {segment_id}")

    report = {
        "check": "validate-segments",
        "segments": safe_relative(segments_path),
        "metadata": safe_relative(metadata_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "generated_at": now_iso(),
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, report)
    if errors:
        print(f"Segment validation failed: {len(errors)} error(s). See {output_path}")
        raise SystemExit(1)
    print(f"Segment validation passed: {len(rows)} segment(s). Report: {output_path}")


def normalize_ws_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = re.sub(r"\s+", "", text)
    return text.strip()


def chunk_text(text: str, max_chars: int, min_chars: int) -> list[tuple[int, int, str]]:
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    chunks: list[tuple[int, int, str]] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append((start, end, text[start:end]))
        start = end
    if len(chunks) > 1 and len(chunks[-1][2]) < min_chars:
        prev_start, _, prev_text = chunks[-2]
        _, last_end, last_text = chunks[-1]
        chunks[-2] = (prev_start, last_end, prev_text + last_text)
        chunks.pop()
    return chunks


def build_segments_from_raw(args: argparse.Namespace) -> None:
    manifest_path = resolve_project_path(args.manifest)
    manifest_rows = read_csv(manifest_path)
    output_rows: list[dict[str, object]] = []
    report_rows: list[dict[str, object]] = []
    max_chars = max(args.max_chars, 1)
    min_chars = max(args.min_chars, 0)

    for row in manifest_rows:
        document_id = row.get("document_id", "").strip()
        raw_source_path = row.get("raw_source_path", "").strip()
        if not document_id or not raw_source_path:
            raise ValueError("RAW_SOURCE_MANIFEST.csv requires document_id and raw_source_path")
        raw_path = resolve_repo_path(raw_source_path)
        raw_text = read_text(raw_path)
        normalized = normalize_ws_text(raw_text)
        chunks = chunk_text(normalized, max_chars=max_chars, min_chars=min_chars)
        for index, (char_start, char_end, chunk) in enumerate(chunks, start=1):
            output_rows.append({
                "segment_id": f"{document_id}_full_{index:04d}",
                "document_id": document_id,
                "segment_index": index,
                "text": chunk,
                "text_type": "full_text_segment_from_repository_raw_text",
                "chapter_title": "unknown",
                "page_ref": f"root:{raw_source_path}",
                "source_file": raw_source_path,
                "char_start": char_start,
                "char_end": char_end,
                "confidence_level": "raw_ws_normalized",
                "notes": "Generated from registered WS raw text. Verify against raw source before final scholarly citation.",
            })
        report_rows.append({
            "document_id": document_id,
            "raw_source_path": safe_relative(raw_path),
            "raw_chars": len(raw_text),
            "normalized_chars": len(normalized),
            "segments": len(chunks),
        })

    output_path = resolve_project_path(args.output)
    write_jsonl(output_path, output_rows)
    report = {
        "check": "build-segments-from-raw",
        "manifest": safe_relative(manifest_path),
        "output": safe_relative(output_path),
        "segment_count": len(output_rows),
        "sources": report_rows,
        "generated_at": now_iso(),
    }
    report_path = resolve_project_path(args.report)
    write_json(report_path, report)
    print(f"Generated {len(output_rows)} segment(s): {output_path}")
    print(f"Build report: {report_path}")


def load_terms(path: Path) -> list[dict[str, str]]:
    return [row for row in read_csv(path) if row.get("term", "").strip()]


def export_lexicon(args: argparse.Namespace) -> None:
    lexicon_path = resolve_project_path(args.lexicon)
    rows = load_terms(lexicon_path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get("category", "uncategorized") or "uncategorized", []).append(row)
    output_path = resolve_project_path(args.output)
    write_json(output_path, grouped)
    print(f"Exported {len(rows)} lexicon term(s): {output_path}")


def generate_kwic(args: argparse.Namespace) -> None:
    segments_path = resolve_project_path(args.segments)
    lexicon_path = resolve_project_path(args.lexicon)
    segments = read_jsonl(segments_path)
    terms = load_terms(lexicon_path)
    rows: list[dict[str, object]] = []

    for segment in segments:
        text = str(segment.get("text", ""))
        for entry in terms:
            term = entry.get("term", "").strip()
            if not term:
                continue
            start = 0
            while True:
                idx = text.find(term, start)
                if idx == -1:
                    break
                rows.append({
                    "document_id": str(segment.get("document_id", "")),
                    "segment_id": str(segment.get("segment_id", "")),
                    "term": term,
                    "normalized_form": entry.get("normalized_form", term),
                    "category": entry.get("category", ""),
                    "subcategory": entry.get("subcategory", ""),
                    "position": idx,
                    "left_context": text[max(0, idx - args.window):idx],
                    "right_context": text[idx + len(term):idx + len(term) + args.window],
                    "evidence_quote": text,
                    "review_status": "candidate",
                })
                start = idx + len(term)

    fieldnames = [
        "document_id",
        "segment_id",
        "term",
        "normalized_form",
        "category",
        "subcategory",
        "position",
        "left_context",
        "right_context",
        "evidence_quote",
        "review_status",
    ]
    output_path = resolve_project_path(args.output)
    write_csv(output_path, rows, fieldnames)
    print(f"Generated {len(rows)} KWIC row(s): {output_path}")


def generate_evidence_table(args: argparse.Namespace) -> None:
    kwic_path = resolve_project_path(args.kwic)
    rows = read_csv(kwic_path)
    evidence_rows: list[dict[str, object]] = []
    limit = args.limit if args.limit and args.limit > 0 else len(rows)

    for index, row in enumerate(rows[:limit], start=1):
        term = row.get("term", "")
        evidence_rows.append({
            "evidence_id": f"EVID-AUTO-{index:05d}",
            "document_id": row.get("document_id", ""),
            "segment_id": row.get("segment_id", ""),
            "term": term,
            "claim_type": "term_context",
            "evidence_quote": row.get("evidence_quote", ""),
            "observation_zh": f"术语「{term}」出现在该段文本中；其解释意义需要人工复核。",
            "observation_en": f"The term '{term}' appears in this segment; its interpretive significance requires human review.",
            "review_status": "candidate",
            "review_note": "Generated from KWIC; not a final scholarly conclusion.",
        })

    fieldnames = [
        "evidence_id",
        "document_id",
        "segment_id",
        "term",
        "claim_type",
        "evidence_quote",
        "observation_zh",
        "observation_en",
        "review_status",
        "review_note",
    ]
    output_path = resolve_project_path(args.output)
    write_csv(output_path, evidence_rows, fieldnames)
    print(f"Generated {len(evidence_rows)} evidence candidate(s): {output_path}")


def iter_files(base: Path) -> Iterable[Path]:
    skip_dirs = {".git", "__pycache__", ".pytest_cache", "node_modules"}
    for path in sorted(base.rglob("*")):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            yield path


def release_manifest(args: argparse.Namespace) -> None:
    base = resolve_project_path(args.base)
    files: list[dict[str, object]] = []
    for path in iter_files(base):
        files.append({
            "path": safe_relative(path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
    manifest = {
        "project": "DH VR / V2 Research Version",
        "base": safe_relative(base),
        "file_count": len(files),
        "files": files,
        "generated_at": now_iso(),
        "note": "Manifest records repository files for review and release handoff. Generated analysis remains candidate material until human review.",
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, manifest)
    print(f"Release manifest generated with {len(files)} file(s): {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dh_v2", description="DH VR/V2 maintenance CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("validate-documents")
    p.add_argument("--metadata", default=DEFAULT_DOCUMENTS)
    p.add_argument("--output", default="outputs/qc/documents_validation_report.json")
    p.set_defaults(func=validate_documents)

    p = sub.add_parser("validate-raw-sources")
    p.add_argument("--manifest", default=DEFAULT_RAW_MANIFEST)
    p.add_argument("--output", default="outputs/qc/raw_sources_validation_report.json")
    p.set_defaults(func=validate_raw_sources)

    p = sub.add_parser("validate-segments")
    p.add_argument("--segments", default=DEFAULT_SAMPLE_SEGMENTS)
    p.add_argument("--metadata", default=DEFAULT_DOCUMENTS)
    p.add_argument("--output", default="outputs/qc/segments_validation_report.json")
    p.set_defaults(func=validate_segments)

    p = sub.add_parser("build-segments-from-raw")
    p.add_argument("--manifest", default=DEFAULT_RAW_MANIFEST)
    p.add_argument("--output", default=DEFAULT_FULL_SEGMENTS)
    p.add_argument("--report", default="outputs/qc/build_segments_from_raw_report.json")
    p.add_argument("--max-chars", type=int, default=450)
    p.add_argument("--min-chars", type=int, default=120)
    p.set_defaults(func=build_segments_from_raw)

    p = sub.add_parser("export-lexicon")
    p.add_argument("--lexicon", default=DEFAULT_LEXICON)
    p.add_argument("--output", default="outputs/features/domain_lexicon.json")
    p.set_defaults(func=export_lexicon)

    p = sub.add_parser("generate-kwic")
    p.add_argument("--segments", default=DEFAULT_SAMPLE_SEGMENTS)
    p.add_argument("--lexicon", default=DEFAULT_LEXICON)
    p.add_argument("--output", default="outputs/features/kwic_terms.csv")
    p.add_argument("--window", type=int, default=18)
    p.set_defaults(func=generate_kwic)

    p = sub.add_parser("generate-evidence-table")
    p.add_argument("--kwic", default="outputs/features/kwic_terms.csv")
    p.add_argument("--output", default="outputs/features/evidence_table_candidates.csv")
    p.add_argument("--limit", type=int, default=200)
    p.set_defaults(func=generate_evidence_table)

    p = sub.add_parser("release-manifest")
    p.add_argument("--base", default=".")
    p.add_argument("--output", default="releases/manifest.json")
    p.set_defaults(func=release_manifest)

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
