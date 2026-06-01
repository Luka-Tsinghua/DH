# V2 数据目录说明
# V2 Data Directory Guide

本目录用于保存 V2 的原始材料、metadata、处理后数据和外部 authority 对照表。

This directory stores V2 raw materials, metadata, processed data, and external authority crosswalks.

---

## 1. 目录结构 / Directory Structure

```text
data/
├── raw/                       # 原始材料，不覆盖 / raw materials, never overwritten
├── metadata/                  # 文献级 metadata / document-level metadata
├── processed/                 # 分段、清洗、样例数据 / segments, cleaned data, sample data
└── external_authorities/      # 外部 authority 对照表 / external authority crosswalks
```

---

## 2. raw / Raw Data

`raw/` 保存原始 OCR、转写文件、影印来源说明或其他不可随意覆盖的材料。

`raw/` stores raw OCR, transcriptions, source notes, or other materials that should not be overwritten casually.

正式项目中，原始材料应带有来源、版本、页码或权利状态说明。

In formal research, raw materials should include source, edition, page, or rights-status notes.

---

## 3. metadata / Metadata

`metadata/documents_seed.csv` 是文献级 metadata 的起点。

`metadata/documents_seed.csv` is the starting point for document-level metadata.

新增文献后，应运行：

After adding a new text, run:

```bash
python V2/scripts/dh_v2.py validate-documents
```

---

## 4. processed / Processed Data

`processed/sample_segments.jsonl` 只是 pipeline 测试样例，不是正式古籍原文。

`processed/sample_segments.jsonl` is only a pipeline test sample, not verified historical source text.

正式 segment 文件应使用 JSONL，每行至少包含：

Formal segment files should use JSONL, with each row containing at least:

```json
{"segment_id":"...","document_id":"...","segment_index":0,"text":"..."}
```

---

## 5. external_authorities / External Authorities

`external_authorities/authority_crosswalk_seed.csv` 用于记录本地人名、文献名、术语和外部数据库之间的候选或已验证对照。

`external_authorities/authority_crosswalk_seed.csv` records candidate or verified links between local persons, texts, terms, and external databases.

外部 authority 数据必须保留来源和授权说明。

External authority data must preserve source and license notes.
