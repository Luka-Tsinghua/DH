# DH V2 使用指南

[项目首页](../README.md) / **V2** / [文档索引](docs/INDEX.md)

V2 是 DH 当前活跃的研究工具版本，使用 Python 标准库完成来源校验、文本分段、关键词上下文（KWIC）、证据候选与研究配置构建。所有自动生成的证据和论断均保留 `candidate` 状态。

## 运行处理链

需要 **Python 3.10+**。在仓库根目录执行：

```bash
python V2/scripts/dh_v2.py pipeline
```

该命令按顺序校验元数据与原始文本、构建分段、校验分段、生成 KWIC 与证据候选、构建既有研究配置的候选输出，最后写入文件清单。执行中任一步失败会停止后续步骤。

也可在 `V2/` 内使用既有 Make 入口：

```bash
make pipeline
make all
```

`make all` 还会运行测试和文档链接检查，需要先安装开发依赖。

## 开发安装

在仓库根目录建立独立环境：

```bash
python -m venv .venv
```

激活环境：

- macOS / Linux：`source .venv/bin/activate`
- Windows PowerShell：`.venv\Scripts\Activate.ps1`

再安装开发依赖：

```bash
python -m pip install -e "./V2[dev]"
dh-v2 --help
dh-v2-build-case --help
```

请使用可编辑安装并保留完整仓库：CLI 的默认配置、原始文本与输出路径以仓库位置为基准。Python 包本身不打包或重新授权研究语料。

## 单步命令

以下命令在仓库根目录运行。CLI 参数中的相对数据路径均以 `V2/` 为基准，与终端当前目录无关。

```bash
python V2/scripts/dh_v2.py validate-documents
python V2/scripts/dh_v2.py validate-raw-sources
python V2/scripts/dh_v2.py build-segments-from-raw
python V2/scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl
python V2/scripts/dh_v2.py generate-kwic --segments data/processed/full_segments.jsonl --output outputs/features/full_kwic_terms.csv
python V2/scripts/dh_v2.py generate-evidence-table --kwic outputs/features/full_kwic_terms.csv --output outputs/features/full_evidence_table.csv
python V2/scripts/dh_v2.py release-manifest
```

完整参数见 `python V2/scripts/dh_v2.py --help` 及各子命令的 `--help`。[处理流程](docs/PIPELINE.md)解释规范化、分段及候选结果的含义。

## 输入与输出

**输入**

- [原始文本清单](data/raw/RAW_SOURCE_MANIFEST.csv)：文献标识与来源路径。
- [文献元数据](data/metadata/documents_seed.csv)：来源、OCR、授权状态等字段。
- [领域词表](config/domain_lexicon_seed.csv)：关键词、规范形式与分类。
- 研究目录下的 `case_config.json`：输入分段、关注词与候选输出路径。

**可再生输出**

| 位置（相对 V2） | 内容 |
| :--- | :--- |
| `data/processed/full_segments.jsonl` | 固定字符长度的规范化文本分段 |
| `outputs/qc/` | 元数据、来源、分段的校验与构建报告 |
| `outputs/features/` | 完整文本 KWIC 与证据候选 CSV |
| 各研究目录的 `generated/` | 对应配置的 KWIC、证据、论断候选与构建报告 |
| `releases/manifest.json` | 文件清单与 SHA-256；不包含清单自身和本地环境、缓存 |

生成结果不自动写入人工整理的 CSV 或解释文本。[数据说明](data/README.md)与[复核规则](docs/REVIEW.md)说明各层材料的用途。

## 测试与检查

在已安装开发依赖的环境中，从仓库根目录运行：

```bash
python -m pytest V2/tests -q
python V2/scripts/check_docs.py
python -m py_compile V2/scripts/dh_v2.py V2/scripts/build_case.py
```

[GitHub Actions](../.github/workflows/v2-ci.yml) 在匹配路径的 `main` 与 `codex/**` 分支推送、面向 `main` 的拉取请求和手动触发时执行检查，覆盖 Python 3.10 / 3.13 与 Windows / Linux 环境。

## 继续阅读

- [文档索引](docs/INDEX.md)：数据、方法、维护与后续设计。
- [数据模型](docs/DATA_MODEL.md)：文献与证据的结构关系。
- [V2 贡献规范](CONTRIBUTING.md)：保护原始材料、保留复核字段。
- [数据与发布政策](docs/DATA_LICENSE_AND_RELEASE_POLICY.md)：分层处理授权；代码许可证尚待确定。
