# Energy Market Dashboard — PROCESS Artifact

## 1. Case Metadata

- **Project Name:** Energy Market Dashboard
- **Case ID:** 2026-EMD-001
- **Phase:** PROCESS
- **Author:** Gábor Sala
- **Date:** 2026-04-05
- **Project Type:** Dashboard / Visualization Project

---

## 2. PROCESS Phase Purpose

The PROCESS phase transforms raw downloaded market data into a clean, standardized, analysis-ready dataset.

Its purpose is to:

- clean raw market data
- standardize schema
- validate data integrity
- align time series across instruments
- define null-handling rules
- prepare a consistent dataset for downstream feature engineering and dashboard use

This phase does **not** produce final business interpretation.
It creates the controlled analytical dataset used by ANALYZE and dashboard development.

---

## 3. Input Datasets

Expected input sources from PREPARE:

- `data/raw/wti_raw.csv`
- `data/raw/brent_raw.csv`
- `data/raw/natgas_raw.csv`
- `data/raw/xle_raw.csv`
- `data/raw/spy_raw.csv`

or a combined raw file such as:

- `data/raw/market_data_raw.csv`

---

## 4. Target Output Datasets

The PROCESS phase should generate:

### 4.1 Combined Clean Dataset
- `data/processed/market_data_combined.csv`

Contains:
- all target instruments
- standardized schema
- cleaned records
- one row per (`date`, `ticker`)

### 4.2 Aligned Dataset
- `data/processed/market_data_aligned.csv`

Contains:
- common overlapping window across all required instruments
- cleaned series suitable for comparison and feature engineering

### 4.3 Process Audit Output
- `artifacts/process_audit.csv`

Contains:
- row counts before and after cleaning
- null handling summary
- duplicate removal summary
- alignment window summary

---

## 5. Processing Objectives

The raw data must be transformed so that:

- all datasets share the same column naming convention
- dates are parsed consistently
- duplicated observations are removed
- numerical columns are coerced safely
- instruments are clearly labeled
- aligned comparison across instruments becomes possible

---

## 6. Standard Schema

The standardized schema for the combined clean dataset is:

```text
date
ticker
open
high
low
close
adj_close
volume

Rules:

column names must be lowercase
use snake_case
date must be datetime-compatible
ticker must be uppercase symbol string
7. Processing Rules
7.1 Column Standardization
convert incoming column names to lowercase
rename adj close or similar variants to adj_close
add ticker column if missing in source file
preserve only required columns for V1
7.2 Date Handling
parse date as datetime
drop rows where date parsing fails
sort rows by ticker, date
7.3 Numeric Handling
coerce open, high, low, close, adj_close, volume to numeric
invalid numeric values become null
record null counts after coercion
7.4 Duplicate Handling
duplicates are defined on (date, ticker)
if duplicates exist, keep the last valid observation unless source logic requires otherwise
duplicate removal must be logged
7.5 Null Handling
rows missing date or ticker must be dropped
rows missing all core price fields must be dropped
rows missing some non-critical fields may remain temporarily if still usable
null handling decisions must be logged explicitly
7.6 Price Field Preference

Primary analytical price field for downstream return calculations:

adj_close, when available and sufficiently populated

Fallback:

close, if adj_close is unavailable or structurally incomplete

This decision must be documented in the processing notes.

8. Alignment Policy

A distinction must be maintained between:

8.1 Combined Clean Dataset

Preserves each instrument’s cleaned history individually.

8.2 Aligned Dataset

Restricts the data to the common overlapping date range across all required instruments.

This aligned dataset is the default base for:

relative comparisons
normalized performance charts
rolling feature calculations
dashboard cross-asset views
9. Common Window Logic

The aligned dataset must:

include all required V1 instruments
identify the latest minimum start date across all instruments
identify the earliest maximum end date across all instruments
restrict the final aligned data to that common range

This prevents misleading comparisons caused by unequal history lengths.

10. Process Validation Checklist

Before PROCESS is considered complete, validate:

10.1 Schema Validation
required columns exist
column names are standardized
output schema matches expected structure
10.2 Integrity Validation
no duplicate (date, ticker) rows remain
date parsing errors are resolved
numeric coercion completed successfully
10.3 Coverage Validation
each required instrument is present
row counts after cleaning are known
aligned common window is identified and documented
10.4 Output Validation
output files are saved successfully
datasets are sorted and reproducible
no silent substitutions occurred
11. Processing Risks
Risk	Description	PROCESS Response
Missing adjusted close	Some assets may have incomplete adjusted data	Document fallback to close if needed
Duplicate rows	Multiple fetches or concatenations may duplicate records	Remove duplicates by (date, ticker)
Partial nulls	Numeric coercion may expose hidden invalid values	Log null counts post-coercion
Unequal histories	Commodity and ETF coverage may differ	Build aligned common-window dataset
Silent drift	Ad hoc fixes may reduce reproducibility	Record rules explicitly in audit
12. Process Audit Specification

Recommended fields for process_audit.csv:

Field	Description
ticker	Asset symbol
raw_rows	Row count before cleaning
clean_rows	Row count after cleaning
rows_dropped	Number of removed rows
duplicates_removed	Duplicate count removed
null_date_removed	Rows removed for null/invalid date
null_ticker_removed	Rows removed for null ticker
null_core_price_removed	Rows removed for missing core prices
min_date_clean	Earliest clean date
max_date_clean	Latest clean date
price_field_selected	adj_close or close
notes	Processing notes

For aligned dataset summary, include:

common_start_date
common_end_date
aligned_row_count
13. Output File Plan

Recommended output structure:

energy-market-dashboard/
├─ artifacts/
│  ├─ ask.md
│  ├─ prepare.md
│  ├─ process.md
│  ├─ prepare_audit.csv
│  └─ process_audit.csv
├─ data/
│  ├─ raw/
│  └─ processed/
│     ├─ market_data_combined.csv
│     └─ market_data_aligned.csv
├─ src/
│  ├─ prepare/
│  └─ process/
14. Acceptance Criteria for PROCESS Completion

PROCESS is complete when:

raw inputs are standardized into one clean combined dataset
duplicate (date, ticker) rows are removed
date and numeric fields are validated
null-handling rules are applied consistently
aligned common-window dataset is created
process audit is generated
outputs are saved reproducibly

Only after these conditions are met should ANALYZE begin.

15. Out of Scope for PROCESS

The following are excluded from this phase:

return interpretation
leadership or market regime conclusions
dashboard layout decisions
explanatory storytelling
final recruiter-facing narrative

Those belong to ANALYZE / ACT / README layers.

16. Transition to ANALYZE

Next phase:

ANALYZE

Focus:

return calculations
normalized performance comparison
rolling volatility
drawdown
relative strength series
chart-ready summary outputs
17. PROCESS Summary

This PROCESS phase converts raw energy and benchmark market data into a controlled analytical dataset by:

standardizing schema
cleaning invalid records
handling duplicates and nulls
preserving instrument-level histories
creating a common aligned comparison base

The objective is not complexity.
The objective is a reliable analytical foundation.