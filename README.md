<p align="center">
  <img src=".github/assets/dh-banner.svg" width="1200" alt="DH V2 — 文献、证据与知识史">
</p>

# DH · 明清西学文本与跨文化知识史

**Ming-Qing Western Learning Texts & Transcultural Knowledge History**

以文献为中心，以证据为基础，以数字方法服务人文学术。DH 为明清西学、耶稣会研究与知识史研究提供一套轻量的文本处理与证据整理工具，让来源、文本片段和解释之间的关系可以追溯、复核与重现。

A lightweight research toolkit for organizing historical texts, tracing textual evidence, and keeping interpretation open to review.

**Python ≥ 3.10 · 标准库运行 · 当前研究版本 V2**

[快速开始](#快速开始) · [工作流](#研究工作流) · [文档](V2/docs/INDEX.md) · [贡献](CONTRIBUTING.md) · [引用与授权](#引用与授权)

---

## 从文献到证据

- **来源可追溯** — 登记文献元数据与原始文本，校验来源文件并记录 SHA-256。
- **语境可检索** — 按固定字符长度生成文本片段，用词表提取 KWIC（关键词上下文）。
- **结果可复核** — 生成证据与论断候选表，保留文献标识、片段标识、原文引句和复核状态。
- **流程可重现** — 通过 Python CLI 运行处理链，生成质量报告与文件清单。

## 研究工作流

1. **登记与校验**：读取原始文本清单、文献元数据与领域词表。
2. **分段与检索**：规范化 WS 文本空白，按字符分段，提取关键词上下文。
3. **整理候选证据**：生成证据表、研究配置对应的 KWIC 与论断候选。
4. **人工复核与解释**：回查原始材料、校勘版本信息，再形成研究判断。

自动生成结果标记为 `candidate`。固定长度分段不是自然章节；规范化文本中的字符位置也不等同于原书页码。证据进入正式解释前仍需人工核对。详见[处理流程](V2/docs/PIPELINE.md)与[复核规则](V2/docs/REVIEW.md)。

## 快速开始

准备 Python 3.10 或更新版本与 Git。在终端运行：

```bash
git clone https://github.com/Luka-Tsinghua/DH.git
cd DH
python V2/scripts/dh_v2.py pipeline
```

处理链使用 Python 标准库，不需要 API 密钥。它读取仓库已登记的原始文本，生成分段、KWIC、证据候选、研究配置对应的候选表和文件清单。

主要输出位于：

- `V2/data/processed/`：生成的完整文本分段。
- `V2/outputs/`：质量报告与特征表。
- 各研究目录的 `generated/`：按配置生成的候选结果。
- `V2/releases/manifest.json`：文件路径、大小与 SHA-256 清单。

这些输出可由脚本重建，与人工整理的研究文件分开保存。原始文本保持不变。

开发安装、单步命令及测试见 [V2 使用指南](V2/README.md)。

## 文档导航

| 阅读入口 | 内容 |
| :--- | :--- |
| [V2 使用指南](V2/README.md) | 安装、命令、输出与测试 |
| [文档索引](V2/docs/INDEX.md) | 按研究与维护任务查找文档 |
| [处理流程](V2/docs/PIPELINE.md) | 原始文本到候选证据的处理规则 |
| [数据模型](V2/docs/DATA_MODEL.md) | 文献、片段、证据与论断的字段关系 |
| [方法原则](V2/docs/METHOD.md) · [复核规则](V2/docs/REVIEW.md) | 人文学术判断与机器候选的边界 |
| [校勘规范](V2/docs/OCR_AND_COLLATION_PROTOCOL.md) | OCR、版本信息与文本核对 |
| [贡献指南](CONTRIBUTING.md) | 开发与研究贡献的入口 |
| [路线图](V2/docs/ROADMAP.md) | 后续研究与工程方向 |

## 仓库地图

- **[V2/](V2/)** — 当前活跃版本：CLI、配置、数据模型、测试与研究文档。
- **仓库根目录** — 已登记的 WS 原始文本与早期工作坊文件；原始文本不由处理脚本覆盖。
- **[V1 历史分支](https://github.com/Luka-Tsinghua/DH/tree/v1-original-archive-2026)** — 早期工作坊版本的保留记录。

目前实现集中在本地文本处理和候选证据整理。外部权威库关联与学术界面设计见[文档索引](V2/docs/INDEX.md)，其中的规划不代表已经实现的功能。

## 引用与授权

引用时请注明所用版本或提交，并区分工具、数据模型与人工复核后的研究成果。作者与版本元数据见 [CITATION.cff](CITATION.cff)。

仓库尚无明确的代码许可证。代码、原始文本、候选结果、人工整理成果及第三方数据的授权范围需分别处理，参见[分层数据与发布政策](V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md)。

## 项目缘起

项目源于作者参与 2023 International Digital Humanities Summer Workshop 的早期小组工作，现以 V2 维护文本处理与证据组织流程。早期材料保留为方法探索记录；学术判断、材料解释与研究结论由研究者负责。
