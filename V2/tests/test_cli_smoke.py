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


def test_validate_documents_generates_qc_report(tmp_path):
    module = load_cli_module()
    output = tmp_path / "documents_validation.json"
    module.main([
        "validate-documents",
        "--metadata",
        "data/metadata/documents_seed.csv",
        "--output",
        str(output.relative_to(PROJECT_ROOT)) if output.is_relative_to(PROJECT_ROOT) else str(output),
    ])
    assert output.exists()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["row_count"] >= 2
    assert report["error_count"] == 0


def test_export_lexicon_generates_grouped_json(tmp_path):
    module = load_cli_module()
    output = tmp_path / "domain_lexicon.json"
    module.main([
        "export-lexicon",
        "--lexicon",
        "config/domain_lexicon_seed.csv",
        "--output",
        str(output.relative_to(PROJECT_ROOT)) if output.is_relative_to(PROJECT_ROOT) else str(output),
    ])
    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert "geography" in data
    assert any(row["term"] == "地球" for row in data["geography"])
