# Data License and Release Policy

## 一、项目内部材料分级

V2 将材料分为五级：

### Level 0：代码与项目文档

包括：

- scripts；
- schema；
- project docs；
- task docs；
- metadata templates。

建议授权：

- MIT 或 Apache-2.0。

### Level 1：项目自建 metadata

包括：

- documents.csv；
- terms.csv；
- manually verified authority crosswalk；
- cleaning logs；
- QC reports。

建议授权：

- CC BY 4.0 或 CC BY-NC 4.0；
- 若混入 CBDB 派生字段，则必须兼容 CC BY-NC-SA 4.0。

### Level 2：原始 OCR 文本

包括：

- raw OCR；
- 影印本转写文本；
- 从丛书、数据库、扫描件整理出的文本。

授权策略：

- 逐项记录来源；
- 不默认公开；
- 公开前确认原书版权、影印本来源和数据库授权；
- 对公版古籍文本也要注明数字化来源。

### Level 3：外部 authority 派生数据

包括：

- CBDB 派生字段；
- CHCD 对应项；
- BDCC 对应项；
- RicciBase 对应项。

授权策略：

- 只发布 external_id 与 minimal crosswalk；
- 不再发布第三方数据库原文或完整记录；
- 遵守各数据库授权；
- 授权不明时只保存内部研究记录。

### Level 4：研究报告与论文草稿

包括：

- pilot report；
- corpus report；
- article drafts；
- interpretive essays。

建议授权：

- Copyright retained by author；
- 公开版本可使用 CC BY-NC-ND 4.0。

## 二、绝对禁止

- 不得把所有数据一律标记为 MIT。
- 不得把 CBDB 数据打包进本仓库后标记为 MIT。
- 不得批量再发布 BDCC 全文。
- 不得在未确认授权时公开 CHCD 原始数据。
- 不得去除数据来源说明。

## 三、推荐发布方式

每次 release 分为：

```text
code-release
metadata-release
sample-data-release
research-report-release
```

不要把所有内容混成一个 release。

## 四、仓库 LICENSE 建议

本仓库可采用“双层授权”：

```text
Code and documentation: MIT
Project-created metadata: CC BY 4.0 unless otherwise noted
Third-party-derived data: governed by original source licenses
Raw texts: source-specific; not automatically redistributable
```

## 五、引用格式

每个 release 应包含：

- version；
- release date；
- commit hash；
- data scope；
- source list；
- license note；
- citation suggestion。
