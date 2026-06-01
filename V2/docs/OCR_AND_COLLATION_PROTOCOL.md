# OCR and Collation Protocol：OCR 与校勘规范

## 一、为什么 OCR 与校勘是学术工作

在明清西学文本研究中，OCR 与校勘不是单纯的技术前处理。它们直接影响研究对象本身。

例如：

- 数字、度量衡、经纬度可能是地理和天文知识的核心证据；
- 人名、官职、机构名可能揭示知识生产网络；
- 题名、卷次、序跋、奉旨、润色等信息可能揭示文本制度背景；
- 音译地名和术语变体可能是概念史与翻译史的重要材料。

因此，清洗不能只追求“干净”，而必须追求“可解释、可回溯、可复核”。

## 二、Raw Data 原则

`V2/data/raw/` 中的文件视为原始层。

规则：

1. 不覆盖 raw data。
2. 不直接在 raw 文件中修正 OCR。
3. 不删除 raw 文件中的序跋、卷次、署名、注释和图题。
4. 不把 raw data 当作可随意格式化的临时文本。
5. 如果发现错误，应在 processed 层和 collation log 中记录。

## 三、文本层级

### raw

原始 OCR 或转写文本。

### raw_normalized

基础编码和空白规范化，尽量不改变文本内容。

### reading_clean

供阅读和校勘使用。可以去除明显页码和噪声，但保留句读、数字、音译词、题名和署名。

### analysis_clean

供统计和抽取使用。可以压缩空白，但仍应保留数字、拉丁字母、度量衡和可疑字。

### segments

用于证据回溯的段落单位。

## 四、OCR 质量等级

| 等级 | 含义 |
|---|---|
| A | 几乎可直接使用，只有少量疑难字 |
| B | 可使用，但需要抽样校对 |
| C | 错误较多，需要系统校对 |
| D | 只能作为参考，建议重新 OCR |
| E | 不可用 |

## 五、校勘日志

建议建立：

```text
V2/data/metadata/collation_log.csv
```

字段：

```csv
document_id,segment_id,location,before,after,reason,source_basis,reviewer,date,confidence
```

### before / after

必须记录修改前后的文本。

### reason

可填写：

- OCR error；
- variant character；
- punctuation restoration；
- page header removed；
- footnote separated；
- uncertain correction；
- source comparison。

### confidence

建议使用：

- low；
- medium；
- high。

## 六、常见错误类型

- 繁体字误识；
- 异体字误识；
- 数字误识；
- 度量单位误识；
- 西文音译词误识；
- 人名误识；
- 官职和机构名误识；
- 页眉页脚混入正文；
- 注释混入正文；
- 行间断裂；
- 图题误入正文。

## 七、人工抽样校验

每本文献至少校验：

- 开头 500 字；
- 中部 500 字；
- 结尾 500 字；
- 数字密集段；
- 音译词密集段；
- 人名和机构密集段；
- 疑似 OCR 错误段。

## 八、不可接受做法

- 直接删除所有数字；
- 直接删除所有拉丁字母；
- 直接删除所有标点；
- 直接删除序跋和署名信息；
- 未记录原因就修改文本；
- 把自动清洗结果当作校勘文本；
- 把模型判断当作校勘依据。

## 九、文史学科底线

OCR 与校勘的目标不是让文本更适合机器，而是让文本更适合可靠研究。机器可读性必须服从文献可解释性。