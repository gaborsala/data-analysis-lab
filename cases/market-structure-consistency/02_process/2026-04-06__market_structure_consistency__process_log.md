# PROCESS — Cleaning & Transformation Log (v1.1 Hardened)

Date: 2026-04-06  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer)  
Input snapshot:  
- Raw price files from `data/raw/*.csv`  
- Ratio panel from `cases/market-structure-consistency/outputs/02_process/historical_ratio_panel.csv`  
- Weekly classification outputs from `src/cases/market-structure-consistency/classify_weekly_structure.py`

---

## 1. Purpose

Document all transformations required to make the historical SPDR sector ETF dataset analytically usable for Market Structure consistency analysis.

This PROCESS stage covers:

- raw data ingestion
- raw data audit
- daily adjusted-close panel construction
- long-format ratio panel construction
- weekly resampling
- block-based structural classification

All changes are intended to be:

- explicit
- justified
- validated
- reproducible

No silent filtering was allowed.

---

## 2. Dataset Snapshot Integrity

### Raw input layer

**Input files:**  
12 ticker CSV files in `data/raw/`

**Tickers:**  
XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY, XLC, XLRE, SPY

**Raw row count (total):**  
45,055

**Raw schema per file:**  
- Date
- Open
- High
- Low
- Close
- Adj Close
- Volume

**Load errors encountered:**  
No

**Raw audit result:**  
`Status counts: {'ok': 12}`

### Processed daily layer

**Wide adjusted-close panel:**  
`historical_adjusted_close_wide.csv`  
Rows: 4,088  
Columns: 13

**Long ratio panel:**  
`historical_ratio_panel.csv`  
Rows: 44,968  
Columns: 5

**Coverage summary:**  
`historical_ratio_panel_coverage.csv`

### Processed weekly layer

**Weekly ratio panel:**  
`historical_weekly_ratio_panel.csv`  
Rows: 9,339

**Weekly classified panel:**  
`historical_weekly_structure_classification.csv`  
Rows: 9,339

**Weekly classification summary:**  
`historical_weekly_structure_summary.csv`

**Latest weekly snapshot:**  
`historical_weekly_structure_latest.csv`

---

## 3. Transformation Summary Table (Mandatory)

| Metric | Before | After | Change | Justification |
|---|---:|---:|---:|---|
| Raw rows | 45,055 | 4,088 | Reshaped to date-aligned wide panel | Canonical cross-ticker price panel required |
| Wide panel columns | N/A | 13 | Date + 12 ticker columns | Supports benchmark-aligned ratio construction |
| Wide rows | 4,088 | 44,968 | Expanded to long format | One row per ticker-date required |
| Long panel columns | 13 wide fields conceptually | 5 | Normalized | Standard analysis-friendly schema |
| Long rows | 44,968 | 9,339 weekly rows | Weekly resampling | Classification logic operates on weekly cadence |
| Weekly rows | 9,339 | 9,339 classified rows | Same row count retained | Classification adds state metadata without dropping rows |

No undocumented row deletion occurred.

---

## 4. Chronological Change Log

| Step | Change | Rationale | Method (rule/code) | Validation Result |
|---|---|---|---|---|
| 1 | Downloaded raw daily OHLCV files | Establish reproducible raw market-data layer | `download_raw_data.py` using yfinance | Passed |
| 2 | Audited raw files | Validate schema and file integrity before transformation | `audit_raw_data.py` | Passed (`ok`: 12) |
| 3 | Selected `Date` and `Adj Close` per ticker | Restrict to required ratio-construction fields | Explicit column subset | Passed |
| 4 | Parsed dates and validated duplicate-free ticker-date keys | Preserve time-series integrity | Date coercion + duplicate check | Passed |
| 5 | Renamed adjusted-close field to ticker symbol | Build mergeable cross-ticker panel | Explicit rename rule | Passed |
| 6 | Outer-merged all tickers on `Date` | Preserve full valid history across different ETF start dates | Sequential outer merge | Passed |
| 7 | Saved wide adjusted-close panel | Freeze canonical intermediate output | CSV export | Passed |
| 8 | Melted sector columns into long format | Create ticker-date analysis panel | `melt()` excluding SPY as sector | Passed |
| 9 | Computed `ratio_value = adj_close / spy_adj_close` | Create core relative-strength measure | Deterministic arithmetic | Passed |
| 10 | Generated coverage summary | Document actual ticker coverage windows | Grouped summary using non-null `adj_close` dates | Passed after patch |
| 11 | Resampled ratio panel to weekly frequency (`W-FRI`) | Align analytical cadence with structure logic | Per-ticker `.resample("W-FRI").last()` | Passed |
| 12 | Added block-based weekly structure classification | Derive structural state from relative-strength behavior | Compare current 4-week block vs prior 4-week block | Passed |
| 13 | Generated classification summary and latest snapshot | Support downstream analysis and QA | Aggregation + latest-row extraction | Passed |

---

## 5. Missing Value Handling

### Raw layer

No raw-file structural failures were detected.

### Long ratio panel

Structural nulls were preserved rather than dropped.

#### Reason
Some ETFs have later inception dates:

- XLC starts: 2018-06-19
- XLRE starts: 2015-10-08

#### Coverage summary

| Ticker | Row Count | Non-null `adj_close` | Non-null `spy_adj_close` | Non-null `ratio_value` | Min Date | Max Date |
|---|---:|---:|---:|---:|---|---|
| XLB | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLE | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLF | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLI | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLK | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLP | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLU | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLV | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLY | 4,088 | 4,088 | 4,088 | 4,088 | 2010-01-04 | 2026-04-06 |
| XLC | 4,088 | 1,959 | 4,088 | 1,959 | 2018-06-19 | 2026-04-06 |
| XLRE | 4,088 | 2,637 | 4,088 | 2,637 | 2015-10-08 | 2026-04-06 |

### Weekly classified panel

Weekly classification preserved rows with missing ratio history by labeling them explicitly:

- `NO_RATIO`: 741 rows
- `INSUFFICIENT_HISTORY`: 77 rows

### Handling rule

- No imputation was applied
- No pre-inception periods were force-filled
- No rows were dropped to create artificial overlap

This preserves both:

- full-history per-ticker analysis
- future common-window comparison if needed

---

## 6. Type Corrections

| Column | Original Observed Type | Corrected Type | Why Required | Risk if Misclassified | Validation Performed |
|---|---|---|---|---|---|
| Date | object/string | datetime64[ns] | Required for merge, resample, ordering | Broken joins and weekly logic | Date parsing checks |
| Adj Close | numeric-like/object | float | Required for ratio calculation | Arithmetic failure | Numeric coercion and positivity checks |
| SPY adjusted close | numeric-like/object | float | Required as benchmark denominator | Invalid ratios | Numeric validation inherited from raw build |
| ratio_value | derived numeric | float | Core relative-strength measure | Invalid classification input | Deterministic derivation |
| ticker | string | string | Required for grouping | Grouping errors | Controlled ticker set |
| direction | derived text | string/category-like | Required for state analysis | Transition misclassification | Controlled assignment logic |
| classification_ready | derived boolean | bool | Indicates analyzable state rows | Wrong inclusion in analysis | Explicit logical flag |

Type changes were explicit and reproducible.

---

## 7. Deduplication Rules

**Duplicate detection logic:**  
Duplicate ticker-date checks were performed before panel construction.

**Criteria for removal:**  
No deduplication was required because the scripts were designed to fail on duplicate ticker-date rows.

**Rows removed:**  
0

**Validation of uniqueness after removal:**  
Passed implicitly through build validation and successful panel creation.

No deduplication without rule transparency. No deduplication occurred.

---

## 8. Outlier / Extreme Value Treatment

**Detection method:**  
Basic validity checks only:
- non-positive adjusted-close values rejected
- invalid dates rejected
- invalid duplicate dates rejected

**Treatment applied:**  
None

**Justification:**  
This PROCESS stage constructs the panel and state labels. It does not censor valid market extremes or optimize distributions.

**Sensitivity analysis performed:**  
No

No outlier treatment was used to strengthen results artificially.

---

## 9. Statistical Sanity Checks

| Check | Result | Notes |
|---|---|---|
| Raw file audit | Passed | 12/12 files structurally valid |
| Wide panel row count | 4,088 | Matches expected shared historical date backbone |
| Long panel row count | 44,968 | Equals 4,088 dates × 11 sector tickers |
| Weekly panel row count | 9,339 | Weekly resample completed without structural failure |
| Classified row count | 9,339 | Classification retained all weekly rows |
| Distinct sector tickers | 11 | SPY excluded from sector classification by design |
| Null ratio values | 3,580 in daily long panel | Consistent with XLC/XLRE inception timing |
| Direction counts | `LH/LL`: 3,516; `HH/HL`: 3,222; `TRANSITION`: 1,783; `NO_RATIO`: 741; `INSUFFICIENT_HISTORY`: 77 | Plausible distribution; requires later analytical interpretation |
| Classification-ready rows | 8,521 | Weekly rows with sufficient valid history |

No unexpected structural failure was detected in the generated outputs.

---

## 10. Validation Checks

**Row counts verified after each major step:**  
Yes

**Range checks performed:**  
Yes
- adjusted close values must be numeric
- adjusted close values must be positive
- date values must parse successfully
- ratio values derive only from aligned sector and SPY prices

**Constraint validation:**  
Yes
- all expected raw files present
- required columns present
- no duplicate ticker-date rows
- benchmark SPY present in ratio construction
- weekly classification retains ticker/date integrity

**Referential integrity checks:**  
Yes
- `ratio_value` requires aligned `adj_close` and `spy_adj_close`
- classification is generated only from ticker-consistent weekly series

**Random manual spot-check performed:**  
Recommended but not yet formally logged

### Classification-specific validation

- Weekly rule used: `W-FRI`
- Block length used: 4 weeks
- State definition:
  - `HH/HL`: current block high > prior block high and current block low > prior block low
  - `LH/LL`: current block high < prior block high and current block low < prior block low
  - `TRANSITION`: all other classification-ready states
  - `NO_RATIO`: no weekly ratio available
  - `INSUFFICIENT_HISTORY`: valid ratio exists but not enough history for two comparison blocks

---

## 11. Reproducibility

**Script locations:**  
- `src/cases/market-structure-consistency/download_raw_data.py`
- `src/cases/market-structure-consistency/audit_raw_data.py`
- `src/cases/market-structure-consistency/build_ratio_panel.py`
- `src/cases/market-structure-consistency/classify_weekly_structure.py`

**Version reference:**  
Git commit hash not yet recorded

**Deterministic steps confirmed:**  
Yes

**Manual steps performed:**  
No manual data edits documented

### Reproducibility status

The process is reproducible provided that:

- the same ticker universe is used
- the same raw source remains available
- the same scripts are run from the repo root
- the same weekly rule and block size are retained

---

## 12. Remaining Data Quality Issues

| Issue description | Impact on analysis | Risk level | Mitigation plan in ANALYZE |
|---|---|---|---|
| XLC shorter history | Weakens direct full-period cross-sector comparability | Moderate | Report full-history and common-window views separately |
| XLRE shorter history | Weakens direct full-period cross-sector comparability | Moderate | Report full-history and common-window views separately |
| No SHA256 file hashes recorded | Weakens strict audit trail | Low | Add hash manifest in next version |
| Manual spot-check not yet logged | Reduces manual validation evidence | Low | Add 5–10 row spot-check note |
| Block-based classification is a design assumption | Findings depend on this window definition | Moderate | State explicitly and test sensitivity later if needed |

---

## 13. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Adjusted close is appropriate for ratio construction | Standard benchmark-relative comparison input | Relative-strength behavior may differ from alternative price fields | Compare against close-price version if needed |
| Weekly `W-FRI` resampling is appropriate | Aligns with brief-style weekly structure workflow | Different weekly anchor may alter edge cases | Sensitivity test with alternate weekly anchor |
| 4-week vs prior 4-week block is a valid structural lens | Needed for deterministic classification | State counts may be window-sensitive | Sensitivity test with other block lengths |
| Preserving structural nulls is preferable to truncation | Avoids silent data loss | Full-history comparisons may be harder to summarize | Add common-window companion analysis |

---

## 14. Limitations

- This PROCESS stage does not yet compute persistence metrics or transition matrices.
- XLC and XLRE have materially shorter histories than the older sector ETFs.
- Manual validation is recommended but not yet formally documented.
- No common-window classification dataset has been created yet.
- File-level hashing has not been added.
- Classification logic is deterministic but window-dependent.

---

## 15. PROCESS Gate Checklist

- [x] Raw snapshot documented
- [x] All transformations logged
- [x] Row changes justified
- [x] Validation performed and recorded
- [x] No silent filtering
- [x] No undocumented assumptions
- [x] Remaining issues acknowledged
- [x] Reproducibility confirmed at script level
- [x] Next stage allowed (ANALYZE)

---

## 16. Integrity Declaration

- Cleaning and transformation choices did not artificially strengthen results
- No selective filtering was performed
- No undocumented transformations were applied
- All executed changes are reproducible at the script level
- Uncertainty and remaining constraints are explicitly acknowledged