# Quality Assurance

## 一、QC 层级

### File-level QC

检查：

- 文件是否为空；
- 编码是否为 UTF-8；
- 字符数；
- 行数；
- 异常字符数量；
- 数字数量；
- 拉丁字母数量；
- OCR 噪声；
- 是否疑似重复文件。

### Document-level QC

检查：

- 标题是否规范；
- 作者是否明确；
- 年代是否明确；
- 来源是否明确；
- 文献边界是否明确；
- 是否有序跋、脚注、页眉页脚；
- 是否需要校勘。

### Segment-level QC

检查：

- 段落长度；
- 是否断裂；
- 是否跨章节；
- 是否保留 evidence；
- 是否可回溯到原文。

### Extraction-level QC

检查：

- 实体是否有 evidence_quote；
- 术语是否有 normalized_form；
- claim 是否有原文依据；
- authority match 是否人工校验；
- 模型置信度是否过度乐观。

## 二、人工抽样标准

每本文献至少检查：

- 开头 500 字；
- 中部 500 字；
- 结尾 500 字；
- 数字密集段；
- 音译词密集段；
- 人名机构密集段；
- 疑似 OCR 错误段。

## 三、红线

以下结果不得进入 release：

- 无来源 metadata；
- 无 evidence 的 claim；
- 授权不明的外部数据；
- 未区分 raw 和 cleaned 的文本；
- 无法复现的分析结果；
- LLM 生成但未人工复核的实体关系。
