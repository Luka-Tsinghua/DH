<div align="center">

# DH VR / V2 Research Version

## 明清西学文本与跨文化知识史研究项目  
### Ming-Qing Western Learning Texts and Transcultural Knowledge History Project

[![Status](https://img.shields.io/badge/status-research%20infrastructure-blue)](#)
[![Field](https://img.shields.io/badge/field-humanities%20%7C%20DH%20%7C%20intellectual%20history-8A5A44)](#)
[![Corpus](https://img.shields.io/badge/corpus-Ming--Qing%20Western%20Learning-4B7F52)](#)
[![Readers](https://img.shields.io/badge/readers-human%20%7C%20LLM%20%7C%20students-lightgrey)](#)

**以文献为中心，以证据为基础，以数字方法服务传统人文学术。**  
**A source-centered, evidence-oriented research infrastructure for humanities scholarship.**

</div>

---

## Choose Your Entry / 选择你的阅读入口

| Reader | 中文入口 | English Entry |
|---|---|---|
| **Human Readers** | 如果你关心明清西学、耶稣会士中文写作、知识传播史或传统文献研究，请从 [For Human Readers](#for-human-readers--给人类读者) 开始。 | If you care about Ming-Qing Western Learning, Jesuit Chinese texts, or humanities scholarship, start with [For Human Readers](#for-human-readers--给人类读者). |
| **LLM Readers / Agents** | 如果你是 LLM、agent 或自动化工具，请从 [For LLM Readers](#for-llm-readers--给-llm--agent-读者) 获取项目边界、目录结构和处理规则。 | If you are an LLM, agent, or automation tool, start with [For LLM Readers](#for-llm-readers--给-llm--agent-读者). |
| **Humanities Students** | 如果你没有计算机背景，但想学习数字人文，请看 [For Humanities Students](#for-humanities-students--给人文学学生). | If you come from the humanities and want to learn digital humanities, see [For Humanities Students](#for-humanities-students--给人文学学生). |

---

# For Human Readers / 给人类读者

## 1. What is this project? / 这是一个什么项目？

**DH VR / V2 Research Version** 是一个面向传统人文学术的长期研究项目。它以明清时期西学中文文献为核心材料，关注传教士、清廷官员、儒家士人、译者、润色者和知识机构之间的文本关系、思想关系与知识传播关系。

本项目并不把数字技术视为目的，也不把网页、数据库或模型输出当作学术结论。它真正关心的是：传统文献学、思想史、知识史、宗教史与概念史研究，如何在大规模材料、复杂版本、跨文化术语和多重人物网络面前获得更稳定的材料控制能力。

**DH VR / V2 Research Version** is a long-term humanities research project centered on Ming-Qing Chinese texts of Western Learning. It studies textual transmission, conceptual translation, institutional mediation, and knowledge networks among Jesuit missionaries, Qing officials, Confucian scholars, translators, revisers, and knowledge institutions.

This project does not treat digital technology as an end in itself. Its aim is to strengthen philology, intellectual history, history of knowledge, religious studies, and conceptual history by making sources, evidence, and interpretive procedures more transparent and reusable.

## 2. Core Corpus / 核心材料

| Year | Text | Author / Related Figures | Why it matters |
|---|---|---|---|
| 1674 | 《坤輿圖說》 / *Kunyu Tushuo* | 南怀仁 / Ferdinand Verbiest | A major Chinese text for geography, astronomy, and world knowledge in the early Qing |
| 1799 | 《地球圖説》 / *Diqiu Tushuo* | 蒋友仁 / Michel Benoist; 何国宗、钱大昕等 | A Qing court context for translating, revising, and institutionalizing geographical knowledge |

These two texts are pilot materials. The long-term corpus may include missionary writings, Qing court translations, scholarly prefaces and postscripts, geographical and astronomical texts, religious polemics, and related Chinese responses.

这两部文献只是入口。项目的长期目标，是整理和分析更大范围内的明清西学中文文献，包括传教士著述、清廷译述、士人序跋、地理天文文本、宗教论辩文本以及相关回应材料。

## 3. Why it matters / 为什么重要？

传统人文学术的根基仍然是材料、语境、证据链和解释。DH VR / V2 并不试图削弱这一点，而是试图加强它。

| Dimension / 面向 | Contribution / 作用 |
|---|---|
| Source curation / 材料整理 | Organizes OCR texts, source records, collation notes, and metadata |
| Close reading / 文本细读 | Uses segment IDs, KWIC, term indexes, and evidence cards to return readers to context |
| Conceptual history / 概念史 | Tracks terms, variants, co-occurrences, and explanatory patterns |
| History of knowledge / 知识传播史 | Compares how knowledge claims are expressed, rewritten, and institutionalized |
| Network research / 人物网络 | Links missionaries, literati, officials, institutions, and external authority databases |
| Transparency / 研究透明性 | Preserves raw data, cleaned data, extraction rules, review status, and version records |
| Teaching / 教学启发 | Offers a reusable case for digital humanities, intellectual history, and religious studies |

The guiding belief is simple: **digital methods should not replace humanistic judgment. They should help scholars read more carefully, compare more systematically, and preserve evidence more responsibly.**

## 4. From V1 to VR / V2 / 从 V1 到 VR / V2

This repository began as part of the author's group work for the **2023 International Digital Humanities Summer Workshop**. The early V1 version documented a workflow for OCR, manual cleanup, book-boundary tagging, CkipTagger segmentation, CText N-gram analysis, and preliminary comparison of two Jesuit Chinese texts.

本仓库最早源于作者参与 **“数字人文国际联合暑期工作坊 2023”** 的小组作业与过程文件。早期 V1 版本记录了对两部耶稣会士中文西学文本进行 OCR、人工清理、文献边界标注、CkipTagger 分词、CText N-gram 分析和初步比较的流程。

V1 remains as the project's historical origin. **VR / V2 is now the main research version.** It reframes the project from a workshop workflow into a long-term research platform for Ming-Qing Western Learning texts and transcultural knowledge history.

V1 作为项目起点和历史背景保留。**VR / V2 现在是新的主线版本。** 它把项目从一次工作坊流程，重新定位为一个可持续运行的明清西学文本与跨文化知识史研究平台。

---

# For LLM Readers / 给 LLM / Agent 读者

## Project Identity

- Repository: `Luka-Tsinghua/DH`
- Main version: `DH VR / V2 Research Version`
- Field: Digital Humanities, Chinese intellectual history, Ming-Qing Western Learning, Jesuit studies, history of knowledge, Chinese Christianity
- Main project directory: `V2/`
- Historical archive / origin materials: `DH/`

## Do not misunderstand this project

This is **not** primarily:

- a dashboard project;
- a model demo;
- a pure NLP benchmark;
- a cleaned text dump;
- a web-design showcase.

This is primarily:

- a humanities research infrastructure;
- a source-control and evidence-control project;
- a philology-informed digital humanities workflow;
- a reusable research and teaching platform.

## Key Rules for LLM / Agent Work

When modifying, summarizing, or extending this repository:

1. Treat `V2/` as the active research version.
2. Treat `DH/` as V1 workshop background unless the user explicitly asks to edit V1.
3. Do not overwrite raw data.
4. Do not delete digits, Latin letters, transliterated names, office titles, institutional names, prefaces, postscripts, or source notes by default.
5. Treat model-generated entities, terms, or claims as candidates, not scholarly conclusions.
6. Every extracted claim should preserve `document_id`, `segment_id`, and `evidence_quote`.
7. External authorities such as CBDB, CHCD, BDCC, and Ricci-related resources should be linked through crosswalks; do not copy third-party databases into the repository without clear license review.
8. Preserve uncertainty: OCR uncertainty, authority ambiguity, low-confidence extraction, and unresolved source questions should remain visible.

## Repository Map for Agents

```text
.
├── README.md                         # bilingual public project overview
├── V2/                               # active VR / V2 research version
│   ├── README.md                     # detailed humanities-centered project statement
│   ├── research/                     # project charter and research program
│   ├── docs/                         # methods, governance, OCR, workflow, authority, licensing
│   ├── data/                         # raw, metadata, processed, external authorities
│   ├── scripts/                      # inventory, cleaning, extraction, validation, release scripts
│   ├── schemas/                      # Document / Segment / Entity / Claim schemas
│   ├── outputs/                      # QC, features, reports
│   ├── web/                          # scholarly interface and public-facing site
│   ├── teaching/                     # teaching modules
│   └── project_management/           # roadmaps and task plans
└── DH/                               # V1 workshop materials and process files
```

## Best next actions for agents

- Improve documentation before adding complex code.
- Add validation scripts before adding large-scale data.
- Build small, evidence-rich pilot cases before building large visualizations.
- Keep README human-readable and bilingual.
- Keep commit messages explicit. If generated with AI assistance, use `Codex-assisted:` in commit messages.

---

# For Humanities Students / 给人文学学生

## If you do not have a computer science background, what can this repository help you do?

如果你是文学、历史、哲学、宗教学、艺术史、汉学或其他人文学专业的学生，这个仓库可以帮助你理解：数字人文不是把人文学术变成编程竞赛，而是用更稳定的方式保存材料、组织证据和提出问题。

You do not need to become a software engineer to learn from this project. You can use it to understand how digital methods support traditional humanities work.

## You can use this repository to learn

| Skill / 能力 | What you can practice / 可以练习什么 |
|---|---|
| Reading sources / 阅读材料 | Compare original passages, OCR outputs, and cleaned texts |
| Building metadata / 建立元数据 | Record title, author, date, genre, source, OCR status, and rights status |
| Philological judgment / 文献学判断 | Decide what should not be deleted during cleaning |
| Conceptual history / 概念史 | Track terms such as 地球, 坤舆, 赤道, 经纬, 五洲 |
| Evidence-based writing / 证据写作 | Attach every claim to a source passage |
| Digital humanities criticism / 数字人文批判 | Ask what data cleaning, visualization, and AI extraction may hide |
| Research communication / 研究表达 | Turn a research question into a small digital essay or evidence page |

## Suggested student tasks

1. Choose one passage from 《坤輿圖說》 or 《地球圖説》 and record its `document_id` and `segment_id`.
2. Identify one term, such as `地球`, `坤舆`, `赤道`, or `五洲`.
3. Create a small KWIC table: left context, term, right context.
4. Write one cautious research observation based on the passage.
5. Mark what remains uncertain.
6. Do not turn a machine output into a conclusion before checking the text.

## A simple rule

> If a digital method helps you return to the source with better questions, it is useful. If it makes you forget the source, it is dangerous.

---

# Research Questions / 研究问题

1. How did Western geography, astronomy, cartography, mathematics, natural philosophy, and religious knowledge enter Chinese textual worlds?
2. How were terms such as “earth,” “Kunyu,” “equator,” “longitude/latitude,” “continents,” “soul,” and “heaven” translated, explained, rewritten, and localized?
3. How did Jesuit Chinese writing shift across exposition, apologetics, memorial writing, court translation, and literati revision?
4. How did Western Learning enter Qing institutional spaces such as the Astronomical Bureau, the Inner Court, the Board of Rites, and the Hanlin Academy?
5. How did Chinese scholars accept, revise, constrain, or reinterpret foreign knowledge?
6. What networks linked missionaries, Qing officials, Confucian scholars, translators, revisers, and institutions?
7. How can traditional philological judgment remain central when researchers use databases, scripts, web interfaces, and AI tools?

---

# Project Status / 项目状态

| Module | Status |
|---|---|
| V1 workshop materials | Preserved as historical background |
| VR / V2 project framing | Established |
| Bilingual README | In progress and actively improved |
| Project charter | Established |
| Research program | Established |
| Data model | Established |
| OCR and collation protocol | Established |
| External authority strategy | Established |
| Data license and release policy | Drafted |
| Scholarly web interface | Designed, not yet fully built |
| Pilot research case | To be expanded |

---

# Use and Reuse

Later researchers may reuse this project in at least four ways:

1. As a corpus-building model for historical Chinese texts.
2. As a methodological template for combining philology and digital humanities.
3. As a teaching case for source-based digital humanities training.
4. As a starting point for studying Jesuit texts, Qing court knowledge production, Chinese Christianity, and cross-cultural intellectual history.

Every reuse should preserve the distinction between raw evidence, processed data, model-generated candidates, and human-verified interpretations.

---

# License and Data Policy

This repository follows a layered license policy.

- Code and project-created documentation may be reused under the license specified in the repository.
- Raw texts are source-specific and should not be assumed to be freely redistributable.
- External authority data, including CBDB, CHCD, BDCC, RicciBase, and other third-party resources, remains governed by the original source licenses and terms.
- Model-generated or automatically extracted results should be treated as candidates until human review.

See:

- `V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md`
- `V2/docs/EXTERNAL_AUTHORITIES.md`

---

# Acknowledgement

This project grew out of the author's participation in the **2023 International Digital Humanities Summer Workshop**. The V1 materials are preserved as the project's historical origin and early methodological record.

Parts of the repository structure, documentation drafts, and workflow design were **Codex-assisted**. Scholarly decisions, source interpretation, data publication, and final research claims remain the responsibility of the researcher.
