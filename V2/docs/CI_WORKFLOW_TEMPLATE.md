# V2 CI 工作流模板
# V2 CI Workflow Template

平台安全检查阻止了直接写入 `.github/workflows/v2-ci.yml`。因此先在文档中保留可复制的 CI 模板。

A platform safety check blocked direct creation of `.github/workflows/v2-ci.yml`. The reusable CI template is therefore preserved here for manual or agent-side installation.

```yaml
name: V2 minimum project checks

on:
  push:
    branches: ["main"]
    paths:
      - "V2/**"
      - ".github/workflows/v2-ci.yml"
  pull_request:
    branches: ["main"]
    paths:
      - "V2/**"
      - ".github/workflows/v2-ci.yml"

jobs:
  v2-checks:
    name: Validate V2 project scaffold
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

      - name: Validate sample segments
        run: python V2/scripts/dh_v2.py validate-segments --segments data/processed/sample_segments.jsonl

      - name: Export domain lexicon
        run: python V2/scripts/dh_v2.py export-lexicon

      - name: Generate KWIC sample
        run: python V2/scripts/dh_v2.py generate-kwic --segments data/processed/sample_segments.jsonl

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
