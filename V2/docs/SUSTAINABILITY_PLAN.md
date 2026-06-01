# Sustainability Plan

## 一、项目可持续性的核心

V2 的可持续性不取决于某个模型，而取决于：

- 稳定的数据模型；
- 可回溯的材料来源；
- 明确的授权边界；
- 分层文本版本；
- 可重复运行的 pipeline；
- 人工校验机制；
- 长期 release 节奏；
- 能产生真实文史研究问题。

## 二、技术可持续性

原则：

- 使用纯文本、CSV、JSONL、SQLite、Parquet 等长期可读格式。
- 不依赖单一闭源模型。
- LLM 输出必须可替换。
- embedding 模型可替换。
- 所有脚本应可在本地运行。
- 所有输出应能从 raw + scripts 重新生成。

## 三、学术可持续性

项目应持续服务于具体研究：

- 明清西学史；
- 耶儒对话；
- 清廷知识制度；
- 传教士中文写作；
- 中国士人与外来知识；
- 地理、天文、制图知识传播；
- 概念翻译史；
- 文史 AI 方法论。

## 四、组织可持续性

建议每月进行一次：

- 新材料录入；
- OCR QC；
- metadata 校验；
- authority matching；
- 文献学复核；
- issue 清理。

建议每季度发布：

- corpus inventory update；
- authority update；
- method note；
- pilot report update。

## 五、失败风险

| 风险 | 后果 | 应对 |
|---|---|---|
| 只做图表 | 项目退化为展示 | 强制 evidence-based report |
| 过度依赖 LLM | 解释不可控 | LLM 输出降级为候选 |
| 授权不清 | 无法公开 | external authority 不入库 |
| raw data 被覆盖 | 无法回溯 | raw immutable |
| metadata 缺失 | 后期不可用 | inventory 先行 |
| 研究问题不清 | 技术空转 | 每个 release 附 research note |
