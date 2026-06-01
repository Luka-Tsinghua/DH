# Governance：项目治理规则

## 一、角色

### Project Lead

负责：

- 研究方向；
- 数据发布；
- 授权判断；
- 最终解释；
- release 审批。

### Data Curator

负责：

- 文献来源记录；
- OCR 文件管理；
- metadata 校验；
- raw data 不被覆盖。

### Philology Reviewer

负责：

- 文本校勘；
- 术语解释；
- 版本判断；
- 文献学问题标注。

### DH Engineer

负责：

- pipeline；
- scripts；
- QC；
- embeddings；
- reproducibility。

### External Authority Reviewer

负责：

- CBDB / CHCD / BDCC / RicciBase 等匹配；
- authority crosswalk；
- 授权边界控制。

## 二、分支规则

推荐：

```text
main
v1-original-archive-2026
v2-data-cleaning-extraction-2026
feature/*
release/v2.x
```

## 三、文件保护规则

禁止直接覆盖：

- `V2/data/raw/`
- `V2/releases/`
- 已发布的 `V2/outputs/reports/`

需要变更时，新增版本文件，而不是覆盖旧文件。

## 四、人工校验规则

以下内容必须人工校验：

- 人名消歧；
- 地名归一；
- 传教士中文名 / 西文名匹配；
- 知识命题；
- 文献间引用或改写关系；
- 外部 authority 匹配；
- OCR 疑难字。

## 五、Issue 标签

建议标签：

- `data:raw`
- `data:metadata`
- `data:cleaning`
- `authority:cbdb`
- `authority:chcd`
- `authority:bdcc`
- `philology`
- `extraction`
- `license`
- `research-question`
- `needs-human-review`
- `blocked`
