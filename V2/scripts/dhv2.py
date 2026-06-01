#!/usr/bin/env python3
"""DH VR/V2 command line utility.

This script is intentionally dependency-light. It gives the V2 project a
maintainable command surface before heavier NLP, database, or web layers are
introduced.

Core commands:

    python V2/scripts/dhv2.py validate-metadata
    python V2/scripts/dhv2.py extract-terms
    python V2/scripts/dhv2.py generate-manifest

The script treats machine outputs as intermediate files. It does not overwrite
raw data and does not make scholarly claims by itself.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
V2_ROOT = REPO_ROOT / "V2"

DOCUMENTS_CSV = V2_ROOT / "data" / "metadata" / "documents.csv"
SEGMENTS_JSONL = V2_ROOT / "data" / "metadata" / "segments.sample.jsonl"
LEXICON_CSV = V2_ROOT / "config" / "domain_lexicon_seed.csv"
QC_DIR = V2_ROOT / "outputs" / "qc"
FEATURE_DIR = V2_ROOT / "outputs" / "features"
RELEASE_DIR = V2_ROOT / "releases"

DOCUMENT_REQUIRED_COLUMNS = [
    "document_id",
    "title_original",
    "title_normalized",
    "year_standard",
    "source_status",
    "ocr_status",
    "rights_status",
]

ALLOWED_SOURCE_STATUS = {"verified", "candidate", "missing", "unclear"}
ALLOWED_OCR_STATUS = {"not_started", "raw_ocr", "sample_checked", "collated", "unclear"}
ALLOWED_RIGHTS_STATUS = {"open", "restricted", "unknown", "do_not_publish_raw"}


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str]
    warnings: List[str]


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_jsonl(path: Path) -> List[Dict[str, object]]:
    if not path.exists():
        return []
    rows: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_documents(path: Path = DOCUMENTS_CSV) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []
    rows = read_csv(path)

    if not rows:
        errors.append("documents.csv has no data rows.")
        return ValidationResult(False, errors, warnings)

    columns = set(rows[0].keys())
    for col in DOCUMENT_REQUIRED_COLUMNS:
        if col not in columns:
            errors.append(f"Missing required column: {col}")

    seen: set[str] = set()
    for idx, row in enumerate(rows, start=2):
        doc_id = row.get("document_id", "").strip()
        if not doc_id:
            errors.append(f"Row {idx}: document_id is empty.")
        elif doc_id in seen:
            errors.append(f"Row {idx}: duplicate document_id: {doc_id}")
        seen.add(doc_id)

        if row.get("source_status", "") not in ALLOWED_SOURCE_STATUS:
            errors.append(f"Row {idx}: invalid source_status: {row.get('source_status')}")
        if row.get("ocr_status", "") not in ALLOWED_OCR_STATUS:
            errors.append(f"Row {idx}: invalid ocr_status: {row.get('ocr_status')}")
        if row.get("rights_status", "") not in ALLOWED_RIGHTS_STATUS:
            errors.append(f"Row {idx}: invalid rights_status: {row.get('rights_status')}")

        if row.get("source_status") != "verified":
            warnings.append(f"Row {idx}: source is not yet verified: {doc_id}")
        if row.get("rights_status") == "unknown":
            warnings.append(f"Row {idx}: rights status is unknown: {doc_id}")

    return ValidationResult(not errors, errors, warnings)


def validate_segments(
    documents_path: Path = DOCUMENTS_CSV,
    segments_path: Path = SEGMENTS_JSONL,
) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []
    documents = read_csv(documents_path)
    document_ids = {row["document_id"] for row in documents if row.get("document_id")}
    segments = read_jsonl(segments_path)

    seen_segments: set[str] = set()
    for idx, row in enumerate(segments, start=1):
        segment_id = str(row.get("segment_id", "")).strip()
        document_id = str(row.get("document_id", "")).strip()
        text = str(row.get("text", ""))

        if not segment_id:
            errors.append(f"Segment line {idx}: missing segment_id.")
        elif segment_id in seen_segments:
            errors.append(f"Segment line {idx}: duplicate segment_id: {segment_id}")
        seen_segments.add(segment_id)

        if document_id not in document_ids:
            errors.append(f"Segment line {idx}: unknown document_id: {document_id}")
        if not text.strip():
            errors.append(f"Segment line {idx}: empty text.")
        if "placeholder" in str(row.get("notes", "")).lower() or "样本" in text:
            warnings.append(f"Segment line {idx}: appears to be placeholder/sample text: {segment_id}")

    if not segments:
        warnings.append("No segment records found. Add JSONL records before feature extraction.")

    return ValidationResult(not errors, errors, warnings)


def command_validate_metadata(args: argparse.Namespace) -> int:
    doc_result = validate_documents(Path(args.documents))
    seg_result = validate_segments(Path(args.documents), Path(args.segments))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "documents_file": args.documents,
        "segments_file": args.segments,
        "documents": {
            "ok": doc_result.ok,
            "errors": doc_result.errors,
            "warnings": doc_result.warnings,
        },
        "segments": {
            "ok": seg_result.ok,
            "errors": seg_result.errors,
            "warnings": seg_result.warnings,
        },
    }
    output = Path(args.output)
    write_json(output, payload)

    print(f"Wrote validation report: {output}")
    if doc_result.errors or seg_result.errors:
        print("Validation failed.", file=sys.stderr)
        return 1
    print("Validation completed with no blocking errors.")
    return 0


def load_lexicon(path: Path) -> List[Dict[str, str]]:
    rows = read_csv(path)
    terms = []
    for row in rows:
        term = row.get("term", "").strip()
        if term:
            terms.append(row)
    return terms


def command_extract_terms(args: argparse.Namespace) -> int:
    segments = read_jsonl(Path(args.segments))
    lexicon = load_lexicon(Path(args.lexicon))
    rows: List[Dict[str, object]] = []

    for segment in segments:
        text = str(segment.get("text", ""))
        document_id = str(segment.get("document_id", ""))
        segment_id = str(segment.get("segment_id", ""))
        for entry in lexicon:
            term = entry["term"]
            start = 0
            while True:
                pos = text.find(term, start)
                if pos < 0:
                    break
                left = text[max(0, pos - args.window):pos]
                right = text[pos + len(term):pos + len(term) + args.window]
                rows.append({
                    "document_id": document_id,
                    "segment_id": segment_id,
                    "term": term,
                    "normalized_form": entry.get("normalized_form", term),
                    "category": entry.get("category", ""),
                    "subcategory": entry.get("subcategory", ""),
                    "position": pos,
                    "left_context": left,
                    "right_context": right,
                    "extraction_method": "literal_lexicon_match",
                    "review_status": "candidate",
                })
                start = pos + len(term)

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
        "extraction_method",
        "review_status",
    ]
    output = Path(args.output)
    write_csv(output, rows, fieldnames)
    print(f"Wrote {len(rows)} term hits: {output}")
    return 0


def iter_project_files(base: Path) -> Iterable[Path]:
    skip_dirs = {".git", "__pycache__", ".pytest_cache", "node_modules"}
    for path in base.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            yield path


def _relative_to_repo(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def command_generate_manifest(args: argparse.Namespace) -> int:
    base = Path(args.base)
    files = []
    for path in sorted(iter_project_files(base)):
        files.append({
            "path": _relative_to_repo(path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })

    payload = {
        "project": "DH VR / V2 Research Version",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base": _relative_to_repo(base),
        "file_count": len(files),
        "files": files,
    }
    output = Path(args.output)
    write_json(output, payload)
    print(f"Wrote release manifest with {len(files)} files: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DH VR/V2 project utility")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate-metadata", help="validate document and segment metadata")
    p_validate.add_argument("--documents", default=str(DOCUMENTS_CSV))
    p_validate.add_argument("--segments", default=str(SEGMENTS_JSONL))
    p_validate.add_argument("--output", default=str(QC_DIR / "metadata_validation_report.json"))
    p_validate.set_defaults(func=command_validate_metadata)

    p_terms = sub.add_parser("extract-terms", help="extract literal lexicon matches from segment JSONL")
    p_terms.add_argument("--segments", default=str(SEGMENTS_JSONL))
    p_terms.add_argument("--lexicon", default=str(LEXICON_CSV))
    p_terms.add_argument("--output", default=str(FEATURE_DIR / "term_hits.csv"))
    p_terms.add_argument("--window", type=int, default=12)
    p_terms.set_defaults(func=command_extract_terms)

    p_manifest = sub.add_parser("generate-manifest", help="generate a file manifest for V2 release review")
    p_manifest.add_argument("--base", default=str(V2_ROOT))
    p_manifest.add_argument("--output", default=str(RELEASE_DIR / "manifest.json"))
    p_manifest.set_defaults(func=command_generate_manifest)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
