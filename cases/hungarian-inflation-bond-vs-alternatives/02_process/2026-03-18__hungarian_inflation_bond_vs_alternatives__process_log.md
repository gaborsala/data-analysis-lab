# PROCESS — Cleaning & Transformation Log

Date: 2026-03-18  
Topic/Dataset: Hungarian Inflation-Linked Government Bond vs Alternative Investments  
Input snapshot: Raw dataset package profiled in PREPARE  
ASK reference: `00_ASK/2026-03-15__hungarian_inflation_bond_vs_alternatives__ask.md`

## 1. Purpose

The purpose of this stage is to document all transformations required to make the dataset reliable and analytically usable for later comparison of:

- a Hungarian inflation-linked government bond
- versus ETF-based alternative investments

This PROCESS stage specifically addressed:

- ETF null handling in `close`
- ticker coverage profiling
- validation of whether ETF nulls occur only before inception or also inside active windows
- percentage-field normalization in the bond reference file
- explicit date alignment and resampling rules for monthly analytical merges
- preservation of raw-file hashes for auditability

All transformations recorded here are explicit, justified, validated, and reproducible.

The ASK stage defined the decision threshold, risk framing, and scope boundaries before dataset interaction. :contentReference[oaicite:0]{index=0}

---

## 2. Dataset Snapshot Integrity

Before any transformation:

| File | Row count (raw) | Column count (raw) | SHA256 |
|---|---:|---:|---|
| `etf_prices_daily.csv` | 44,814 | 3 | `ed9eeb3b64a84747c843643794bd3f4b2735da8aa37b5e63bfbc6887ca1b2a0b` |
| `hungary_cpi_yoy.csv` | 184 | 2 | `518c0fbbc95d37be632f368f32433cfaba62ea2eab1d93078eedf9581f30925c` |
| `hungary_10y_yield.csv` | 325 | 2 | `0176713cc0be1ea3884b71dc20a868db867e30dbe8888ed2963b60f5c7456c98` |
| `bond_reference_template.csv` | 1 | 5 | `8d7a4ad2afb9f34ab4f87ea25382f7accb7163d2913f3d046c10cb98973d4145` |

Load errors encountered: No

These hashes anchor the raw snapshot and preserve auditability across downstream stages.

---

## 3. Transformation Summary Table

| Metric | Before | After | Change | Justification |
|---|---:|---:|---:|---|
| ETF row count | 44,814 | 41,234 | -3,580 | removed null `close` rows outside active ticker windows |
| ETF column count | 3 | 4 | +1 | added `year_month` for monthly alignment |
| ETF missing `close` count | 3,580 | 0 | -3,580 | all nulls validated as outside active valid windows |
| CPI row count | 184 | 184 | 0 | no cleaning required beyond date standardization and period key |
| CPI column count | 2 | 3 | +1 | added `year_month` for merge alignment |
| Yield row count | 325 | 325 | 0 | no cleaning required beyond date standardization and period key |
| Yield column count | 2 | 3 | +1 | added `year_month` for merge alignment |
| Bond template row count | 1 | 1 | 0 | reference table preserved |
| Bond template column count | 5 | 7 | +2 | added normalized numeric percentage-point fields |
| ETF monthly resample row count | n/a | 1,975 | n/a | month-end analytical layer created |
| Monthly merged context row count | n/a | 1,975 | n/a | structural merge for later analysis |

---

## 4. Chronological Change Log

| Step | Change | Rationale | Method (rule/code) | Validation Result |
|---|---|---|---|---|
| 1 | Reconfirmed raw hashes and shapes | preserve audit trail | snapshot summary from raw files | completed successfully |
| 2 | Built ticker-level coverage profile | identify active windows per ticker | grouped by `ticker`; computed first/last date, null/non-null counts | completed successfully |
| 3 | Classified ETF null `close` rows | distinguish structural padding from active-window data loss | compared each null row date to ticker first/last valid close dates | completed successfully |
| 4 | Removed ETF null rows outside active windows | prevent invalid return calculations | retained rows with valid close or nulls inside active window only | 3,580 rows removed |
| 5 | Verified internal active-window ETF nulls | avoid hidden data loss | counted nulls within first/last valid close range per ticker | 0 internal active-window nulls |
| 6 | Standardized date fields | enable reproducible time-series logic | parsed date columns to datetime | 0 parse failures |
| 7 | Normalized bond percent fields | support later threshold calculations | converted `premium` and `redemption_fee` strings into numeric percentage-point columns | all parses successful |
| 8 | Added `year_month` keys | support monthly structural merge | derived monthly period key from date fields | completed successfully |
| 9 | Resampled ETF daily prices to month-end | define later analytical grain explicitly | last valid close within calendar month per ticker | 1,975 monthly rows created |
| 10 | Merged monthly ETF, CPI, and yield context | prepare structural analysis table | left joined on `year_month` | completed successfully |

---

## 5. Missing Value Handling

### File: `etf_prices_daily.csv`

Observed before cleaning:

- missing `close` count: 3,580
- missing `close` percentage: 7.9886%

### Validation performed

Ticker-level null classification showed:

- `XLC`: 2,129 null rows, all **pre-inception**
- `XLRE`: 1,451 null rows, all **pre-inception**
- all other tickers: 0 null rows
- **internal active-window nulls: 0**
- **post-coverage nulls: 0**

### Handling rule applied

- No imputation performed
- Rows with null `close` outside a ticker’s active valid window were removed
- No active-window null rows required preservation or special treatment because none existed

### Result

| Metric | Value |
|---|---:|
| ETF rows before | 44,814 |
| ETF rows after | 41,234 |
| Rows removed | 3,580 |
| Missing `close` before | 3,580 |
| Missing `close` after | 0 |

### Rationale

This is a defensible structural cleaning rule because the null rows were not random gaps inside active trading history. They were pre-inception padding for later-launched sector ETFs.

### Sensitivity risk

Low to Moderate.  
The cleaning rule is structurally justified, but later analysis must still acknowledge unequal ticker inception dates.

---

## 6. Type Corrections

### Date columns

| File | Column | Original observed type | Corrected type | Why required | Validation performed |
|---|---|---|---|---|---|
| `etf_prices_daily.csv` | `Date` | string/object in raw load | datetime | time-series sorting, resampling, rolling windows | 0 parse failures |
| `hungary_cpi_yoy.csv` | `date` | string/object in raw load | datetime | monthly alignment | 0 parse failures |
| `hungary_10y_yield.csv` | `date` | string/object in raw load | datetime | monthly alignment | 0 parse failures |

### Bond reference normalization

| File | Column | Original observed type | Corrected type | Why required | Validation performed |
|---|---|---|---|---|---|
| `bond_reference_template.csv` | `premium` | string (`0.5%`) | numeric percentage points | benchmark calculations | parsed successfully |
| `bond_reference_template.csv` | `redemption_fee` | string (`1%`) | numeric percentage points | redemption cost modeling | parsed successfully |

### Added fields

- `premium_pct_points`
- `redemption_fee_pct_points`

Raw string fields were preserved; normalization was additive, not destructive.

---

## 7. Deduplication Rules

Duplicate detection logic from PREPARE was preserved.

### Candidate keys

- ETF: `(Date, ticker)`
- CPI: `date`
- Yield: `date`
- Bond template: `bond_id`

### Deduplication applied

- No row-level deduplication was required
- No full-row duplicates were detected in the raw snapshot
- No duplicate-date issues were introduced during cleaning in CPI or yield files

### Validation result

- duplicate ETF full rows: 0 in raw snapshot
- duplicate CPI dates after cleaning: 0
- duplicate yield dates after cleaning: 0

---

## 8. Outlier / Extreme Value Treatment

No outlier capping, winsorization, removal, or transformation was applied.

### Checks performed

- non-positive ETF close values after cleaning: 0
- CPI range remained unchanged and plausible
- yield range remained unchanged and plausible

### Rationale

Valid market moves, CPI spikes, and bond-yield variation should not be altered during PROCESS unless they are proven structural data errors. No such evidence was found here.

### Treatment applied

None

---

## 9. Statistical Sanity Checks

### ETF dataset

| Check | Result |
|---|---|
| rows before | 44,814 |
| rows after | 41,234 |
| rows removed | 3,580 |
| missing `close` before | 3,580 |
| missing `close` after | 0 |
| internal active-window nulls | 0 |
| non-positive `close` after | 0 |

### Ticker coverage note

Ticker coverage profiling confirmed unequal history lengths:

- `XLC` first valid close: 2018-06-19
- `XLRE` first valid close: 2015-10-08
- most other tickers begin at 2010-01-04
- all tickers share latest valid close date: 2026-03-16

### CPI and yield

| Dataset | Rows before | Rows after | Missing after | Duplicate dates after |
|---|---:|---:|---:|---:|
| CPI YoY | 184 | 184 | 0 | 0 |
| Hungary 10Y yield | 325 | 325 | 0 | 0 |

### Bond template

| Check | Result |
|---|---|
| rows before | 1 |
| rows after | 1 |
| premium parse success | 1 |
| redemption fee parse success | 1 |
| parse failures | 0 |

No unexpected variance reduction from statistical manipulation occurred. The main distributional change is removal of structurally invalid ETF rows.

---

## 10. Validation Checks

| Validation | Result |
|---|---|
| Raw hashes rechecked and preserved | Yes |
| Row counts verified after major steps | Yes |
| Date parse failures reported | Yes |
| ETF ticker-level coverage generated | Yes |
| ETF null-window classification generated | Yes |
| Internal active-window ETF nulls checked | Yes |
| Non-positive ETF close values checked | Yes |
| CPI duplicate dates checked | Yes |
| Yield duplicate dates checked | Yes |
| Bond percent parsing checked | Yes |
| Monthly resampling rule recorded | Yes |
| Monthly merge rule recorded | Yes |
| Random manual spot-check performed | Recommended, not script-evidenced |

---

## 11. Reproducibility

### Script location

`src/cases/hungarian-inflation-bond-vs-alternatives/process/`

### Script pack used

- `common_process_utils.py`
- `process_profile_ticker_coverage.py`
- `process_validate_etf_null_windows.py`
- `process_clean_datasets.py`
- `process_generate_summary.py`
- `run_process_full.py`

### Determinism

- deterministic scripted workflow: Yes
- manual spreadsheet edits: No
- raw hashes preserved: Yes
- helper logs retained in output folder: Yes

### Core generated outputs

- `etf_ticker_coverage_profile.csv`
- `etf_null_window_classification_summary.csv`
- `etf_prices_daily_clean.csv`
- `hungary_cpi_yoy_clean.csv`
- `hungary_10y_yield_clean.csv`
- `bond_reference_template_clean.csv`
- `etf_prices_month_end.csv`
- `monthly_merged_context.csv`
- `process_cleaning_overall_summary.json`
- `process_output_summary.md`

---

## 12. Explicit Resampling / Alignment Rule

### Rule used

For monthly structural analysis:

- ETF daily prices were resampled to **month-end last valid close** per ticker
- CPI YoY retained monthly frequency and was aligned by `year_month`
- Hungary 10Y yield retained monthly frequency and was aligned by `year_month`
- Merge key: `year_month`
- Join type: ETF month-end table left joined to CPI and yield

### Result

| Output | Row count | Missing CPI | Missing yield |
|---|---:|---:|---:|
| `etf_prices_month_end.csv` | 1,975 | n/a | n/a |
| `monthly_merged_context.csv` | 1,975 | 121 | 11 |

### Interpretation constraint

These missing macro-context joins are structural alignment outcomes, not yet analytical defects. Their effect must be assessed in ANALYZE before any inference about return windows is made.

---

## 13. Remaining Data Quality Issues

| Issue description | Impact on analysis | Risk level | Mitigation plan in ANALYZE |
|---|---|---|---|
| Unequal ETF inception dates across tickers | cross-ticker comparability differs by time window | Moderate | define common-window and full-history comparison views |
| Macro series do not fully cover all ETF month-end rows | some merged monthly rows lack CPI or yield context | Moderate | quantify usable overlapping windows before statistical comparisons |
| Bond template is a reference table, not an official term sheet | benchmark interpretation risk | Moderate | verify instrument rules before final decision statements |
| ETF source adjustment methodology is not yet documented | possible precision limit in long-horizon return interpretation | Moderate | disclose as limitation |
| Monthly merge is structural only | some later windows may need additional filtering | Low to Moderate | enforce explicit analytical inclusion rules |

No hidden data debt is carried forward.

---

## 14. PROCESS Gate Checklist

- [x] Raw snapshot documented
- [x] All transformations logged
- [x] Row changes justified
- [x] Validation performed and recorded
- [x] No silent filtering
- [x] No undocumented assumptions
- [x] Remaining issues acknowledged
- [x] Reproducibility confirmed
- [x] Next stage allowed: ANALYZE

---

## 15. Assumptions

- Pre-inception ETF null rows are not economically meaningful observations and may be removed safely.
- Month-end last valid close is an appropriate monthly aggregation rule for this case.
- Added numeric percentage-point columns are the correct representation for bond premium and redemption fee.
- The merged monthly context table is intended for structural alignment, not yet final analytical filtering.

---

## 16. Limitations

- This stage does not verify official legal terms of the Hungarian inflation-linked bond.
- This stage does not calculate returns, volatility, drawdowns, or threshold-exceedance probabilities.
- It does not resolve whether the ETF source uses adjusted close logic beyond observed field behavior.
- Monthly merged rows with missing CPI or yield remain present and require explicit inclusion rules in ANALYZE.
- Unequal ticker coverage remains a substantive comparability limitation even after valid cleaning.

---

## 17. Integrity Declaration

Cleaning choices do not artificially strengthen results.

No selective filtering was performed.

No undocumented transformations were applied.

All changes are reproducible.

Data integrity was preserved.