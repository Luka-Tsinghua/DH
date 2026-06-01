# DH V2：明清西学文本与跨文化知识史研究项目
# DH V2: Ming-Qing Western Learning Texts and Transcultural Knowledge History Project

V2 是本仓库的当前主版本。它不再只是 V1 工作坊成果的整理，而是一个面向长期研究、教学复用和可持续维护的人文学术基础设施。

V2 is the current main version of this repository. It is no longer only a cleaned-up continuation of the V1 workshop materials, but a humanities research infrastructure designed for long-term research, teaching reuse, and sustainable maintenance.

---

## 1. 当前成熟度 / Current Maturity

V2 目前已经具备项目骨架、配置、metadata、schema、CLI、真实仓库文本 raw source manifest、真实文本摘录 segment、KWIC、claim review、解释札记和维护计划。此前的 `sample_segments.jsonl` 只保留为 pipeline smoke test，不再作为研究主线。

V2 now contains a project scaffold, configuration, metadata, schemas, CLI, a raw source manifest for existing repository texts, real-text excerpt segments, KWIC output, claim review, interpretive note, and maintenance plan. The earlier `sample_segments.jsonl` is retained only for pipeline smoke testing and is no longer the research main line.

| 层级 / Layer | 位置 / Location | 当前状态 / Current Status |
|---|---|---|
| 项目配置 / Project configuration | `V2/config/project.yml` | 已建立 / established |
| 领域词表 / Domain lexicon | `V2/config/domain_lexicon_seed.csv` | 已建立 seed，可扩展 / seed established, extensible |
| 文献 metadata / Document metadata | `V2/data/metadata/documents_seed.csv` | 已有两条 pilot records / two pilot records available |
| 原始文本登记 / Raw source manifest | `V2/data/raw/RAW_SOURCE_MANIFEST.csv` | 已指向仓库根目录真实文本 / points to existing root-level real texts |
| 真实摘录 segment / Real excerpt segments | `V2/data/processed/verified_excerpt_segments.jsonl` | 已建立 / established |
| 数据模型 / Data schemas | `V2/schemas/` | 已有 Document、Segment、Claim、AuthorityCrosswalk 等 schema / Document, Segment, Claim, AuthorityCrosswalk schemas available |
| CLI 入口 / CLI entry point | `V2/scripts/dh_v2.py` | 可运行最低维护命令 / minimum maintenance commands available |
| 测试样例 / Smoke-test sample | `V2/data/processed/sample_segments.jsonl` | 仅用于测试 pipeline / only for smoke testing |
| 研究案例 / Research case | `V2/cases/kunyu_diqiu_comparison/` | 已使用真实仓库文本摘录 / uses real repository-text excerpts |
| 维护计划 / Maintenance plan | `V2/docs/MAINTENANCE_PLAN.md` | 已建立 / established |

---

## 2. 快速开始 / Quick Start

进入仓库根目录后，可以直接运行以下命令。

From the repository root, run the following commands.

```bash
python V2/scripts/dh_v2.py validate-documents
python V2/scripts/dh_v2.py validate-segments --segments data/processed/verified_excerpt_segments.jsonl
python V2/scripts/dh_v2.py export-lexicon
python V2/scripts/dh_v2.py generate-kwic --segments data/processed/verified_excerpt_segments.jsonl --output cases/kunyu_diqiu_comparison/kwic_terms.csv
python V2/scripts/dh_v2.py release-manifest
```

这些命令不会替代人文学术解释。它们只负责保证项目的 metadata、segment、词表、KWIC 和 release manifest 可以被重复生成。

These commands do not replace humanistic interpretation. They only ensure that metadata, segments, lexicons, KWIC tables, and release manifests can be regenerated.

---

## 3. 目录结构 / Directory Structure

```text
V2/
├── README.md
├── pyproject.toml
├── config/
│   ├── project.yml
│   └── domain_lexicon_seed.csv
├── data/
│   ├── README.md
│   ├── raw/
│   │   └── RAW_SOURCE_MANIFEST.csv
│   ├── metadata/
│   │   └── documents_seed.csv
│   ├── processed/
│   │   ├── verified_excerpt_segments.jsonl
│   │   └── sample_segments.jsonl
│   └── external_authorities/
│       └── authority_crosswalk_seed.csv
├── schemas/
│   ├── document.schema.json
│   ├── segment.schema.json
│   ├── claim.schema.json
│   └── authority_crosswalk.schema.json
├── scripts/
│   ├── __init__.py
│   └── dh_v2.py
├── tests/
│   └── test_cli_smoke.py
├── templates/
│   └── research_case/
├── cases/
│   └── kunyu_diqiu_comparison/
│       ├── README.md
│       ├── evidence_table.csv
│       ├── kwic_terms.csv
│       ├── claims_review.csv
│       └── interpretive_note.md
├── docs/
│   ├── MAINTENANCE_PLAN.md
│   ├── PROJECT_MATURITY_CHECKLIST.md
│   ├── ROADMAP.md
│   └── CI_WORKFLOW_TEMPLATE.md
├── outputs/
└── releases/
```

仓库根目录中的 `1674_坤輿圖說_WS.txt` 与 `1799_地球圖説_WS.txt` 是 V2 当前登记使用的真实 raw source。

The root-level `1674_坤輿圖說_WS.txt` and `1799_地球圖説_WS.txt` are the real raw sources currently registered for V2.

---

## 4. 项目对象 / Project Objects

V2 的核心对象不是“网页页面”，而是可追踪的研究对象。

The core objects of V2 are not web pages, but traceable research objects.

| 对象 / Object | 作用 / Function |
|---|---|
| Document | 保存文献级信息，例如题名、作者、年代、来源、OCR 状态、权利状态。 / Stores document-level information such as title, author, date, source, OCR status, and rights status. |
| RawSource | 登记真实原始文本路径，不覆盖原始材料。 / Registers real raw text paths without overwriting source materials. |
| Segment | 保存可引用文本片段，每段必须有 `document_id` 和 `segment_id`。 / Stores citable textual segments; every segment must have `document_id` and `segment_id`. |
| Term | 保存术语、规范形式、类别和说明。 / Stores terms, normalized forms, categories, and notes. |
| Claim | 保存知识命题候选、证据引文、抽取方法和人工复核状态。 / Stores candidate knowledge claims, evidence quotes, extraction methods, and human review status. |
| Case | 保存一个可复核的小型研究单元。 / Stores a reviewable small research unit. |
| Release | 保存可发布版本的 manifest 和说明。 / Stores manifest and notes for a publishable version. |

---

## 5. 最小 pipeline / Minimum Pipeline

V2 的最低闭环如下。

The minimum closed loop of V2 is as follows.

```text
raw_source_manifest
  ↓
metadata
  ↓
segments
  ↓
lexicon
  ↓
KWIC
  ↓
claims_review
  ↓
interpretive_note
  ↓
release_manifest
```

每一步都必须保留证据、来源和不确定性。

Every step must preserve evidence, source information, and uncertainty.

---

## 6. 真实文本与样例数据 / Real Texts and Sample Data

V2 当前研究主线使用 `verified_excerpt_segments.jsonl`，其段落来自仓库根目录已有的《坤輿圖說》和《地球圖説》文本。`sample_segments.jsonl` 仅用于 smoke test，不应进入正式研究解释。

The V2 research main line currently uses `verified_excerpt_segments.jsonl`, whose segments derive from the existing root-level *Kunyu Tushuo* and *Diqiu Tushuo* text files. `sample_segments.jsonl` is only for smoke testing and should not enter formal research interpretation.

正式研究的下一步不是“替换 sample”，而是从根目录 raw source 自动生成完整 segment JSONL，并补充版本、页码、卷次、OCR 状态和校勘说明。

The next formal step is not merely to “replace samples,” but to generate full segment JSONL from the root-level raw sources and add edition, page, fascicle, OCR status, and collation notes.

---

## 7. 新增文献 / Adding a New Text

新增文献时，不应直接把文本放进仓库后开始分析，而应经过固定流程。

When adding a new text, do not simply place it in the repository and start analysis. Follow a fixed workflow.

1. 将原始文件放入 `V2/data/raw/`，或在 `RAW_SOURCE_MANIFEST.csv` 登记既有仓库路径。
2. 在 `V2/data/metadata/documents_seed.csv` 添加 metadata。
3. 运行 `validate-documents`。
4. 建立 segment JSONL。
5. 运行 `validate-segments`。
6. 按需要扩展 `domain_lexicon_seed.csv`。
7. 生成 KWIC。
8. 建立或扩展研究 case。
9. 对 claim 做人工复核。
10. 写 interpretive note。

1. Place raw files in `V2/data/raw/`, or register existing repository paths in `RAW_SOURCE_MANIFEST.csv`.
2. Add metadata to `V2/data/metadata/documents_seed.csv`.
3. Run `validate-documents`.
4. Create segment JSONL.
5. Run `validate-segments`.
6. Extend `domain_lexicon_seed.csv` if needed.
7. Generate KWIC.
8. Create or extend a research case.
9. Manually review claims.
10. Write an interpretive note.

---

## 8. 新增研究案例 / Adding a New Research Case

每个研究案例至少应包含以下文件。

Each research case should contain at least the following files.

```text
case_name/
├── README.md
├── evidence_table.csv
├── kwic_terms.csv
├── claims_review.csv
└── interpretive_note.md
```

研究案例不是展示页，而是证据、方法、复核和解释的组合。

A research case is not a display page. It is a combination of evidence, method, review, and interpretation.

---

## 9. 发展路线 / Development Roadmap

### Phase 1: Scaffold stabilization
### 第一阶段：项目骨架稳定化

- 保持 README、config、metadata、schemas、CLI、tests 一致。
- Keep README, config, metadata, schemas, CLI, and tests consistent.

### Phase 2: Full-source segmentation
### 第二阶段：完整原文分段

- 从 `1674_坤輿圖說_WS.txt` 和 `1799_地球圖説_WS.txt` 自动生成完整 segment JSONL。
- Generate full segment JSONL from `1674_坤輿圖說_WS.txt` and `1799_地球圖説_WS.txt`.

### Phase 3: Case completion
### 第三阶段：完成第一个研究案例

- 补全 KWIC、evidence table、claims review 和 interpretive note。
- Complete KWIC, evidence table, claims review, and interpretive note.

### Phase 4: Corpus expansion
### 第四阶段：扩展语料

- 加入更多明清西学文献，复用同一 metadata、segment、claim 和 case 结构。
- Add more Ming-Qing Western Learning texts while reusing the same metadata, segment, claim, and case structure.

### Phase 5: Scholarly interface
### 第五阶段：学术界面

- 在不牺牲证据透明性的前提下建设网页界面。
- Build a web interface without sacrificing evidence transparency.

---

## 10. 判断标准 / Maturity Criteria

只有当以下条件满足时，V2 才能称为成熟项目。

V2 should be considered mature only when the following conditions are met.

- 至少一个研究案例使用真实仓库文本，而不是 synthetic sample。
- At least one research case uses real repository text rather than synthetic sample data.
- 每条 claim 都有 evidence quote 和 review status。
- Every claim has an evidence quote and review status.
- metadata、segment、KWIC、claim review 和 release manifest 可以重复生成。
- Metadata, segments, KWIC, claim review, and release manifest can be regenerated.
- 新增文献有稳定流程，而不是临时处理。
- New texts can be added through a stable workflow rather than ad hoc processing.
- README、V2 README 和维护文档保持一致。
- The root README, V2 README, and maintenance documentation remain consistent.

---

## 11. 研究底线 / Scholarly Bottom Line

V2 的最终目标不是让机器替研究者做结论，而是让研究者更可靠地组织材料、保存证据、控制不确定性，并提出可以被复核的解释。

The final goal of V2 is not to let machines make conclusions for researchers. It is to help researchers organize sources, preserve evidence, control uncertainty, and formulate interpretations that can be reviewed.
