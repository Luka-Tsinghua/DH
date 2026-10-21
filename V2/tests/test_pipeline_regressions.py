from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from test_cli_smoke import load_cli_module

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_release_manifest_excludes_itself_and_local_build_files(tmp_path):
    module = load_cli_module()
    base = tmp_path / "release-input"
    base.mkdir()
    (base / "research.txt").write_text("research input", encoding="utf-8")
    for directory in [".venv", "venv", "build", "dist", "__pycache__", ".pytest_cache", "dh_vr_v2.egg-info"]:
        folder = base / directory
        folder.mkdir()
        (folder / "local-only.txt").write_text("local build product", encoding="utf-8")
    output = base / "manifest.json"
    command = ["release-manifest", "--base", str(base), "--output", str(output)]
    module.main(command)
    first = json.loads(output.read_text(encoding="utf-8"))
    module.main(command)
    second = json.loads(output.read_text(encoding="utf-8"))
    assert first["files"] == second["files"]
    assert second["file_count"] == 1
    assert Path(second["files"][0]["path"]).name == "research.txt"


def test_pipeline_runs_outside_checkout_and_preserves_research_sources(tmp_path):
    repo = tmp_path / "checkout"
    project = repo / "V2"
    shutil.copytree(
        PROJECT_ROOT, project,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.egg-info", "build", "dist",
                                     "full_segments.jsonl", "manifest.json", "features", "qc"),
    )
    for raw in PROJECT_ROOT.parent.glob("*_WS.txt"):
        shutil.copy2(raw, repo / raw.name)
    protected = list(repo.glob("*_WS.txt")) + [
        path for path in (project / "cases").rglob("*")
        if path.is_file() and "generated" not in path.parts
    ]
    original = {path: path.read_bytes() for path in protected}
    result = subprocess.run(
        [sys.executable, str(project / "scripts" / "dh_v2.py"), "pipeline"],
        cwd=tmp_path, capture_output=True, encoding="utf-8", timeout=60,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert all(path.read_bytes() == contents for path, contents in original.items())
    segments = [json.loads(line) for line in
                (project / "data/processed/full_segments.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {row["document_id"] for row in segments} == {"kunyutushuo_1674", "diqiutushuo_1799"}
    with (project / "outputs/features/full_evidence_table.csv").open(encoding="utf-8", newline="") as stream:
        evidence = list(csv.DictReader(stream))
    assert evidence
    assert all(row["review_status"] == "candidate" and row["segment_id"] and row["evidence_quote"]
               for row in evidence)
    config = json.loads((project / "cases/kunyu_diqiu_comparison/case_config.json").read_text(encoding="utf-8"))
    with (project / config["outputs"]["claims"]).open(encoding="utf-8", newline="") as stream:
        claims = list(csv.DictReader(stream))
    assert claims
    assert all(row["claim_status"] == "candidate" for row in claims)
    report = json.loads((project / config["outputs"]["report"]).read_text(encoding="utf-8"))
    assert report["used_fallback_segments"] is False
    manifest = json.loads((project / "releases/manifest.json").read_text(encoding="utf-8"))
    assert not any(row["path"].endswith("releases/manifest.json") for row in manifest["files"])
