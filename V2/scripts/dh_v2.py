#!/usr/bin/env python3
"""Command-line entry point for the DH VR/V2 project.

This dependency-light CLI is the project's stable maintenance interface. It is
not a replacement for humanistic interpretation. Its purpose is to keep metadata,
lexicons, evidence tables, case files, and release manifests reproducible.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


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


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


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


def generate_release_manifest(args: argparse.Namespace) -> None:
    paths = [
        "config",
        "data/metadata",
        "schemas",
        "scripts",
        "cases",
        "docs",
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
        "notes": "This manifest lists project-maintenance files, not necessarily redistributable raw source texts.",
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
