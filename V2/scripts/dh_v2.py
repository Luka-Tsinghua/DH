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
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def resolve_repo_path(value: str) -> Path:
    """Resolve paths that may be relative to V2 or to the repository root."""
    path = Path(value)
    if path.is_absolute():
        return path
    project_candidate = PROJECT_ROOT / path
    if project_candidate.exists():
        return project_candidate
    return REPO_ROOT / path


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_ws_text(text: str) -> str:
    """Normalize WS/OCR-style text by removing tokenization whitespace.

    The root-level WS files store Chinese text with heavy spacing between tokens.
    For KWIC and segment-level evidence, V2 keeps a normalized continuous text.
    Formal philological citation should still check the raw source file.
    """
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
    seen: set[str] = set()

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

    report = {
        "check": "validate-documents",
        "metadata": str(metadata_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "errors": errors,
        "generated_at": datetime.now(timezone.utc).isoformat(),
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
            "raw_source_path": str(raw_path),
            "exists": exists,
            "size_bytes": raw_path.stat().st_size if exists else 0,
        })

    report = {
        "check": "validate-raw-sources",
        "manifest": str(manifest_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "errors": errors,
        "checked": checked,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, report)
    if errors:
        print(f"Raw source validation failed: {len(errors)} error(s). See {output_path}")
        raise SystemExit(1)
    print(f"Raw source validation passed: {len(rows)} source(s). Report: {output_path}")


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
                "notes": "Generated from registered root-level WS raw text. Whitespace removed; verify against raw source before final scholarly citation.",
            })
        report_rows.append({
            "document_id": document_id,
            "raw_source_path": str(raw_path),
            "raw_chars": len(raw_text),
            "normalized_chars": len(normalized),
            "segments": len(chunks),
        })

    output_path = resolve_project_path(args.output)
    write_jsonl(output_path, output_rows)
    report = {
        "check": "build-segments-from-raw",
        "manifest": str(manifest_path),
        "output": str(output_path),
        "segment_count": len(output_rows),
        "sources": report_rows,
        "parameters": {"max_chars": max_chars, "min_chars": min_chars},
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    report_path = resolve_project_path(args.report)
    write_json(report_path, report)
    print(f"Full segments written: {output_path} ({len(output_rows)} segment(s)); report: {report_path}")


def validate_segments(args: argparse.Namespace) -> None:
    segment_path = resolve_project_path(args.segments)
    rows = read_jsonl(segment_path)
    required = ["segment_id", "document_id", "segment_index", "text"]
    errors: list[str] = []
    seen: set[str] = set()
    for i, row in enumerate(rows, start=1):
        for field in required:
            if field not in row or str(row.get(field, "")).strip() == "":
                errors.append(f"row {i}: missing required field {field}")
        segment_id = str(row.get("segment_id", "")).strip()
        if segment_id in seen:
            errors.append(f"row {i}: duplicate segment_id {segment_id}")
        seen.add(segment_id)
    report = {
        "check": "validate-segments",
        "segments": str(segment_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "errors": errors,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, report)
    if errors:
        print(f"Segment validation failed: {len(errors)} error(s). See {output_path}")
        raise SystemExit(1)
    print(f"Segment validation passed: {len(rows)} segment(s). Report: {output_path}")


def inventory(args: argparse.Namespace) -> None:
    target = resolve_project_path(args.path)
    files = []
    for p in sorted(target.rglob("*")) if target.exists() else []:
        if p.is_file():
            files.append({
                "path": str(p.relative_to(PROJECT_ROOT)),
                "size_bytes": p.stat().st_size,
                "suffix": p.suffix,
            })
    output_path = resolve_project_path(args.output)
    write_json(output_path, {
        "check": "inventory",
        "root": str(target),
        "file_count": len(files),
        "files": files,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    })
    print(f"Inventory written: {output_path}")


def export_lexicon(args: argparse.Namespace) -> None:
    lexicon_path = resolve_project_path(args.lexicon)
    rows = read_csv(lexicon_path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get("category", "uncategorized"), []).append(row)
    output_path = resolve_project_path(args.output)
    write_json(output_path, grouped)
    print(f"Lexicon exported: {output_path}")


def generate_kwic(args: argparse.Namespace) -> None:
    segment_path = resolve_project_path(args.segments)
    lexicon_path = resolve_project_path(args.lexicon)
    rows = read_jsonl(segment_path)
    terms = [row["term"] for row in read_csv(lexicon_path) if row.get("term")]
    window = max(args.window, 1)
    output_rows: list[dict[str, str]] = []
    for row in rows:
        text = str(row.get("text", ""))
        for term in terms:
            start = 0
            while True:
                idx = text.find(term, start)
                if idx == -1:
                    break
                output_rows.append({
                    "document_id": str(row.get("document_id", "")),
                    "segment_id": str(row.get("segment_id", "")),
                    "term": term,
                    "left_context": text[max(0, idx - window):idx],
                    "right_context": text[idx + len(term):idx + len(term) + window],
                    "evidence_quote": text,
                })
                start = idx + len(term)
    output_path = resolve_project_path(args.output)
    fieldnames = ["document_id", "segment_id", "term", "left_context", "right_context", "evidence_quote"]
    write_csv(output_path, output_rows, fieldnames)
    print(f"KWIC written: {output_path} ({len(output_rows)} hit(s))")


def generate_evidence_table(args: argparse.Namespace) -> None:
    kwic_path = resolve_project_path(args.kwic)
    kwic_rows = read_csv(kwic_path)
    output_rows: list[dict[str, str]] = []
    limit = args.limit if args.limit and args.limit > 0 else None
    for index, row in enumerate(kwic_rows[:limit], start=1):
        term = row.get("term", "")
        output_rows.append({
            "evidence_id": f"EVID-AUTO-{index:05d}",
            "document_id": row.get("document_id", ""),
            "segment_id": row.get("segment_id", ""),
            "term": term,
            "claim_type": "term_context",
            "evidence_quote": row.get("evidence_quote", ""),
            "observation_zh": f"术语「{term}」出现在该段文本中；具体解释需人工复核。",
            "observation_en": f"The term '{term}' appears in this segment; interpretation requires human review.",
            "review_status": "candidate",
            "review_note": "Generated from KWIC; not a scholarly conclusion.",
        })
    output_path = resolve_project_path(args.output)
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
    write_csv(output_path, output_rows, fieldnames)
    print(f"Evidence table written: {output_path} ({len(output_rows)} row(s))")


def generate_release_manifest(args: argparse.Namespace) -> None:
    paths = [
        "config",
        "data/raw",
        "data/metadata",
        "data/processed",
        "data/external_authorities",
        "schemas",
        "scripts",
        "cases",
        "docs",
        "templates",
        "tests",
    ]
    files = []
    for relative in paths:
        root = PROJECT_ROOT / relative
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file():
                files.append({
                    "path": str(p.relative_to(PROJECT_ROOT)),
                    "size_bytes": p.stat().st_size,
                })
    manifest = {
        "project": "DH VR / V2 Research Version",
        "release_name": args.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "included_files": files,
        "notes": "This manifest lists V2 project-maintenance files. Registered root-level raw sources are listed in data/raw/RAW_SOURCE_MANIFEST.csv.",
    }
    output_path = resolve_project_path(args.output)
    write_json(output_path, manifest)
    print(f"Release manifest written: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dh_v2", description="DH VR/V2 maintenance CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate-documents", help="Validate document metadata CSV")
    p_validate.add_argument("--metadata", default="data/metadata/documents_seed.csv")
    p_validate.add_argument("--output", default="outputs/qc/documents_validation.json")
    p_validate.set_defaults(func=validate_documents)

    p_raw = sub.add_parser("validate-raw-sources", help="Validate registered raw source files")
    p_raw.add_argument("--manifest", default="data/raw/RAW_SOURCE_MANIFEST.csv")
    p_raw.add_argument("--output", default="outputs/qc/raw_sources_validation.json")
    p_raw.set_defaults(func=validate_raw_sources)

    p_build = sub.add_parser("build-segments-from-raw", help="Build full segment JSONL from registered raw source files")
    p_build.add_argument("--manifest", default="data/raw/RAW_SOURCE_MANIFEST.csv")
    p_build.add_argument("--output", default="data/processed/full_segments.jsonl")
    p_build.add_argument("--report", default="outputs/qc/raw_segment_build_report.json")
    p_build.add_argument("--max-chars", type=int, default=400)
    p_build.add_argument("--min-chars", type=int, default=80)
    p_build.set_defaults(func=build_segments_from_raw)

    p_segments = sub.add_parser("validate-segments", help="Validate a segment JSONL file")
    p_segments.add_argument("--segments", required=True)
    p_segments.add_argument("--output", default="outputs/qc/segments_validation.json")
    p_segments.set_defaults(func=validate_segments)

    p_inventory = sub.add_parser("inventory", help="Inventory files under a project path")
    p_inventory.add_argument("--path", default="data")
    p_inventory.add_argument("--output", default="outputs/qc/inventory.json")
    p_inventory.set_defaults(func=inventory)

    p_lexicon = sub.add_parser("export-lexicon", help="Export domain lexicon CSV to grouped JSON")
    p_lexicon.add_argument("--lexicon", default="config/domain_lexicon_seed.csv")
    p_lexicon.add_argument("--output", default="outputs/features/domain_lexicon.json")
    p_lexicon.set_defaults(func=export_lexicon)

    p_kwic = sub.add_parser("generate-kwic", help="Generate a KWIC table from segment JSONL and lexicon CSV")
    p_kwic.add_argument("--segments", required=True)
    p_kwic.add_argument("--lexicon", default="config/domain_lexicon_seed.csv")
    p_kwic.add_argument("--output", default="outputs/features/kwic_terms.csv")
    p_kwic.add_argument("--window", type=int, default=12)
    p_kwic.set_defaults(func=generate_kwic)

    p_evidence = sub.add_parser("generate-evidence-table", help="Generate candidate evidence rows from a KWIC table")
    p_evidence.add_argument("--kwic", required=True)
    p_evidence.add_argument("--output", default="outputs/features/evidence_table.csv")
    p_evidence.add_argument("--limit", type=int, default=0, help="Maximum rows to export; 0 means all")
    p_evidence.set_defaults(func=generate_evidence_table)

    p_manifest = sub.add_parser("release-manifest", help="Generate a release manifest for project-maintenance files")
    p_manifest.add_argument("--name", default="v2-working-release")
    p_manifest.add_argument("--output", default="releases/release_manifest.json")
    p_manifest.set_defaults(func=generate_release_manifest)

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
