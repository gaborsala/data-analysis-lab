# PREPARE — Energy Market Dashboard

Date: 2026-04-05  
Topic/Dataset: energy-market-dashboard  
Source: Yahoo Finance raw fetch via `yfinance`  
Time range: 2021-04-05 to 2026-04-02  
Rows/Cols: 6,288 rows across 5 raw files; each file has 8 columns

## 1. Context

This dataset exists to support a local analytical dashboard that monitors energy-market-linked instruments and compares commodity behavior with sector and market benchmarks.

The real-world process generating the data is market trading activity captured as daily OHLCV price records for selected tradable instruments.

This dataset supports the ASK-stage decision context: define a disciplined, portfolio-ready dashboard that tracks energy market structure using reproducible daily market data without forecasting or causal overclaiming.

No interpretation of performance or outcomes is introduced in this stage.

## 2. Grain / Unit of Analysis

**One row represents:**  
One instrument on one trading date.

**Expected unique identifier:**  
`date + ticker`

**Potential primary key:**  
Composite key: `date`, `ticker`

**Aggregation level:**  
Daily market observations

**Is grain consistent across dataset?**  
Yes. All five raw files use daily instrument-level observations.

## 3. Schema

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| date | string-formatted date in raw CSV | datetime | Trading date | Valid market dates | No | Needs parsing in PROCESS |
| adj_close | numeric | float | Adjusted close | >= 0 | No | Present in all five files |
| close | numeric | float | Session close price | >= 0 | No | Present in all five files |
| high | numeric | float | Session high price | >= low | No | Range check passed in raw scan |
| low | numeric | float | Session low price | >= 0 | No | Range check passed in raw scan |
| open | numeric | float | Session open price | >= 0 | No | Present in all five files |
| volume | numeric | float/int | Traded volume | >= 0 | No | Present in all five files |
| ticker | string | string | Instrument identifier | Fixed whitelist | No | One unique ticker per file |

**Observed file-level schema consistency:**  
All five raw files share the same 8-column schema:

- `date`
- `adj_close`
- `close`
- `high`
- `low`
- `open`
- `volume`
- `ticker`

No corrections are performed in PREPARE.

## 4. Missingness Overview

**Overall missing %:**  
0.0%

**Columns with missing values:**  
None

**Missingness pattern (MCAR / MAR / Structural / Unknown):**  
No missingness detected in the uploaded raw files.

**Potential analytical bias risk:**  
Missingness risk is low in the current raw snapshot. The larger analytical risk is date alignment across instruments rather than null completeness.

**Columns with >5% missingness (if any):**  
None

No imputation or correction is allowed in this stage.

## 5. Anomaly Scan (No Edits Performed)

**Duplicate rows detected:**  
0 duplicate full rows in every file

**Duplicate `date` rows within file:**  
0 in every file

**Out-of-range values:**  
No negative values detected in:
- `open`
- `high`
- `low`
- `close`
- `adj_close`
- `volume`

**Timestamp inconsistencies:**  
No file-level date duplication detected. Date coverage differs slightly by instrument count, which is expected in cross-market datasets.

**Unexpected categories:**  
No unexpected tickers detected. Observed tickers:

- `CL=F` (WTI)
- `BZ=F` (Brent)
- `NG=F` (Natural Gas)
- `XLE`
- `SPY`

**Extreme values (initial distribution scan):**  
Not formally profiled in PREPARE. This should be handled in PROCESS/ANALYZE.

**Structural inconsistencies:**  
No `high < low` cases detected in any file.

**Observed file sizes and date ranges:**

| File | Ticker | Rows | Cols | Min Date | Max Date |
|---|---|---:|---:|---|---|
| `wti_raw.csv` | `CL=F` | 1,258 | 8 | 2021-04-05 | 2026-04-02 |
| `brent_raw.csv` | `BZ=F` | 1,259 | 8 | 2021-04-05 | 2026-04-02 |
| `natgas_raw.csv` | `NG=F` | 1,259 | 8 | 2021-04-05 | 2026-04-02 |
| `xle_raw.csv` | `XLE` | 1,256 | 8 | 2021-04-05 | 2026-04-02 |
| `spy_raw.csv` | `SPY` | 1,256 | 8 | 2021-04-05 | 2026-04-02 |

**Common overlapping date window across all five instruments:**  
2021-04-05 to 2026-04-02

**Common intersected trading dates across all five instruments:**  
1,256 dates

Document only. No corrections performed.

## 6. Data Credibility Assessment

**Source reliability:**  
Moderate to high for exploratory financial analysis and dashboard prototyping.

**Collection method:**  
Automated fetch via `yfinance`.

**Known distortions:**  
Potential source-specific differences in exchange calendars, futures contract handling, and adjusted price methodology.

**Data freshness:**  
Recent daily snapshot ending 2026-04-02.

**Trust level:**  
Moderate

**Justification:**  
The raw files are structurally complete and internally consistent for dashboard development, but source methodology and cross-asset comparability still require careful handling in PROCESS.

## 7. Risks / Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| `date + ticker` is a stable key | No duplicate dates detected within each file | Unioned dataset could still create duplication if bad merges occur later | Re-check after concatenation in PROCESS |
| Common-date intersection is the correct comparison base | Multi-asset dashboard comparisons require aligned dates | Non-overlap handling may affect chart logic and summary metrics | Build aligned dataset and compare row counts |
| `adj_close` is usable across all five instruments | Column is present and non-null in all files | Futures adjustment logic may differ from ETF adjustment logic | Compare `close` vs `adj_close` behavior by ticker in PROCESS |
| Slight row-count differences are calendar-related rather than data corruption | Futures and ETFs can have different trading calendars | Misaligned dates could distort rolling metrics if not normalized | Inspect unmatched dates after concatenation |
| Raw snapshot reflects successful full fetch | All five files were uploaded and readable | Local fetch environment may still differ later | Re-run fetch deterministically and compare outputs |

Assumptions must remain testable in PROCESS or ANALYZE.

## 8. Refined Analytical Questions

Derived strictly from ASK:

1. What is the correct aligned daily comparison window across WTI, Brent, Natural Gas, XLE, and SPY?
2. Which processed price field should be used consistently for dashboard metrics: `close` or `adj_close`?
3. What structural dashboard views are supportable from the cleaned aligned panel: normalized performance, relative strength, rolling volatility, and drawdown?
4. How much information is lost when enforcing a common-date intersection versus retaining each instrument’s full daily history?

These questions refine scope without answering them.

## 9. Interpretation Guardrail (Mandatory)

The following are prohibited in PREPARE:

- “This suggests…”
- “This implies…”
- “This shows that…”
- performance comparisons
- causal statements
- predictive statements

Allowed:

- structural observations
- distribution description
- missingness documentation
- data integrity notes

If interpretive language appears, PREPARE is invalid.

## 10. Validation Checks Performed

**Row count confirmed:**  
Yes

**Column count confirmed:**  
Yes

**Schema matches source documentation (Yes/No):**  
Yes at the raw-file level

**Random row spot-check performed (Yes/No):**  
Not formally documented

**Data load errors encountered (Yes/No):**  
Yes during initial fetch due to tuple-style column handling in `yfinance`; fetch script was patched and the final raw export completed successfully

**Additional validation checks performed:**

- confirmed all five expected raw files are present
- confirmed each file contains exactly one ticker value
- confirmed no missing values in any file
- confirmed no duplicate full rows
- confirmed no duplicate dates within file
- confirmed no negative numeric values in core numeric fields
- confirmed no `high < low` anomalies
- confirmed common date intersection across all five instruments

## 11. PREPARE Gate Checklist

- [x] Dataset identity documented
- [x] Grain clearly defined
- [x] Schema documented
- [x] Missingness analyzed
- [x] Anomalies recorded
- [x] Risks documented
- [x] No transformations performed
- [x] No interpretive language present
- [x] Next stage allowed (PROCESS)

## 12. Integrity Declaration

- No data transformation performed
- No assumptions hidden
- No performance interpretation introduced
- Observations limited to structural properties
- PREPARE completed from observed raw-file properties, not planned checks