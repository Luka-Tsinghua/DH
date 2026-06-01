# DH V2：明清西学文本与跨文化知识史研究项目

V2 是本仓库当前主版本。它的定位不是数字人文工作坊展示页，而是一个面向长期研究、教学复用和持续维护的人文学术基础设施。

## 1. 当前状态

V2 已经把仓库根目录中的真实 WS 文本登记为 raw source，并建立了从 raw source 到 segment、KWIC、evidence、claim、case、release 的可复现 pipeline。`sample_segments.jsonl` 只保留为 smoke test，不再作为研究主线。

当前真实 raw source：

```text
1674_坤輿圖說_WS.txt
1799_地球圖説_WS.txt
```

## 2. 核心结构

```text
V2/
├── README.md
├── Makefile
├── pyproject.toml
├── config/
│   ├── project.yml
│   └── domain_lexicon_seed.csv
├── data/
│   ├── README.md
│   ├── raw/RAW_SOURCE_MANIFEST.csv
│   ├── metadata/documents_seed.csv
│   ├── processed/
│   │   ├── verified_excerpt_segments.jsonl
│   │   └── sample_segments.jsonl
│   └── external_authorities/authority_crosswalk_seed.csv
├── scripts/
│   ├── dh_v2.py
│   └── build_case.py
├── tests/test_cli_smoke.py
├── cases/kunyu_diqiu_comparison/
│   ├── case_config.json
│   ├── README.md
│   ├── evidence_table.csv
│   ├── kwic_terms.csv
│   ├── claims_review.csv
│   ├── interpretive_note.md
│   └── generated/
├── docs/
│   ├── PIPELINE.md
│   ├── METHOD.md
│   ├── MAINTENANCE_PLAN.md
│   ├── PROJECT_MATURITY_CHECKLIST.md
│   ├── ROADMAP.md
│   └── CI_WORKFLOW_TEMPLATE.md
├── outputs/
└── releases/
```

## 3. 一键运行

在 `V2/` 目录下运行：

```bash
make pipeline
```

这会执行：

```text
validate metadata and raw sources
build full text segments
generate KWIC
generate evidence candidates
build case-level candidate outputs
generate release manifest
```

也可以从仓库根目录逐步运行：

```bash
python V2/scripts/dh_v2.py validate-documents
python V2/scripts/dh_v2.py validate-raw-sources
python V2/scripts/dh_v2.py build-segments-from-raw
python V2/scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl
python V2/scripts/dh_v2.py generate-kwic --segments data/processed/full_segments.jsonl --output outputs/features/full_kwic_terms.csv
python V2/scripts/dh_v2.py generate-evidence-table --kwic outputs/features/full_kwic_terms.csv --output outputs/features/full_evidence_table.csv --limit 200
python V2/scripts/build_case.py --config cases/kunyu_diqiu_comparison/case_config.json
python V2/scripts/dh_v2.py release-manifest
```

## 4. 研究对象

V2 的核心对象不是网页，而是可追踪的研究对象。

- `RawSource`：真实原始文本路径。
- `Document`：文献级 metadata。
- `Segment`：可引用文本片段。
- `Term`：术语、规范形式和类别。
- `KWIC`：关键词语境表。
- `Evidence`：候选证据行。
- `Claim`：可复核命题。
- `Case`：一个可复核的小型研究单元。
- `Release`：可交接版本。

## 5. 最小闭环

```text
raw source manifest
  ↓
document metadata
  ↓
full segments
  ↓
lexicon
  ↓
KWIC
  ↓
evidence candidates
  ↓
claim candidates
  ↓
human review
  ↓
interpretive note
  ↓
release manifest
```

自动生成内容只能作为 `candidate`。正式学术结论必须经过人工复核、校勘和解释。

## 6. 当前 case

当前核心 case 是：

```text
V2/cases/kunyu_diqiu_comparison/
```

它比较《坤輿圖說》与《地球圖説》的术语、地理知识表达、图说体裁和制度化翻译语境。`case_config.json` 定义了 focus terms、segment source 和输出路径。`scripts/build_case.py` 可以自动生成 case-level KWIC、evidence candidates、claim candidates 和 build report。

## 7. 新增文献流程

新增文献时，应按以下流程处理：

1. 把 raw source 放入仓库，或登记既有仓库路径。
2. 更新 `V2/data/raw/RAW_SOURCE_MANIFEST.csv`。
3. 更新 `V2/data/metadata/documents_seed.csv`。
4. 运行 `validate-documents` 和 `validate-raw-sources`。
5. 运行 `build-segments-from-raw`。
6. 扩展 `domain_lexicon_seed.csv`。
7. 生成 KWIC 和 evidence candidates。
8. 建立或扩展 research case。
9. 人工复核 claims。
10. 写 interpretive note。

## 8. 新增 case 流程

新增 case 至少应包含：

```text
case_config.json
README.md
evidence_table.csv
kwic_terms.csv
claims_review.csv
interpretive_note.md
generated/
```

`generated/` 保存脚本生成的候选结果。人工筛选和复核后的结果才进入 case 根目录下的正式 CSV 与 interpretive note。

## 9. 成熟度判断

V2 当前已经达到一个真实、可复现、可扩展、可维护的最低项目形态。它已经具备真实 raw source、raw manifest、metadata、segment pipeline、case builder、tests、Makefile、CI template、method note、maintenance plan 和 release manifest 机制。

它仍不是“完成的学术论文”。下一阶段重点是人工复核自动生成的 evidence 和 claims，补充版本、页码、卷次、OCR 状态、校勘说明，并将第一个 case 打磨成可发布的小型数字论文。

## 10. 学术底线

V2 不让机器替研究者下结论。V2 的目标是让研究者更可靠地组织材料、保存证据、控制不确定性，并提出可以被复核的解释。