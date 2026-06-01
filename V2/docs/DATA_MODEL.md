# Data Model：DH V2 数据模型

DH V2 的数据模型服务于文史研究中的证据链，而不是服务于抽象的 NLP benchmark。每一个字段都应回答一个人文学术问题：这条材料从哪里来？它属于哪本文献？它支持什么判断？它是否经过人工复核？它能否回到原文？

## 一、Document

Document 是文献单位。

核心字段：

```csv
document_id,title_original,title_normalized,year_original,year_standard,author_original,author_normalized,translator,reviser,editor,dynasty,genre,knowledge_domain,source_collection,source_volume,source_page_start,source_page_end,ocr_status,correction_status,rights_status,notes
```

用途：

- 保存文献基本信息；
- 支持年代、作者、体裁、知识领域分析；
- 记录 OCR、校勘和授权状态；
- 防止文本脱离来源。

## 二、Segment

Segment 是可回溯的文本段落单位。

核心字段：

```csv
segment_id,document_id,segment_index,text,text_type,chapter_title,page_ref,char_start,char_end,source_file,confidence_level
```

用途：

- 让术语、实体、claim 能回到具体段落；
- 支持 KWIC、相似段落、证据卡片；
- 方便人工复核。

## 三、Entity

Entity 是文本中的人名、地名、机构、书名、官职、单位等对象。

核心字段：

```csv
entity_id,entity_text,entity_type,normalized_form,document_id,segment_id,evidence_quote,char_start,char_end,extraction_method,human_verified
```

实体类型包括：

- person；
- place；
- institution；
- office_title；
- book_title；
- dynasty；
- country；
- astronomical_object；
- measurement_unit。

## 四、Term

Term 是概念史与知识史分析的术语单位。

核心字段：

```csv
term_id,term_text,normalized_form,category,subcategory,variants,first_seen_document,first_seen_year,notes
```

用途：

- 追踪术语变体；
- 连接 KWIC；
- 生成 concept page；
- 服务概念史解释。

## 五、Claim

Claim 是 V2 的关键对象，表示文本中的知识命题候选。

核心字段：

```csv
claim_id,document_id,segment_id,claim_text,knowledge_domain,claim_type,subject,predicate,object,evidence_quote,confidence,extraction_method,human_verified
```

Claim 的意义在于：传统人文学术关心的不是词频本身，而是文本如何提出、解释、转述或限制某一知识判断。

示例：

```text
claim_text: 地與海合為一球
evidence_quote: 地與海本是圓形而合爲一球
confidence: medium
human_verified: false
```

## 六、Relation

Relation 表示实体、术语、文本、claim 之间的关系。

关系类型示例：

- same_as；
- variant_of；
- translated_as；
- authored_by；
- revised_by；
- cites；
- rewrites；
- explains；
- contradicts；
- institutionally_produced_by。

## 七、Authority Crosswalk

Authority crosswalk 用于连接外部权威数据库。

核心字段：

```csv
entity_id,entity_text,entity_type,normalized_form,cbdb_id,chcd_id,bdcc_url,ricci_id,match_status,match_confidence,evidence,note
```

匹配状态：

- unmatched；
- candidate；
- verified；
- rejected；
- ambiguous。

## 八、数据模型的文史意义

这个模型的目的不是把文本变成数据之后抛弃阅读，而是让阅读留下结构化痕迹。一个成熟的人文学术项目，应当同时保存原文、判断、证据、方法和不确定性。