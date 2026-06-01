# 解释札记：《坤輿圖說》与《地球圖説》的真实文本摘录比较
# Interpretive Note: Comparing Real Repository Excerpts from *Kunyu Tushuo* and *Diqiu Tushuo*

## 1. 当前材料状态 / Current Source Status

本案例已经不再以 synthetic sample 作为主线。V2 现在使用仓库根目录中已经存在的两个真实文本文件作为 raw source：`1674_坤輿圖說_WS.txt` 与 `1799_地球圖説_WS.txt`。

This case no longer uses synthetic samples as its main line. V2 now treats the two existing root-level repository files as raw sources: `1674_坤輿圖說_WS.txt` and `1799_地球圖説_WS.txt`.

`V2/data/processed/verified_excerpt_segments.jsonl` 保存从上述 raw source 中抽取并经 V2 标点整理的摘录段落。它们是可用于 pipeline 的真实仓库文本摘录，但仍需要进一步做版本、页码、卷次和校勘层面的正式核验。

`V2/data/processed/verified_excerpt_segments.jsonl` stores excerpt segments extracted from those raw sources and punctuated for V2 processing. They are real repository-text excerpts usable for the pipeline, but still require formal verification of edition, page, fascicle, and collation details.

## 2. 初步观察 / Preliminary Observations

《坤輿圖說》的开端以“全地相聯貫合之大端”说明全地知识的总括性，并列举地形、地震、山岳、海潮、江河、人物、风俗与物产等范围。这说明它不是单纯地理名词表，而是把自然地理、世界知识和人文风俗放在同一个“坤舆”框架下。

The opening of *Kunyu Tushuo* frames the work as a general account of the connected whole earth and lists terrain, earthquakes, mountains, tides, rivers, peoples, customs, and products. This suggests that it is not merely a geographical glossary, but a framework that joins physical geography, world knowledge, and human customs under the category of “Kunyu.”

《坤輿圖說》又以“地與海本是圓形而合爲一球”说明地海合为球体，并通过“地爲方”的解释把传统说法转化为“定而不移之性”，而非形体判断。这一处理体现出一种解释性调和：它不是简单否定旧说，而是重新限定旧说的语义层级。

*Kunyu Tushuo* also states that earth and sea together form a sphere, while reinterpreting the traditional claim that the earth is square as referring to stability rather than physical shape. This is an interpretive reconciliation: the old claim is not simply rejected, but reassigned to a different semantic level.

《地球圖説》则直接以“地圓如球”“兩半球”“全球”等图说语言展开，且题署中出现“奉旨譜譯”“奉旨潤色”及何国宗、钱大昕等清廷官员身份。这说明《地球圖説》的表达更强烈地处于清廷制度化知识生产语境中。

*Diqiu Tushuo* more directly uses diagrammatic language such as “earth round like a sphere,” “two hemispheres,” and “globe.” Its title statement also names imperial translation and revision by Qing officials such as He Guozong and Qian Daxin. This places the text more explicitly within Qing institutional knowledge production.

## 3. 可检验命题 / Reviewable Claims

当前 `claims_review.csv` 已经用真实仓库文本摘录替换原有 sample claims。所有 claim 仍标为 `candidate`，因为下一步还需要人工核验版本、页码、断句和原始 OCR。

The current `claims_review.csv` has replaced the original sample claims with claims based on real repository-text excerpts. All claims remain marked as `candidate` because the next step is to verify edition, page, punctuation, and raw OCR.

## 4. 下一步 / Next Steps

第一步应从根目录 raw source 自动生成完整 segment JSONL，而不是只保留摘录段落。

The first next step should be to generate full segment JSONL from the root-level raw sources, not only excerpt segments.

第二步应围绕“地球 / 坤舆 / 赤道 / 经度 / 纬度 / 半球 / 全球 / 五洲”等核心术语生成完整 KWIC 表。

The second step should generate a complete KWIC table for core terms such as earth, Kunyu, equator, longitude, latitude, hemisphere, globe, and continents.

第三步应把《坤輿圖說》与《地球圖説》的概念表达差异转化为可复核的 claim group，而不是直接写成结论。

The third step should turn the conceptual differences between *Kunyu Tushuo* and *Diqiu Tushuo* into reviewable claim groups rather than immediate conclusions.
