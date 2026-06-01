.PHONY: validate raw segments kwic evidence release test pipeline

validate:
	python scripts/dh_v2.py validate-documents
	python scripts/dh_v2.py validate-raw-sources

raw:
	python scripts/dh_v2.py validate-raw-sources

segments:
	python scripts/dh_v2.py build-segments-from-raw
	python scripts/dh_v2.py validate-segments --segments data/processed/full_segments.jsonl

kwic:
	python scripts/dh_v2.py generate-kwic --segments data/processed/full_segments.jsonl --output outputs/features/full_kwic_terms.csv

evidence:
	python scripts/dh_v2.py generate-evidence-table --kwic outputs/features/full_kwic_terms.csv --output outputs/features/full_evidence_table.csv --limit 200

release:
	python scripts/dh_v2.py release-manifest

test:
	pytest tests

pipeline: validate segments kwic evidence release
