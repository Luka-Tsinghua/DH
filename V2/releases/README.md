# V2 发布目录说明
# V2 Releases Directory Guide

本目录用于保存 V2 的 release manifest 和可发布版本说明。

This directory stores V2 release manifests and release notes.

---

## 1. 生成 release manifest / Generate a Release Manifest

```bash
python V2/scripts/dh_v2.py release-manifest
```

该命令默认输出：

The command outputs by default:

```text
V2/releases/release_manifest.json
```

---

## 2. 发布前原则 / Pre-release Principles

发布前必须确认：

Before release, confirm that:

- raw data 没有被覆盖；
- raw data has not been overwritten;
- sample data 没有被误标为正式古籍证据；
- sample data is not mislabeled as verified source evidence;
- metadata 已通过 validation；
- metadata has passed validation;
- claims 均有 evidence quote 和 review status；
- claims have evidence quotes and review status;
- 外部 authority 数据保留来源和授权说明。
- external authority data preserves source and license notes.
