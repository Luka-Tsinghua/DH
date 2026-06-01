# V2 CI 工作流模板
# V2 CI Workflow Template

平台安全检查阻止了直接写入 `.github/workflows/v2-ci.yml`。因此先在文档中保留可复制的 CI 模板。

A platform safety check blocked direct creation of `.github/workflows/v2-ci.yml`. The reusable CI template is therefore preserved here for manual or agent-side installation.

```yaml
name: V2 real-text pipeline checks

on:
  push:
    branches: ["main"]
    paths:
      - "V2/**"
      - "1674_坤輿圖說_WS.txt"
      - "1799_地球圖説_WS.txt"
      - ".github/workflows/v2-ci.yml"
  pull_request:
    branches: ["main"]
    paths:
      - "V2/**"
      - "1674_坤輿圖說_WS.txt"
      - "1799_地球圖説_WS.txt"
      - ".github/workflows/v2-ci.yml"

jobs:
  v2-checks:
    name: Validate V2 real-text pipeline
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install test dependency
        run: python -m pip install --upgrade pip pytest

      - name: Validate document metadata
        run: python V2/scripts/dh_v2.py validate-documents

      - name: Validate registered raw sources
        run: python V2/scripts/dh_v2.py validate-raw-sources

      - name: Build full segments from raw repository texts
        run: python V2/scripts/dh_v2.py build-segments-from-raw

      - name: Validate generated full segments
        run: python V2/scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl

      - name: Export domain lexicon
        run: python V2/scripts/dh_v2.py export-lexicon

      - name: Generate KWIC from full segments
        run: python V2/scripts/dh_v2.py generate-kwic --segments data/processed/full_segments.jsonl --output outputs/features/full_kwic_terms.csv

      - name: Generate evidence table from KWIC
        run: python V2/scripts/dh_v2.py generate-evidence-table --kwic outputs/features/full_kwic_terms.csv --output outputs/features/full_evidence_table.csv --limit 200

      - name: Generate release manifest
        run: python V2/scripts/dh_v2.py release-manifest

      - name: Run smoke tests
        run: pytest V2/tests
```

安装路径应为：

Install this workflow at:

```text
.github/workflows/v2-ci.yml
```
