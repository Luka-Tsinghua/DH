# 《坤輿圖說》与《地球圖説》比较研究案例
# Pilot Case: Comparing *Kunyu Tushuo* and *Diqiu Tushuo*

## 1. 案例目标 / Case Goal

本案例不是一次性展示，而是 V2 项目的第一个可扩展研究单元。它用于测试从原始文本、metadata、分段、术语抽取、KWIC、知识命题、人工复核到研究解释的完整链条。

This case is not a one-off demonstration. It is the first expandable research unit of the V2 project. It tests the full chain from raw text, metadata, segmentation, term extraction, KWIC, knowledge claims, human review, and scholarly interpretation.

## 2. 核心问题 / Core Questions

1. 《坤輿圖說》和《地球圖説》如何分别表达地球、坤舆、经纬、赤道、五洲等地理概念？
2. 两部文本在知识解释方式、术语使用、制度语境和读者预设上有什么差异？
3. 哪些表达可能体现传教士知识、清廷制度、士人润色和中文概念资源之间的互动？

1. How do *Kunyu Tushuo* and *Diqiu Tushuo* express geographical concepts such as earth, Kunyu, longitude/latitude, equator, and continents?
2. How do the two texts differ in explanatory strategy, terminology, institutional context, and imagined readership?
3. Which expressions may reveal interactions among missionary knowledge, Qing institutions, literati revision, and Chinese conceptual resources?

## 3. 输入材料 / Inputs

| 文件 / File | 用途 / Purpose |
|---|---|
| `V2/data/metadata/documents_seed.csv` | 文献级 metadata 起点 / starting document-level metadata |
| `V2/config/domain_lexicon_seed.csv` | 术语分析起点 / seed lexicon for term analysis |
| `V2/data/raw/` | 原始文本或 OCR 文件，需逐步补充 / raw texts or OCR files to be added |
| `V2/data/processed/` | 清洗与分段结果 / cleaned and segmented outputs |

## 4. 输出材料 / Outputs

| 文件 / File | 用途 / Purpose |
|---|---|
| `evidence_table.csv` | 每条观察对应原文证据 / observations linked to textual evidence |
| `kwic_terms.csv` | 核心术语 KWIC 表 / KWIC table for core terms |
| `claims_review.csv` | 知识命题候选与人工复核 / candidate claims and human review |
| `interpretive_note.md` | 研究解释草稿 / interpretive note |

## 5. 可扩展原则 / Extension Principles

新增文献时，不应复制粘贴本案例后随意改名，而应保持相同结构：metadata、raw source、processed segments、features、claims、review、interpretation。

When adding a new text, do not simply duplicate this case and rename files casually. Preserve the same structure: metadata, raw source, processed segments, features, claims, review, and interpretation.

每一个研究观察都必须能够回到 `document_id`、`segment_id` 和 `evidence_quote`。

Every research observation must be traceable back to `document_id`, `segment_id`, and `evidence_quote`.
