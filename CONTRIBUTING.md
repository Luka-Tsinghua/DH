# Contributing

This repository is a humanities research project, not only a code repository. Contributions should improve evidence control, source transparency, reproducibility, or long-term maintainability.

## Active area

- `V2/` is the active research version.
- Early workshop files remain at the repository root; the V1 snapshot is on the `v1-original-archive-2026` branch.
- Root-level WS text files are raw sources and should not be overwritten.

## Before changing files

1. Read `README.md`.
2. Read `V2/README.md`.
3. Check `V2/docs/PIPELINE.md` and `V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md` if you are changing data or generated outputs.
4. Check `V2/CONTRIBUTING.md` for detailed V2 rules.

## Minimum rules

- Do not overwrite raw source files.
- Do not treat generated outputs as reviewed scholarship.
- Preserve `document_id`, `segment_id`, `evidence_quote`, and `review_status` for claims.
- Keep generated files separate from curated case files.
- Update tests and documentation when changing the pipeline.

## Recommended checks

From the repository root, after installing development dependencies with `python -m pip install -e "./V2[dev]"`, run:

```bash
python V2/scripts/dh_v2.py pipeline
python -m pytest V2/tests -q
python V2/scripts/check_docs.py
```

If this fails, fix the failing step before expanding the repository further.
