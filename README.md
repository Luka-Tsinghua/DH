<div align="center">

# DH VR / V2 Research Version

## 明清西学文本与跨文化知识史研究项目
## Ming-Qing Western Learning Texts and Transcultural Knowledge History Project

**以文献为中心，以证据为基础，以数字方法服务传统人文学术。**

</div>

---

## 1. 项目一句话说明

本仓库是一个面向中国思想史、明清西学、耶稣会研究、知识史与数字人文方法的长期研究项目。它最初来自 2023 年数字人文工作坊实验材料，但当前主线 `V2/` 已经重构为可复现、可扩展、可维护的人文学术研究基础设施。

This repository is a long-term humanities research project for Chinese intellectual history, Ming-Qing Western Learning, Jesuit studies, history of knowledge, and digital humanities. It began from 2023 workshop materials, but the active `V2/` line is now maintained as reproducible research infrastructure.

---

## 2. 快速入口 / Quick Links

| 入口 | 用途 |
|---|---|
| `V2/README.md` | V2 主说明与运行入口 |
| `V2/docs/INDEX.md` | V2 文档索引 |
| `V2/docs/PIPELINE.md` | 可复现 pipeline |
| `V2/docs/METHOD.md` | 方法原则 |
| `V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md` | 数据与发布政策 |
| `V2/cases/kunyu_diqiu_comparison/` | 当前核心研究案例 |
| `CONTRIBUTING.md` | 仓库级贡献规范 |
| `V2/CONTRIBUTING.md` | V2 贡献规范 |

---

## 3. 当前状态 / Current Status

| 维度 | 状态 |
|---|---|
| 当前活跃版本 | `V2/` |
| 历史材料 | `DH/` |
| 真实 raw source | 已登记 |
| 可复现 pipeline | 已建立 |
| case builder | 已建立 |
| 测试 | 已建立 |
| CI | 手动触发，待稳定后恢复自动触发 |
| 学术解释 | candidate 阶段，需人工复核 |

V2 已经不是一次性工作坊展示内容。它现在是一个可继续扩展的研究仓库雏形。它仍不是完成的学术论文。下一阶段重点是人工复核、校勘说明、版本页码信息和第一个可发布 digital essay。

---

## 4. 当前真实材料 / Real Sources

当前 V2 主线登记并使用仓库根目录中的两部 WS 文本：

```text
1674_坤輿圖說_WS.txt
1799_地球圖説_WS.txt
```

这两部文件是当前 pipeline 的真实 raw source。`V2/data/processed/sample_segments.jsonl` 只用于 smoke test，不进入正式研究解释。

---

## 5. 如何运行 / How to Run

进入 `V2/` 后运行：

```bash
make pipeline
```

完整检查：

```bash
make all
```

`make pipeline` 会执行 raw source validation、segment build、KWIC、candidate evidence、case-level candidate outputs 和 release manifest。`make all` 会在此基础上运行 smoke tests。

---

## 6. 仓库结构 / Repository Structure

```text
.
├── README.md                         # 仓库入口说明
├── CONTRIBUTING.md                   # 仓库级贡献规范
├── .github/workflows/v2-ci.yml       # V2 检查 workflow，当前为手动触发
├── 1674_坤輿圖說_WS.txt              # V2 raw source
├── 1799_地球圖説_WS.txt              # V2 raw source
├── V2/                               # 当前活跃研究版本
│   ├── README.md                     # V2 主说明
│   ├── Makefile                      # pipeline 入口
│   ├── pyproject.toml                # Python 项目配置
│   ├── config/                       # 项目配置与词表
│   ├── data/                         # raw manifest、metadata、processed data
│   ├── schemas/                      # 数据结构 schema
│   ├── scripts/                      # CLI 与 case builder
│   ├── tests/                        # smoke tests
│   ├── cases/                        # 研究案例
│   ├── docs/                         # 方法、维护、政策、路线图
│   ├── outputs/                      # 可再生成输出
│   └── releases/                     # release manifest 与发布材料
└── DH/                               # V1 工作坊历史材料
```

`DH/` 保存早期工作坊材料和方法探索记录。`V2/` 是当前活跃版本。不要把 `DH/` 当作当前主线来修改，除非任务明确要求处理 V1 历史材料。

---

## 7. 研究对象模型 / Research Objects

V2 的核心对象不是网页，而是可复核的研究对象：

```text
RawSource → Document → Segment → Term → KWIC → Evidence → Claim → Case → Release
```

这一模型的基本原则是：解释不能脱离证据，证据不能脱离文本，文本不能脱离来源。

---

## 8. 当前核心案例 / Current Case

当前核心 case 位于：

```text
V2/cases/kunyu_diqiu_comparison/
```

该 case 比较《坤輿圖說》与《地球圖説》的术语、地理知识表达、图说体裁和制度化翻译语境。`case_config.json` 定义 focus terms、segment source 和输出路径。脚本生成的候选结果进入 `generated/`；人工复核后的结果进入 case 根目录下的 curated CSV 和 interpretive note。

---

## 9. 给 LLM / Agent 的规则

- 将 `V2/` 视为当前活跃版本。
- 将 `DH/` 视为 V1 历史材料。
- 不覆盖 raw source。
- 不把 generated candidate outputs 写成最终学术结论。
- 每条 claim 必须保留 `document_id`、`segment_id`、`evidence_quote` 和 `review_status`。
- 新增 case 时必须保留 `case_config.json`、`generated/` 与 curated case files 的分层。
- 修改 pipeline 后必须同步更新 README、Makefile、tests 和 docs。

---

## 10. 授权与数据政策 / License and Data Policy

本仓库采用分层授权原则。项目自有代码和文档、raw texts、generated candidate outputs、curated scholarly outputs、external authority data 不应混用同一种授权逻辑。

详见：

```text
V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md
```

---

## 11. 致谢 / Acknowledgement

本项目源于作者参与 2023 International Digital Humanities Summer Workshop 的早期小组作业。V1 材料作为项目历史起点和方法探索记录保留。仓库结构、部分文档草案和工作流设计曾由 Codex / ChatGPT 辅助生成。学术判断、材料解释、数据发布和最终研究结论仍由研究者负责。
