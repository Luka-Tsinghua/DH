from __future__ import annotations

import importlib.util
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "dh_v2.py"
CASE_BUILDER_PATH = PROJECT_ROOT / "scripts" / "build_case.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_cli_module():
    return load_module(SCRIPT_PATH, "dh_v2")


def load_case_builder_module():
    return load_module(CASE_BUILDER_PATH, "build_case")


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


def test_case_builder_generates_candidate_outputs(tmp_path):
    module = load_case_builder_module()
    config = {
        "case_id": "test_case",
        "segments": "data/processed/verified_excerpt_segments.jsonl",
        "lexicon": "config/domain_lexicon_seed.csv",
        "focus_terms": ["坤輿", "地球", "赤道", "經緯"],
        "window": 12,
        "outputs": {
            "kwic": as_cli_path(tmp_path / "case_kwic.csv"),
            "evidence": as_cli_path(tmp_path / "case_evidence.csv"),
            "claims": as_cli_path(tmp_path / "case_claims.csv"),
            "report": as_cli_path(tmp_path / "case_report.json"),
        },
    }
    config_path = tmp_path / "case_config.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")

    module.main(["--config", as_cli_path(config_path)])

    kwic = tmp_path / "case_kwic.csv"
    evidence = tmp_path / "case_evidence.csv"
    claims = tmp_path / "case_claims.csv"
    report = tmp_path / "case_report.json"
    assert kwic.exists()
    assert evidence.exists()
    assert claims.exists()
    assert report.exists()
    report_data = json.loads(report.read_text(encoding="utf-8"))
    assert report_data["case_id"] == "test_case"
    assert report_data["kwic_count"] >= 1
    assert report_data["claim_candidate_count"] >= 1
