<div align="center">

# DH VR / V2 Research Version

## 明清西学文本与跨文化知识史研究项目
## Ming-Qing Western Learning Texts and Transcultural Knowledge History Project

**以文献为中心，以证据为基础，以数字方法服务传统人文学术。**

</div>

---

## 项目定位

本仓库是一个面向中国思想史、明清西学、耶稣会研究、知识史和数字人文方法的长期研究项目。它最初源于 2023 年数字人文工作坊的实验材料，但当前 `V2/` 已经被重构为真实、可复现、可扩展、可维护的研究基础设施。

V2 不把网页、模型输出或可视化图表当作学术结论。它的目标是帮助研究者更稳定地保存 raw source、组织 metadata、生成可复核 segment、建立术语索引、保存 evidence quote、区分 candidate claim 与 reviewed claim，并最终形成可发布的小型数字论文或语料库版本。

---

## 当前真实材料

当前 V2 主线已经登记并使用仓库根目录中的两部真实 WS 文本：

```text
1674_坤輿圖說_WS.txt
1799_地球圖説_WS.txt
```

这两部文本不是 synthetic sample。它们是当前 pipeline 的真实 raw source。`V2/data/processed/sample_segments.jsonl` 仅保留为 smoke test，不进入正式研究解释。

---

## V2 能做什么

V2 已经具备以下能力：

- 验证 document metadata。
- 验证 raw source manifest。
- 从登记的真实 WS 文本生成 full segment JSONL。
- 验证 segment JSONL。
- 导出领域词表。
- 生成 KWIC。
- 生成 candidate evidence table。
- 根据 case config 生成 case-level KWIC、candidate evidence、candidate claims 和 build report。
- 生成 release manifest。
- 通过 Makefile 一键运行 pipeline。
- 通过 GitHub Actions workflow 自动检查 V2 pipeline。

---

## 快速开始

进入 `V2/` 后运行：

```bash
make pipeline
```

这会执行从 raw source validation 到 case build 与 release manifest 的最低闭环。

也可以从仓库根目录运行测试：

```bash
pytest V2/tests
```

---

## 核心目录

```text
.
├── README.md
├── .github/workflows/v2-ci.yml
├── V2/
│   ├── README.md
│   ├── Makefile
│   ├── pyproject.toml
│   ├── config/
│   ├── data/
│   ├── schemas/
│   ├── scripts/
│   ├── tests/
│   ├── cases/
│   ├── docs/
│   ├── outputs/
│   └── releases/
└── DH/
```

`DH/` 保存 V1 工作坊材料和历史流程。`V2/` 是当前活跃研究版本。

---

## 当前核心 case

当前核心 case 位于：

```text
V2/cases/kunyu_diqiu_comparison/
```

该 case 比较《坤輿圖說》与《地球圖説》的术语、地理知识表达、图说体裁和制度化翻译语境。它已经包含 curated case files，并新增 `case_config.json` 与 `generated/` 分层。脚本生成的候选结果先进入 `generated/`，人工复核后的结果再进入 case 根目录下的正式 CSV 与 interpretive note。

---

## 研究问题

本项目当前关注以下问题：

1. 西方地理、天文、制图、数学、自然哲学和宗教知识如何进入中文文本世界？
2. “地球”“坤舆”“赤道”“经纬”“五洲”“灵魂”“天堂”等概念如何被翻译、解释、改写和本土化？
3. 传教士中文写作如何在讲解、辩护、奏呈、奉旨译述、士人润色等不同文体之间转换？
4. 西学知识如何进入清廷制度空间？
5. 中国士人如何接受、改写、限制或重新解释这些外来知识？
6. 当研究者使用数据库、脚本、网页和 AI 工具时，传统文献学判断如何保持主导地位？

---

## 给 LLM / Agent 的规则

自动化工具修改本仓库时，应遵守以下规则：

- 将 `V2/` 视为当前活跃版本。
- 不覆盖 raw source。
- 不把 generated candidate outputs 写成最终学术结论。
- 每条 claim 必须保留 `document_id`、`segment_id`、`evidence_quote` 和 `review_status`。
- 保留不确定性。
- 新增 case 时必须使用 `case_config.json`、`generated/` 和 curated case files 的分层。
- 修改 pipeline 后必须同步更新 README、Makefile、tests 和 docs。

---

## 授权与数据政策

本仓库采用分层授权原则。项目自有代码和文档可按仓库授权复用；raw texts 具有来源差异，不应默认视为可自由再发布；外部 authority 数据应遵守原始数据库或平台授权；自动抽取和模型生成结果在人工复核前只应视为 candidate。

详见：

```text
V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md
```

---

## 当前状态

V2 当前已经达到真实、可复现、可扩展、可维护的最低项目形态。它仍不是完成的学术论文。下一阶段的重点是人工复核 generated claims、补充版本与页码信息、完善校勘说明，并将第一个 case 打磨为可发布的小型数字论文。

---

## 致谢

本项目源于作者参与 2023 International Digital Humanities Summer Workshop 的早期小组作业。V1 材料作为项目历史起点和方法探索记录保留。仓库结构、部分文档草案和工作流设计曾由 Codex / ChatGPT 辅助生成。学术判断、材料解释、数据发布和最终研究结论仍由研究者负责。
