# PREPARE Run Notes

## Inputs
- Raw directory: `data\raw`

## Outputs
- `prepare_file_profile.csv`
- `prepare_dataset_summary.csv`
- `prepare_key_validation_summary.csv`
- `*_column_profile.csv`
- `*_overview.json`
- `*_key_validation.json`
- `prepare_output_summary.md`

## Purpose
This run profiles the raw dataset package for structural understanding only.
No cleaning or transformation is applied here.

## Validation scope
- file-level row/column checks
- schema profiling
- null profiling
- duplicate full-row checks
- candidate primary key validation

## Limitations
- no economic interpretation
- no return calculations
- no frequency harmonization
- no source-authority reconciliation
