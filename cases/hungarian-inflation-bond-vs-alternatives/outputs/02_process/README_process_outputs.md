# PROCESS Run Notes

## Inputs
- Raw directory: `data\raw`

## Outputs
- raw_snapshot hashes preserved through summary generation
- etf_ticker_coverage_profile.csv
- etf_null_window_classification_detailed.csv
- etf_null_window_classification_summary.csv
- cleaned CSV outputs
- month-end ETF resample
- monthly merged context
- process_output_summary.md

## Execution order
1. ticker coverage profiling
2. ETF null-window validation
3. dataset cleaning and normalization
4. monthly resampling and merged context generation
5. summary generation

## Guardrails
- no silent filtering
- no imputation of ETF close prices
- percent normalization adds columns instead of overwriting raw strings
- resampling rule is explicit and auditable
