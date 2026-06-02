# Repository Structure

This document defines the intended structure of the active V2 research version. It is written for human researchers, students, and automation agents.

## Root level

```text
.
├── README.md
├── CONTRIBUTING.md
├── .github/workflows/v2-ci.yml
├── 1674_坤輿圖說_WS.txt
├── 1799_地球圖説_WS.txt
├── V2/
└── DH/
```

## Root-level roles

- `README.md`: repository-level navigation hub.
- `CONTRIBUTING.md`: repository-level contribution rules.
- `.github/workflows/v2-ci.yml`: CI workflow, currently kept as manual dispatch while checks are stabilized.
- `1674_坤輿圖說_WS.txt`: raw source used by V2.
- `1799_地球圖説_WS.txt`: raw source used by V2.
- `V2/`: active reproducible research version.
- `DH/`: historical V1 workshop archive.

## V2 structure

```text
V2/
├── README.md
├── CONTRIBUTING.md
├── Makefile
├── pyproject.toml
├── config/
├── data/
├── schemas/
├── scripts/
├── tests/
├── cases/
├── docs/
├── outputs/
└── releases/
```

## V2 roles

- `config/`: project configuration and controlled vocabulary seed.
- `data/`: raw source manifest, document metadata, processed segments, and authority crosswalk seeds.
- `schemas/`: JSON schemas for structured research objects.
- `scripts/`: stable command-line tools and case builder.
- `tests/`: smoke tests for the minimum reproducible pipeline.
- `cases/`: research cases with curated files and generated candidate outputs.
- `docs/`: methods, pipeline, review protocol, governance, roadmap, and policy documents.
- `outputs/`: generated runtime outputs. These are reproducible and should not be confused with curated scholarship.
- `releases/`: release manifests and release-oriented files.

## Generated versus curated

Generated candidate outputs should remain under:

```text
V2/outputs/
V2/cases/<case_id>/generated/
```

Curated scholarly files should remain under each case directory root:

```text
V2/cases/<case_id>/evidence_table.csv
V2/cases/<case_id>/claims_review.csv
V2/cases/<case_id>/interpretive_note.md
```

No generated row should become a scholarly conclusion without human review.

## Expansion rules

When adding a new text:

1. Register the raw source in `data/raw/RAW_SOURCE_MANIFEST.csv`.
2. Add document metadata in `data/metadata/documents_seed.csv`.
3. Run validation.
4. Generate segments.
5. Create or extend a case.
6. Keep generated outputs separate from curated files.

When adding a new case:

1. Create `case_config.json`.
2. Create `README.md`.
3. Create `generated/README.md`.
4. Add curated CSV files only after review.
5. Document uncertainty in `interpretive_note.md`.
