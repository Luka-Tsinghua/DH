# V2 路线图
# V2 Roadmap

## 0. 当前状态 / Current State

V2 已经具备可维护项目脚手架，并且已经把仓库根目录中的《坤輿圖說》《地球圖説》WS 文本登记为真实 raw source。当前任务已经从“替换 sample data”转为“从完整 raw source 生成完整 segment、KWIC、evidence table，并完成首个正式 case 的人工复核”。

V2 now has a maintainable project scaffold and has registered the root-level WS texts of *Kunyu Tushuo* and *Diqiu Tushuo* as real raw sources. The current task has shifted from “replacing sample data” to generating full segments, KWIC, and evidence tables from complete raw sources, then completing human review for the first formal case.

---

## 1. 近期目标：从 scaffold 到 first formal case
## Near-term Goal: From Scaffold to First Formal Case

### 1.1 完整原文分段 / Full-source Segmentation

- 使用 `RAW_SOURCE_MANIFEST.csv` 登记的根目录 WS 文本作为 raw source。
- 运行 `build-segments-from-raw` 生成 `full_segments.jsonl`。
- 运行 `validate-segments` 检查完整 segment JSONL。
- 保留 `verified_excerpt_segments.jsonl` 作为 pilot case 的人工摘录层。
- 保留 `sample_segments.jsonl` 仅作为 smoke-test sample。

- Use the root-level WS texts registered in `RAW_SOURCE_MANIFEST.csv` as raw sources.
- Run `build-segments-from-raw` to generate `full_segments.jsonl`.
- Run `validate-segments` to check the full segment JSONL.
- Keep `verified_excerpt_segments.jsonl` as the manually curated excerpt layer for the pilot case.
- Keep `sample_segments.jsonl` only as a smoke-test sample.

### 1.2 完成第一个正式 case / Complete the First Formal Case

- 基于 `full_segments.jsonl` 为核心术语生成完整 KWIC。
- 从 KWIC 生成候选 evidence table。
- 从候选 evidence table 中人工筛选可解释证据。
- 将 candidate claims 逐条人工复核。
- 写出正式 interpretive note。

- Generate complete KWIC for core terms from `full_segments.jsonl`.
- Generate candidate evidence tables from KWIC.
- Manually select interpretable evidence from the candidate evidence table.
- Manually review candidate claims.
- Write a formal interpretive note.

### 1.3 安装 CI / Install CI

- 将 `V2/docs/CI_WORKFLOW_TEMPLATE.md` 中的 workflow 复制到 `.github/workflows/v2-ci.yml`。
- 确认 push 和 pull request 时能自动运行 raw source validation、segment build、KWIC、evidence table、release manifest 和 smoke tests。

- Copy the workflow in `V2/docs/CI_WORKFLOW_TEMPLATE.md` to `.github/workflows/v2-ci.yml`.
- Confirm that push and pull request automatically run raw source validation, segment build, KWIC, evidence table generation, release manifest, and smoke tests.

---

## 2. 中期目标：扩展语料 / Mid-term Goal: Corpus Expansion

- 新增至少 3 部明清西学中文文献。
- 为每部文献建立 metadata、raw source manifest、segments、KWIC、claims review。
- 建立人物、机构、术语和 authority crosswalk 的基础样例。

- Add at least three more Ming-Qing Western Learning texts.
- Create metadata, raw source manifest entries, segments, KWIC, and claims review for each text.
- Build initial samples for persons, institutions, terms, and authority crosswalks.

---

## 3. 长期目标：研究平台 / Long-term Goal: Research Platform

- 形成可发布 corpus release。
- 建立面向研究者和学生的学术网页界面。
- 输出可复核的小型数字论文。
- 支持课程教学和跨项目复用。

- Produce publishable corpus releases.
- Build a scholarly web interface for researchers and students.
- Produce reviewable small digital essays.
- Support teaching and reuse across projects.
