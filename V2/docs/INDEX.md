# DH V2 文档

[项目首页](../../README.md) / [V2 使用指南](../README.md) / **文档**

从运行工具到复核证据，按当前任务选择阅读入口。

## 开始使用

- [V2 使用指南](../README.md)：环境、完整处理链、单步命令与检查。
- [处理流程](PIPELINE.md)：原始文本、规范化分段、KWIC 与候选证据。
- [仓库结构](REPOSITORY_STRUCTURE.md)：当前目录与职责。

## 研究方法与数据

- [方法原则](METHOD.md) · [复核规则](REVIEW.md)：证据与解释的边界。
- [数据模型](DATA_MODEL.md) · [数据层说明](../data/README.md)：字段、来源与各层材料。
- [OCR 与校勘规范](OCR_AND_COLLATION_PROTOCOL.md)：原书核对、版本与文本质量。
- [数据与发布政策](DATA_LICENSE_AND_RELEASE_POLICY.md)：不同材料层级的授权与发布范围。
- [研究纲领](../research/RESEARCH_PROGRAM.md) · [项目章程](../research/PROJECT_CHARTER.md)：研究问题与项目范围。

## 贡献与维护

- [仓库贡献指南](../../CONTRIBUTING.md) · [V2 贡献规范](../CONTRIBUTING.md)
- [质量检查](QUALITY_ASSURANCE.md) · [维护计划](MAINTENANCE_PLAN.md)
- [治理](GOVERNANCE.md) · [持续维护](SUSTAINABILITY_PLAN.md)
- [成熟度记录](MATURITY_STATUS.md) · [项目检查清单](PROJECT_MATURITY_CHECKLIST.md)
- [路线图](ROADMAP.md) · [当前 CI 配置](../../.github/workflows/v2-ci.yml)

## 设计与后续方向

以下文档包含设计建议与未来方向，需与已实现的 CLI 功能区分阅读。

- [学术界面设计](SCHOLARLY_INTERFACE_DESIGN.md)
- [Web 架构设计](WEBCODING_ARCHITECTURE.md)
- [外部权威数据关联](EXTERNAL_AUTHORITIES.md)
- [研究工作流设计](WORKFLOW.md)
- [人文研究与数字方法](HUMANITIES_DH_WEBCODING_MANIFESTO.md)

## 运行入口

在仓库根目录：

```bash
python V2/scripts/dh_v2.py pipeline
python -m pytest V2/tests -q
python V2/scripts/check_docs.py
```
