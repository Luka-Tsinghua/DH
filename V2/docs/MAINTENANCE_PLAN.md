# V2 可维护性计划
# V2 Maintenance Plan

## 1. 目标 / Goal

V2 不应成为一次性展示文件夹，而应成为可持续扩展、可复核、可教学、可发布的人文学术研究系统。

V2 should not become a one-off presentation folder. It should become a sustainable, extensible, reviewable, teachable, and publishable humanities research system.

## 2. 维护对象 / Maintained Objects

| 对象 / Object | 位置 / Location | 维护原则 / Maintenance Principle |
|---|---|---|
| 项目配置 / project configuration | `V2/config/project.yml` | 新增目录、数据层或核心对象时同步更新。 / Update whenever directories, data layers, or core objects change. |
| 领域词表 / domain lexicon | `V2/config/domain_lexicon_seed.csv` | 新增术语必须有 normalized form、category 和 note。 / New terms require normalized form, category, and note. |
| 文献 metadata / document metadata | `V2/data/metadata/documents_seed.csv` | 新增文献必须通过 metadata validation。 / New documents must pass metadata validation. |
| 数据模型 / data schemas | `V2/schemas/` | schema 变化必须保留向后兼容说明。 / Schema changes must include backward-compatibility notes. |
| 研究案例 / research cases | `V2/cases/` | 每个案例必须保留 evidence table 和 interpretive note。 / Every case must keep an evidence table and interpretive note. |
| 脚本入口 / script entry point | `V2/scripts/dh_v2.py` | 新增脚本优先注册为 CLI 子命令。 / New scripts should be registered as CLI subcommands first. |
| 质检报告 / QC reports | `V2/outputs/qc/` | 每次 release 前必须重新生成。 / Regenerate before every release. |

## 3. 推荐工作流 / Recommended Workflow

```bash
python V2/scripts/dh_v2.py validate-documents
python V2/scripts/dh_v2.py inventory --path data
python V2/scripts/dh_v2.py export-lexicon
```

上述命令不是最终研究结果，而是项目是否仍然可维护的最低检查。

These commands are not final research results. They are the minimum checks for whether the project remains maintainable.

## 4. 新增文献流程 / Adding a New Text

1. 将原始材料放入 `V2/data/raw/`，不要覆盖旧文件。
2. 在 `V2/data/metadata/documents_seed.csv` 增加文献记录。
3. 运行 `validate-documents`。
4. 建立分段文件，并确保每一段都有 `document_id` 和 `segment_id`。
5. 按需要扩展词表。
6. 在 `V2/cases/` 中新建研究案例，保留 evidence table。
7. 写出 interpretive note，并标明不确定性。

1. Place raw materials in `V2/data/raw/` without overwriting old files.
2. Add a document record to `V2/data/metadata/documents_seed.csv`.
3. Run `validate-documents`.
4. Create segmented files with `document_id` and `segment_id` for every segment.
5. Extend the lexicon when needed.
6. Create a research case under `V2/cases/` and preserve the evidence table.
7. Write an interpretive note and mark uncertainty.

## 5. 新增研究案例流程 / Adding a New Research Case

每个研究案例至少应包含：

Each research case should contain at least:

```text
case_name/
├── README.md
├── evidence_table.csv
├── kwic_terms.csv
├── claims_review.csv
└── interpretive_note.md
```

`README.md` 说明问题意识、输入材料、输出材料和扩展方式。

`README.md` explains research questions, inputs, outputs, and extension principles.

`evidence_table.csv` 负责把每条观察绑定到文本证据。

`evidence_table.csv` binds every observation to textual evidence.

`claims_review.csv` 负责区分模型候选、脚本候选和人工接受的结论。

`claims_review.csv` separates model candidates, script candidates, and human-accepted claims.

## 6. Release 检查 / Release Checklist

- README 是否仍然中英并列、对人类和 LLM 都可读？
- metadata 是否通过验证？
- raw data 是否没有被覆盖？
- 每个 claim 是否有 evidence quote？
- 自动生成结果是否标为 candidate？
- 外部 authority 数据是否保留来源和授权说明？
- 研究案例是否有 interpretive note？

- Is the README still bilingual and readable for both humans and LLMs?
- Does metadata pass validation?
- Has raw data remained unoverwritten?
- Does every claim have an evidence quote?
- Are automatically generated outputs marked as candidates?
- Do external authority records preserve source and license information?
- Does each research case include an interpretive note?
