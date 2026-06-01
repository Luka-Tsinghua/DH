# 解释札记：从样例链条到正式研究
# Interpretive Note: From Sample Chain to Formal Research

本文件目前不是正式研究结论，而是一个解释层模板。它展示 V2 的研究案例应如何从证据表、KWIC 表和 claim review 表进入可审查的解释写作。

This file is not yet a formal research conclusion. It is an interpretive-layer template showing how a V2 research case should move from evidence tables, KWIC tables, and claim review tables toward reviewable scholarly interpretation.

## 1. 当前状态 / Current Status

当前 `sample_segments.jsonl` 中的两条文本是 pipeline 测试样例，不应被引用为真实古籍原文。

The two records in `sample_segments.jsonl` are pipeline test samples and should not be cited as verified source passages.

它们的作用是让项目具备最小闭环：metadata → segment → lexicon → KWIC → claim review → interpretive note。

Their purpose is to provide a minimal closed loop: metadata → segment → lexicon → KWIC → claim review → interpretive note.

## 2. 正式研究需要替换的内容 / What Must Be Replaced for Formal Research

1. 用经过来源核验的《坤輿圖說》和《地球圖説》文本替换 sample segment。
2. 为每一段补充版本、页码或卷次信息。
3. 将 `candidate` 状态的 claim 逐条人工复核。
4. 区分文本中直接出现的知识命题和研究者解释性的概括。
5. 对每一个术语变体记录 normalized form 和上下文。

1. Replace sample segments with source-verified passages from *Kunyu Tushuo* and *Diqiu Tushuo*.
2. Add edition, page, or fascicle information for every segment.
3. Manually review every claim marked as `candidate`.
4. Distinguish direct textual claims from the researcher's interpretive summaries.
5. Record normalized forms and contexts for every term variant.

## 3. 后续正式问题 / Next Formal Questions

《坤輿圖說》中“坤舆”与“地球”的关系是否体现了传统宇宙空间词汇与西方球形地理知识之间的转译？

Does the relation between “Kunyu” and “earth” in *Kunyu Tushuo* reflect a translation between traditional cosmographic vocabulary and Western spherical geography?

《地球圖説》中经纬、赤道、五洲等术语是否呈现出更制度化、更教科书化的知识表达？

Do terms such as longitude/latitude, equator, and continents in *Diqiu Tushuo* indicate a more institutionalized or textbook-like mode of knowledge presentation?

这些问题不能仅由词频回答，必须回到具体语境、文体、读者预设和清廷制度空间。

These questions cannot be answered by term frequency alone. They require attention to context, genre, imagined readership, and Qing institutional space.
