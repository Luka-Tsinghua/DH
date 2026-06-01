# V2 贡献规范
# V2 Contribution Guidelines

本文件说明如何向 V2 增加材料、脚本、研究案例或文档。

This file explains how to add materials, scripts, research cases, or documentation to V2.

---

## 1. 基本原则 / Basic Principles

不要把 V2 当作一次性展示文件夹。每一次修改都应该让项目更容易复核、扩展或维护。

Do not treat V2 as a one-off display folder. Every change should make the project easier to review, extend, or maintain.

不要覆盖 raw data。不要把模型输出直接写成学术结论。不要删除看似“脏”的历史文本信息，例如数字、音译词、官职、序跋、页码、卷次、来源说明。

Do not overwrite raw data. Do not turn model outputs directly into scholarly conclusions. Do not delete historically meaningful textual information such as numbers, transliterated names, official titles, prefaces, page numbers, fascicle numbers, or source notes.

---

## 2. 新增文献 / Adding Texts

新增文献必须至少完成以下步骤。

A new text must complete at least the following steps.

1. 添加原始文件到 `V2/data/raw/`。
2. 添加 metadata 到 `V2/data/metadata/documents_seed.csv`。
3. 运行 `python V2/scripts/dh_v2.py validate-documents`。
4. 建立 segment JSONL。
5. 运行 `python V2/scripts/dh_v2.py validate-segments --segments <path>`。
6. 在研究案例中添加 evidence table 或 claims review。

1. Add raw files to `V2/data/raw/`.
2. Add metadata to `V2/data/metadata/documents_seed.csv`.
3. Run `python V2/scripts/dh_v2.py validate-documents`.
4. Create segment JSONL.
5. Run `python V2/scripts/dh_v2.py validate-segments --segments <path>`.
6. Add an evidence table or claims review to a research case.

---

## 3. 新增脚本 / Adding Scripts

新增脚本应优先注册到 `V2/scripts/dh_v2.py` 的 CLI 子命令中。

New scripts should preferably be registered as subcommands in `V2/scripts/dh_v2.py`.

脚本输出应写入 `V2/outputs/`、`V2/cases/` 或 `V2/releases/`，避免散落在项目根目录。

Script outputs should be written to `V2/outputs/`, `V2/cases/`, or `V2/releases/`, not scattered in the project root.

---

## 4. 新增研究案例 / Adding Research Cases

每个研究案例至少包含以下文件。

Each research case should include at least the following files.

```text
case_name/
├── README.md
├── evidence_table.csv
├── kwic_terms.csv
├── claims_review.csv
└── interpretive_note.md
```

研究案例必须把解释和证据绑定起来。没有 evidence quote 的 claim 只能是候选，不能作为结论。

A research case must bind interpretation to evidence. A claim without an evidence quote can only be a candidate, not a conclusion.

---

## 5. 提交前检查 / Pre-commit Checklist

- README 或 V2 README 是否需要同步更新？
- metadata 是否通过验证？
- 新增 sample 是否明确标为 sample？
- 新增 claim 是否有 evidence quote？
- 自动生成结果是否标为 candidate？
- 外部数据库或 authority 是否保留来源与授权说明？

- Should the root README or V2 README be updated?
- Does metadata pass validation?
- Are new samples clearly marked as samples?
- Does every new claim have an evidence quote?
- Are automatically generated outputs marked as candidates?
- Do external databases or authorities preserve source and license notes?
