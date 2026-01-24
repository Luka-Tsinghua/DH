# DH

本仓库为“数字人文国际联合暑期工作坊2023”（https://camp2023.pkudh.org/）的部分成果。

This repository documents a digital humanities workflow comparing two Jesuit missionary texts:
- 1674 《坤輿圖說》
- 1799 《地球圖説》

The goal is to trace how geographic and astronomical knowledge in China changed across time.

## Data sources

The working example uses a sample PDF containing two books. The full database contains 69 missionary documents. See:
- `DH/2_database_prompt_EN.txt`
- `DH/2_database_prompt_CN.txt`

## Workflow overview

1) OCR the PDF into a single `.txt` file.
- Recommended OCR: Foxit PDF Reader, text type set to Taiwan Traditional Chinese.
- Manual verification is required to ensure OCR quality.

2) Manual cleanup and book boundary tagging.
- Remove covers, non-missionary prefaces/postfaces, footnotes.
- Mark book boundaries with `["Book_Title"]` and `[/"Book_Title"]`.
- Save as `_work1.txt`.

3) Text cleaning and book extraction via ChatGPT CI.
- Remove punctuation, English letters, numbers, spaces, and line breaks.
- Preserve the book boundary symbols.
- Extract each book into its own `_cleaned1.txt` file.

4) Verification of extracted files.
- Re-check zero-byte outputs and re-run extraction if needed.
- Optionally package outputs into a `.zip`.

5) (Optional) Merge all books into a single database `.txt` file.
- Can be automated with Python if handling many documents.

## Python annotation (CkipTagger)

Two scripts are provided:
- `DH/3_Jesuitknowledge_1.py`: single-file annotation; downloads model from Google Drive.
- `DH/3_Jesuitknowledge_2.py`: batch annotation of all `.txt` files in an input folder; assumes model already downloaded locally.

Both scripts output WS/POS/NER results. Update the data, input, and output paths before running.

## Example outputs

Pre-segmented samples (WS results):
- `DH/1674_坤輿圖說_WS.txt`
- `DH/1799_地球圖説_WS.txt`

Extraction guidance:
- `DH/3_extraction_EN.txt`
- `DH/3_extraction_CN.txt`

## Analysis step

1) Use the CText N-gram tool to extract word frequencies from the WS files:
- http://ctext.org/plugins/texttools/#ngram

2) Manually filter results.

3) Analyze using ChatGPT Code Interpreter.

## Dependencies

- Python 3.x
- CkipTagger: https://github.com/ckiplab/ckiptagger

## Notes

- CkipTagger segmentation quality is higher than Jieba but still requires manual verification.
- Prompts for cleaning/extraction are provided in `DH/2_database_prompt_EN.txt` and `DH/2_database_prompt_CN.txt`.
