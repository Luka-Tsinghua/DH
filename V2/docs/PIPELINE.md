# V2 真实文本处理流程
# V2 Real-text Processing Pipeline

本文件说明 V2 如何从仓库根目录中的真实 WS 文本进入可复核的数据链条。

This file explains how V2 moves from the root-level real WS texts into a reviewable data chain.

---

## 1. 输入 / Inputs

当前登记的 raw source 见：

Current registered raw sources are listed in:

```text
V2/data/raw/RAW_SOURCE_MANIFEST.csv
```

目前包括：

Currently included:

```text
1674_坤輿圖說_WS.txt
1799_地球圖説_WS.txt
```

这两个文件位于仓库根目录，不应被 V2 脚本覆盖。

These two files are located at the repository root and should not be overwritten by V2 scripts.

---

## 2. 生成完整 segment / Build Full Segments

```bash
python V2/scripts/dh_v2.py validate-raw-sources
python V2/scripts/dh_v2.py build-segments-from-raw
python V2/scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl
```

默认输出：

Default outputs:

```text
V2/data/processed/full_segments.jsonl
V2/outputs/qc/raw_segment_build_report.json
V2/outputs/qc/raw_sources_validation.json
V2/outputs/qc/segments_validation.json
```

生成逻辑：

Generation logic:

1. 读取 `RAW_SOURCE_MANIFEST.csv`。
2. 定位仓库根目录的 WS 文本。
3. 移除 WS 文本中的 tokenization whitespace。
4. 按固定字符长度切分为 segment。
5. 写入 `segment_id`、`document_id`、`segment_index`、`text`、`char_start`、`char_end`、`source_file` 等字段。

1. Read `RAW_SOURCE_MANIFEST.csv`.
2. Locate root-level WS text files.
3. Remove tokenization whitespace in WS text.
4. Split into fixed-length segments.
5. Write fields including `segment_id`, `document_id`, `segment_index`, `text`, `char_start`, `char_end`, and `source_file`.

---

## 3. 生成 KWIC / Generate KWIC

```bash
python V2/scripts/dh_v2.py generate-kwic \
  --segments data/processed/full_segments.jsonl \
  --output outputs/features/full_kwic_terms.csv
```

KWIC 只说明术语出现于某段文本中，不等于解释结论。

KWIC only shows that a term appears in a segment. It is not an interpretive conclusion.

---

## 4. 生成候选 evidence table / Generate Candidate Evidence Table

```bash
python V2/scripts/dh_v2.py generate-evidence-table \
  --kwic outputs/features/full_kwic_terms.csv \
  --output outputs/features/full_evidence_table.csv \
  --limit 200
```

生成的 evidence rows 一律标记为 `candidate`。正式研究必须人工复核。

Generated evidence rows are marked as `candidate`. Formal research requires human review.

---

## 5. 与 case 的关系 / Relation to Cases

`outputs/features/` 中的文件是可再生中间结果。进入正式研究案例时，应将经过人工筛选与复核的条目写入：

Files under `outputs/features/` are reproducible intermediate outputs. For formal research cases, manually selected and reviewed rows should be written to:

```text
V2/cases/<case_name>/evidence_table.csv
V2/cases/<case_name>/kwic_terms.csv
V2/cases/<case_name>/claims_review.csv
V2/cases/<case_name>/interpretive_note.md
```

---

## 6. 注意事项 / Cautions

WS 文本的空格被视为分词或 OCR 后处理痕迹。V2 默认移除这些空格以便生成 KWIC，但正式引文仍应回查 raw source。

Whitespace in WS texts is treated as tokenization or OCR-postprocessing residue. V2 removes it by default for KWIC generation, but formal citation should still check the raw source.

固定长度 segment 适合 pipeline 和检索，但不等于自然章节或文义段落。后续可再增加基于卷、标题、句读或主题的 philological segmentation。

Fixed-length segments are useful for pipeline and retrieval, but they are not equivalent to natural chapters or semantic paragraphs. Later versions may add philological segmentation based on fascicles, titles, punctuation, or topics.
