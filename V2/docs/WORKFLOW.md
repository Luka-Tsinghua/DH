# Workflow：DH V2 标准工作流

DH V2 的工作流服务于文史研究中的材料控制、证据组织和解释生成。它不是单纯的数据处理流水线，而是一套从原始材料到可复查研究判断的过程记录。

## 一、总原则

1. 原始材料不覆盖。
2. 每一步处理都必须留下输出文件。
3. 每个抽取结果都必须能回到文献、段落和证据。
4. 自动处理结果必须经过人工复核后才能进入研究结论。
5. 数据、方法、授权和版本必须同时记录。

## 二、阶段 1：材料盘点

目标：确认仓库中到底有哪些材料。

运行：

```bash
python V2/scripts/v2_inventory.py --root . --output V2/outputs/qc/inventory.csv
```

输出：

- `V2/outputs/qc/inventory.csv`

检查内容：

- 文件路径；
- 文件类型；
- 文件大小；
- hash；
- 是否为空；
- 是否为 V1 遗留文件；
- 是否为 V2 项目文件；
- 是否可能属于 raw data、processed data、script、documentation。

## 三、阶段 2：metadata 建立与校验

目标：为每本文献建立基本身份。

核心文件：

```text
V2/data/metadata/documents.csv
```

运行：

```bash
python V2/scripts/v2_validate_metadata.py \
  --documents V2/data/metadata/documents.csv \
  --report V2/outputs/qc/metadata_validation_report.csv
```

检查内容：

- document_id 是否唯一；
- 题名是否完整；
- 年代是否可解析；
- 作者、译者、润色者是否区分；
- OCR 状态是否明确；
- 校勘状态是否明确；
- 权利状态是否明确。

## 四、阶段 3：分层清洗

目标：在不破坏原始材料的情况下，生成不同用途的文本层。

运行：

```bash
python V2/scripts/v2_clean_corpus.py \
  --input V2/data/raw \
  --output V2/data/processed \
  --report V2/outputs/qc/cleaning_qc_report.csv
```

输出层级：

```text
raw_normalized.txt      基础规范化，保留原始信息
reading_clean.txt       供阅读和校勘使用
analysis_clean.txt      供统计和抽取使用
segments.jsonl          可回溯段落单位
```

原则：

- 不删除数字；
- 不删除拉丁字母；
- 不删除音译词；
- 不删除官职和机构名；
- 不随意删除序跋、题名、卷次和署名信息。

## 五、阶段 4：术语、实体、度量衡和 KWIC 抽取

运行：

```bash
python V2/scripts/v2_extract_features.py \
  --segments V2/data/processed \
  --lexicon V2/config/domain_lexicon_seed.csv \
  --output V2/outputs/features
```

输出：

- `ngram_frequency.csv`
- `domain_term_hits.csv`
- `kwic_core_terms.csv`
- `entities_rule_based.csv`
- `measurements.csv`

这些输出是研究线索，不是最终结论。

## 六、阶段 5：知识命题候选抽取

目标：从“词语出现”推进到“文本提出了什么知识判断”。

方法：

- 规则抽取；
- 人工标注；
- LLM 候选抽取；
- 人工复核。

每条 claim 必须包含：

- `document_id`
- `segment_id`
- `claim_text`
- `evidence_quote`
- `confidence`
- `human_verified`

## 七、阶段 6：外部 authority crosswalk

目标：把文本中的人物、机构和地点与外部权威数据库连接。

优先级：

- 中国士人、官员、儒者：CBDB；
- 传教士、教会机构、空间网络：CHCD；
- 传教士与中国基督徒传记：BDCC；
- 传教士姓名、著述、机构补充：Ricci 相关资源。

原则：

- 只保存 crosswalk；
- 不直接复制外部数据库；
- 授权不清时不公开再发布；
- match_status 必须区分 candidate、verified、rejected、ambiguous。

## 八、阶段 7：研究报告与学术界面

研究报告应包含：

- 研究问题；
- 材料范围；
- 原文证据；
- 方法说明；
- 抽取结果；
- 人工复核状态；
- 解释；
- 不确定性；
- 可复现命令。

网页界面应服务于上述结构，而不是替代论文论证。

## 九、阶段 8：release

每次 release 应包含：

- release version；
- commit hash；
- 文件清单；
- 数据范围；
- 授权说明；
- 未完成事项；
- 引用建议。

运行：

```bash
python V2/scripts/v2_generate_release_manifest.py \
  --root . \
  --output V2/releases/manifest_v2.json
```

## 十、工作流的学术意义

这个 workflow 的目的不是把人文学术简化为流水线，而是让每一次材料处理、每一次判断、每一次解释都可以被复查、被教学、被继承和被批判。