#!/usr/bin/env python3
"""Command-line entry point for the DH VR/V2 project.

This script is intentionally small and dependency-light. It provides a stable
entry point for later expansion, so the project does not become a collection of
one-off notebooks or ad hoc scripts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def validate_documents(args: argparse.Namespace) -> None:
    metadata_path = PROJECT_ROOT / args.metadata
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

    report = {
        "metadata": str(metadata_path),
        "row_count": len(rows),
        "error_count": len(errors),
        "errors": errors,
    }
    output_path = PROJECT_ROOT / args.output
    write_json(output_path, report)

    if errors:
        print(f"Validation failed: {len(errors)} error(s). See {output_path}")
        raise SystemExit(1)
    print(f"Validation passed: {len(rows)} document record(s). Report: {output_path}")


def inventory(args: argparse.Namespace) -> None:
    target = PROJECT_ROOT / args.path
    files = []
    for p in sorted(target.rglob("*")):
        if p.is_file():
            files.append({
                "path": str(p.relative_to(PROJECT_ROOT)),
                "size_bytes": p.stat().st_size,
                "suffix": p.suffix,
            })
    output_path = PROJECT_ROOT / args.output
    write_json(output_path, {"root": str(target), "file_count": len(files), "files": files})
    print(f"Inventory written: {output_path}")


def export_lexicon(args: argparse.Namespace) -> None:
    lexicon_path = PROJECT_ROOT / args.lexicon
    rows = read_csv(lexicon_path)
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row.get("category", "uncategorized"), []).append(row)
    output_path = PROJECT_ROOT / args.output
    write_json(output_path, grouped)
    print(f"Lexicon exported: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dh_v2", description="DH VR/V2 maintenance CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate-documents", help="Validate document metadata CSV")
    p_validate.add_argument("--metadata", default="data/metadata/documents_seed.csv")
    p_validate.add_argument("--output", default="outputs/qc/documents_validation.json")
    p_validate.set_defaults(func=validate_documents)

    p_inventory = sub.add_parser("inventory", help="Inventory files under a project path")
    p_inventory.add_argument("--path", default="data")
    p_inventory.add_argument("--output", default="outputs/qc/inventory.json")
    p_inventory.set_defaults(func=inventory)

    p_lexicon = sub.add_parser("export-lexicon", help="Export domain lexicon CSV to grouped JSON")
    p_lexicon.add_argument("--lexicon", default="config/domain_lexicon_seed.csv")
    p_lexicon.add_argument("--output", default="outputs/features/domain_lexicon.json")
    p_lexicon.set_defaults(func=export_lexicon)

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
