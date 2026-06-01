# V2 贡献规范
# V2 Contribution Guidelines

本文件说明如何向 V2 增加材料、脚本、研究案例或文档。V2 不是一次性展示文件夹。每一次修改都应该让项目更容易复核、扩展或维护。

This file explains how to add materials, scripts, research cases, or documentation to V2. V2 is not a one-off display folder. Every change should make the project easier to review, extend, or maintain.

---

## 1. 基本原则 / Basic Principles

- 不覆盖 raw data。
- 不把模型输出直接写成学术结论。
- 不删除看似“脏”的历史文本信息，例如数字、音译词、官职、序跋、页码、卷次、来源说明。
- 不把 generated candidate outputs 与 curated case files 混在一起。
- 每条 claim 都必须保留 evidence quote、document id、segment id 和 review status。

- Do not overwrite raw data.
- Do not turn model outputs directly into scholarly conclusions.
- Do not delete historically meaningful textual information such as numbers, transliterated names, official titles, prefaces, page numbers, fascicle numbers, or source notes.
- Do not mix generated candidate outputs with curated case files.
- Every claim must preserve evidence quote, document id, segment id, and review status.

---

## 2. 新增文献 / Adding Texts

新增文献必须至少完成以下步骤。

A new text must complete at least the following steps.

1. 将 raw source 放入仓库，或在 `V2/data/raw/RAW_SOURCE_MANIFEST.csv` 登记既有仓库路径。
2. 添加 metadata 到 `V2/data/metadata/documents_seed.csv`。
3. 运行 `python scripts/dh_v2.py validate-documents`。
4. 运行 `python scripts/dh_v2.py validate-raw-sources`。
5. 运行 `python scripts/dh_v2.py build-segments-from-raw`。
6. 运行 `python scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl`。
7. 按需要扩展 `V2/config/domain_lexicon_seed.csv`。
8. 建立或扩展 research case。

1. Place the raw source in the repository, or register an existing repository path in `V2/data/raw/RAW_SOURCE_MANIFEST.csv`.
2. Add metadata to `V2/data/metadata/documents_seed.csv`.
3. Run `python scripts/dh_v2.py validate-documents`.
4. Run `python scripts/dh_v2.py validate-raw-sources`.
5. Run `python scripts/dh_v2.py build-segments-from-raw`.
6. Run `python scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl`.
7. Extend `V2/config/domain_lexicon_seed.csv` when needed.
8. Create or extend a research case.

---

## 3. 新增脚本 / Adding Scripts

新增脚本应优先注册到稳定 CLI，或在 README、Makefile、tests 中说明其入口。

New scripts should preferably be registered in a stable CLI or documented in README, Makefile, and tests.

脚本输出应写入 `V2/outputs/`、`V2/cases/<case>/generated/` 或 `V2/releases/`，避免散落在项目根目录。

Script outputs should be written to `V2/outputs/`, `V2/cases/<case>/generated/`, or `V2/releases/`, not scattered in the project root.

---

## 4. 新增研究案例 / Adding Research Cases

每个研究案例至少包含以下文件。

Each research case should include at least the following files.

```text
case_name/
├── case_config.json
├── README.md
├── evidence_table.csv
├── kwic_terms.csv
├── claims_review.csv
├── interpretive_note.md
└── generated/
```

`generated/` 保存脚本候选结果。人工筛选和复核后的结果才进入 case 根目录下的正式 CSV 与 interpretive note。

`generated/` stores script-generated candidate outputs. Only human-selected and reviewed rows should enter the curated CSV files and interpretive note at the case root.

---

## 5. 提交前检查 / Pre-commit Checklist

- README 或 V2 README 是否需要同步更新？
- metadata 是否通过验证？
- raw source manifest 是否通过验证？
- 新增 sample 是否明确标为 sample？
- 新增 claim 是否有 evidence quote？
- 自动生成结果是否标为 candidate？
- 外部数据库或 authority 是否保留来源与授权说明？
- tests 是否覆盖新增 pipeline？
- Makefile 是否需要新增入口？

- Should the root README or V2 README be updated?
- Does metadata pass validation?
- Does the raw source manifest pass validation?
- Are new samples clearly marked as samples?
- Does every new claim have an evidence quote?
- Are automatically generated outputs marked as candidates?
- Do external databases or authorities preserve source and license notes?
- Do tests cover the new pipeline?
- Does the Makefile need a new entry?
