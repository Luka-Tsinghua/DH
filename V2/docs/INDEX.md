# V2 Documentation Index

This index gives readers and agents a stable entry point into the V2 documentation.

## Start here

- `V2/README.md` — V2 overview and quick start.
- `V2/docs/PIPELINE.md` — reproducible processing workflow.
- `V2/docs/METHOD.md` — methodological principles.
- `V2/docs/REVIEW.md` — review statuses and candidate-output rules.

## Data and release policy

- `V2/data/README.md` — data-layer explanation.
- `V2/docs/DATA_LICENSE_AND_RELEASE_POLICY.md` — layered data and release policy.
- `V2/docs/EXTERNAL_AUTHORITIES.md` — external authority strategy.

## Maintenance and governance

- `V2/CONTRIBUTING.md` — detailed contribution rules for V2.
- `V2/docs/MAINTENANCE_PLAN.md` — maintenance plan.
- `V2/docs/PROJECT_MATURITY_CHECKLIST.md` — maturity checklist.
- `V2/docs/ROADMAP.md` — project roadmap.
- `V2/docs/CI_WORKFLOW_TEMPLATE.md` — workflow template.

## Current research case

- `V2/cases/kunyu_diqiu_comparison/README.md`
- `V2/cases/kunyu_diqiu_comparison/case_config.json`
- `V2/cases/kunyu_diqiu_comparison/interpretive_note.md`
- `V2/cases/kunyu_diqiu_comparison/generated/README.md`

## Operational entry points

From `V2/`:

```bash
make pipeline
make all
```

`make pipeline` builds the reproducible research pipeline. `make all` runs the pipeline and smoke tests.
