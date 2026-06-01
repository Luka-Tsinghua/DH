# External Authorities：外部权威数据库接入策略

## 总原则

V2 不应把所有外部数据库直接并入仓库。外部 authority 的正确接入方式是：

1. 本项目保存 crosswalk、external_id、查询脚本和引用说明；
2. 不直接再发布第三方原始数据库；
3. 不大量复制第三方数据库内容；
4. 所有授权不明的数据，一律只做链接和人工校验记录；
5. 外部数据库只作为辅助 authority，不替代文献原文判断。

## 一、CBDB

### 角色

CBDB 应作为 V2 的 **中国历史人物 authority layer**。

适用对象：

- 中国士人；
- 官员；
- 清廷学者；
- 序跋作者；
- 润色者；
- 儒家回应者；
- 与传教士互动的中国知识人。

典型例子：

- 钱大昕；
- 何国宗；
- 清廷相关官员；
- 地方士人。

### 不适用或弱适用对象

- 传教士；
- 教会机构；
- 修会网络；
- 教堂、学校、医院、出版社；
- 中国基督教空间网络。

这些应优先接入 CHCD / BDCC / Ricci Roundtable / RicciBase 等资源。

### 授权判断

CBDB SQLite 的 GitHub 仓库指向 Hugging Face 最新 SQLite 数据集。公开页面显示其 license 为 CC BY-NC-SA 4.0。该授权不是 MIT。

因此：

- 不将 CBDB SQLite 原始数据打包进本仓库；
- 不把本项目整体授权误写成“所有数据 MIT”；
- 只保存 `cbdb_id`、匹配状态、匹配证据与查询脚本；
- 如果发布包含 CBDB 派生字段的数据，必须遵守 CC BY-NC-SA 4.0；
- 商业或不确定用途应避免使用 CBDB 派生数据。

## 二、CHCD：China Historical Christian Database

### 角色

CHCD 应作为 V2 的 **中国基督教空间—机构—人物网络 authority layer**。

适用对象：

- 传教士；
- 中外基督徒；
- 教堂；
- 学校；
- 医院；
- 孤儿院；
- 出版机构；
- 地点；
- 机构内部工作人员；
- 宗教网络与空间网络。

CHCD 由 Boston University Center for Global Christianity and Mission 托管，覆盖 1550–1950 年中国基督教历史，并强调空间地图和关系网络。

### 授权策略

CHCD 官网说明 advanced DH users have open access to its data，但未在首页明确给出可再发布的开放许可证。因此 V2 应采取保守策略：

- 不抓取和再发布 CHCD 原始数据；
- 不复制大规模 CHCD 记录；
- 保存 CHCD URL、external_id、人工核验字段；
- 若需系统使用 CHCD 数据，应联系 CHCD 团队确认授权；
- 将 CHCD 作为 linked authority，而非内置数据源。

## 三、BDCC：Biographical Dictionary of Chinese Christianity

### 角色

BDCC 应作为 V2 的 **传教士与中国基督徒传记说明 authority**。

适用用途：

- 人物背景；
- 中文名 / 英文名互证；
- 传教士与中国基督徒的传记说明；
- 人物释名；
- 人物生平时间线补充。

### 授权策略

BDCC 更接近在线传记辞典。V2 不应抓取和再发布其全文内容。

允许：

- 保存 URL；
- 保存人物名规范化；
- 保存人工整理的极简事实字段；
- 在研究报告中引用。

不建议：

- 批量爬取全文；
- 将其传记文本复制进仓库；
- 把 BDCC 当作结构化主数据库。

## 四、authority crosswalk 表

建议新增：

```csv
entity_id,entity_text,entity_type,normalized_form,cbdb_id,chcd_id,bdcc_url,ricci_id,match_status,match_confidence,evidence,note
```

`match_status` 可用：

- unmatched
- candidate
- verified
- rejected
- ambiguous

`match_confidence` 可用：

- low
- medium
- high

## 五、authority 优先级

| 任务 | 首选 authority |
|---|---|
| 中国士人 / 官员消歧 | CBDB |
| 传教士人物 | CHCD + BDCC |
| 教会机构空间分布 | CHCD |
| 人物传记叙述 | BDCC |
| 西学文献作者与传教士中文名 | CHCD + BDCC + Ricci resources |
| 清廷官员网络 | CBDB |
| 中西知识网络 | CBDB + CHCD crosswalk |
