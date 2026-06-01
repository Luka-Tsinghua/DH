# V2 路线图
# V2 Roadmap

## 0. 当前状态 / Current State

V2 已经具备可维护项目脚手架，但尚未达到成熟研究项目状态。

V2 now has a maintainable project scaffold, but it has not yet reached the status of a mature research project.

---

## 1. 近期目标：从 scaffold 到 first formal case
## Near-term Goal: From Scaffold to First Formal Case

### 1.1 替换 sample data / Replace Sample Data

- 获取经过来源核验的《坤輿圖說》文本片段。
- 获取经过来源核验的《地球圖説》文本片段。
- 用真实 segment JSONL 替换或并列保留 `sample_segments.jsonl`。
- 明确版本、页码、卷次、OCR 状态和校勘状态。

- Add source-verified passages from *Kunyu Tushuo*.
- Add source-verified passages from *Diqiu Tushuo*.
- Replace or supplement `sample_segments.jsonl` with real segment JSONL.
- Record edition, page, fascicle, OCR status, and collation status.

### 1.2 完成第一个正式 case / Complete the First Formal Case

- 为核心术语生成 KWIC。
- 为每条观察补充 evidence quote。
- 将 candidate claims 逐条人工复核。
- 写出正式 interpretive note。

- Generate KWIC for core terms.
- Add evidence quotes for every observation.
- Manually review candidate claims.
- Write a formal interpretive note.

### 1.3 安装 CI / Install CI

- 将 `V2/docs/CI_WORKFLOW_TEMPLATE.md` 中的 workflow 复制到 `.github/workflows/v2-ci.yml`。
- 确认 push 和 pull request 时能自动运行最低检查。

- Copy the workflow in `V2/docs/CI_WORKFLOW_TEMPLATE.md` to `.github/workflows/v2-ci.yml`.
- Confirm that minimum checks run automatically on push and pull request.

---

## 2. 中期目标：扩展语料 / Mid-term Goal: Corpus Expansion

- 新增至少 3 部明清西学中文文献。
- 为每部文献建立 metadata、segments、KWIC、claims review。
- 建立人物、机构、术语和 authority crosswalk 的基础样例。

- Add at least three more Ming-Qing Western Learning texts.
- Create metadata, segments, KWIC, and claims review for each text.
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
