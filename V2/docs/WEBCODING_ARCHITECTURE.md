# Webcoding Architecture：V2 Web 架构设计

## 推荐路线

```text
Astro + MDX + TypeScript + JSON/CSV data + lightweight interactive components
```

## 选择理由

V2 是文本密集、方法密集、证据密集的人文项目。它的大部分内容是相对稳定的研究说明、文献页面、案例页面、术语页面和方法页面，因此应采用静态优先的架构。

推荐 Astro 作为主框架，因为：

- 适合 content-heavy scholarly site；
- Markdown / MDX 适合写研究案例和方法说明；
- content collections 适合管理结构化内容；
- 静态构建适合 GitHub Pages / Cloudflare Pages / Netlify；
- 可渐进加入 D3 / Observable / React / Svelte 等交互组件。

## 页面类型

1. Project Home：说明项目使命、V1/V2 差异、材料范围和授权。
2. Corpus Browser：浏览文献 metadata、OCR 状态、校勘状态。
3. Document Page：展示 metadata、segments、terms、entities、claims。
4. Concept Page：展示术语变体、KWIC、历时分布和解释。
5. Person / Institution Page：展示 authority crosswalk 与证据段落。
6. Research Case Page：小型数字论文。
7. Method Page：解释清洗、抽取、LLM、authority 接入。
8. Teaching Page：说明后来者如何复用。

## 数据流

```text
V2/data/raw
  ↓
V2/scripts/v2_clean_corpus.py
  ↓
V2/data/processed/*/segments.jsonl
  ↓
V2/scripts/v2_extract_features.py
  ↓
V2/outputs/features/*.csv
  ↓
V2/web/scripts/export_for_web.py
  ↓
V2/web/src/data/*.json
  ↓
Astro pages and components
```

## 不建议一开始做重型全栈

早期不需要用户系统、动态写入和复杂后端。应先完成静态 scholarly site。若后续需要多人在线校勘，再单独开发 annotation backend。
