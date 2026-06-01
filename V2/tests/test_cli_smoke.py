from __future__ import annotations

import importlib.util
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "dh_v2.py"


def load_cli_module():
    spec = importlib.util.spec_from_file_location("dh_v2", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def as_cli_path(path: Path) -> str:
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def test_validate_documents_generates_qc_report(tmp_path):
    module = load_cli_module()
    output = tmp_path / "documents_validation.json"
    module.main([
        "validate-documents",
        "--metadata",
        "data/metadata/documents_seed.csv",
        "--output",
        as_cli_path(output),
    ])
    assert output.exists()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["row_count"] >= 2
    assert report["error_count"] == 0


def test_validate_raw_sources_uses_existing_root_texts(tmp_path):
    module = load_cli_module()
    output = tmp_path / "raw_sources_validation.json"
    module.main([
        "validate-raw-sources",
        "--manifest",
        "data/raw/RAW_SOURCE_MANIFEST.csv",
        "--output",
        as_cli_path(output),
    ])
    assert output.exists()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["row_count"] >= 2
    assert report["error_count"] == 0
    assert all(item["exists"] for item in report["checked"])


def test_build_segments_from_raw_generates_full_segments(tmp_path):
    module = load_cli_module()
    output = tmp_path / "full_segments.jsonl"
    report = tmp_path / "raw_segment_build_report.json"
    module.main([
        "build-segments-from-raw",
        "--manifest",
        "data/raw/RAW_SOURCE_MANIFEST.csv",
        "--output",
        as_cli_path(output),
        "--report",
        as_cli_path(report),
        "--max-chars",
        "800",
        "--min-chars",
        "120",
    ])
    assert output.exists()
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) >= 2
    assert {row["document_id"] for row in rows} >= {"kunyutushuo_1674", "diqiutushuo_1799"}
    assert all(row["text_type"] == "full_text_segment_from_repository_raw_text" for row in rows)
    assert report.exists()


def test_export_lexicon_generates_grouped_json(tmp_path):
    module = load_cli_module()
    output = tmp_path / "domain_lexicon.json"
    module.main([
        "export-lexicon",
        "--lexicon",
        "config/domain_lexicon_seed.csv",
        "--output",
        as_cli_path(output),
    ])
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert "geography" in data
    assert any(row["term"] == "地球" for row in data["geography"])


def test_generate_kwic_and_evidence_from_real_excerpt_segments(tmp_path):
    module = load_cli_module()
    kwic = tmp_path / "kwic_terms.csv"
    evidence = tmp_path / "evidence_table.csv"
    module.main([
        "generate-kwic",
        "--segments",
        "data/processed/verified_excerpt_segments.jsonl",
        "--lexicon",
        "config/domain_lexicon_seed.csv",
        "--output",
        as_cli_path(kwic),
    ])
    assert kwic.exists()
    assert "地球" in kwic.read_text(encoding="utf-8")

    module.main([
        "generate-evidence-table",
        "--kwic",
        as_cli_path(kwic),
        "--output",
        as_cli_path(evidence),
        "--limit",
        "5",
    ])
    assert evidence.exists()
    text = evidence.read_text(encoding="utf-8")
    assert "candidate" in text
    assert "evidence_quote" in text
