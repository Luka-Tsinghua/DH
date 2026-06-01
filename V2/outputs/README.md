# V2 输出目录说明
# V2 Outputs Directory Guide

本目录保存由脚本生成的中间结果、质检报告、features 和研究报告。

This directory stores script-generated intermediate outputs, QC reports, features, and research reports.

---

## 1. 推荐结构 / Recommended Structure

```text
outputs/
├── qc/          # validation and inventory reports
├── features/    # lexicon exports, KWIC outputs, feature tables
└── reports/     # generated research or maintenance reports
```

---

## 2. 原则 / Principles

自动生成结果应当可重新生成，而不是作为唯一版本保存。

Generated outputs should be reproducible, not preserved as the only version.

脚本输出如果参与研究解释，必须在 case 中绑定 evidence quote 和 review status。

If script outputs support interpretation, they must be linked to evidence quotes and review status inside a research case.
