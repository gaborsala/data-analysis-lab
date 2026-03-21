# PREPARE — Dataset Understanding

Date: 2026-03-11  
Topic/Dataset: SPDR Sector ETFs  
Source: ZIP archive provided by user (`SPDR_SECTOR_ETFS.zip`) containing one combined dataset (`all_sectors.csv`) and 11 per-ticker CSV files under `individual_data/`  
Time range: 1998-12-22 to 2024-06-24  
Rows/Cols: 61,448 rows / 8 columns

---

## 1. Context

This dataset appears to exist to provide historical daily OHLCV market data for the SPDR sector ETF universe in a format suitable for cross-sector comparison.

The real-world process represented is daily market trading for sector ETFs, recorded as end-of-day price/volume observations and exported into CSV format.

This dataset relates directly to the ASK-stage decision context:

- compare sector return distributions
- compare volatility structure
- assess whether sector allocation differences are analytically defensible using historical evidence

No performance interpretation is introduced in this stage.

---

## 2. Grain / Unit of Analysis

**One row represents:**  
One ETF on one trading date, with daily open, high, low, close, and volume fields.

**Expected unique identifier:**  
`ticker + date`

**Potential primary key:**  
Composite key: `ticker`, `date`

**Aggregation level:**  
Daily market data

**Is grain consistent across dataset?**  
Yes, at row level.  
However, history length is not uniform across ETFs because some sector ETFs begin later than others:

- Legacy sector funds begin on 1998-12-22
- XLRE begins on 2015-10-08
- XLC begins on 2018-06-19

This is a structural comparability issue, not a grain inconsistency.

---

## 3. Schema

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| ticker | object | string / categorical | ETF ticker symbol | Known SPDR sector tickers | No | 11 unique values observed |
| sector | object | string / categorical | Sector label mapped to ticker | Valid sector names | No | One sector per ticker observed |
| date | object | date | Trading date | 1998-12-22 to 2024-06-24 in raw file | No | Parses cleanly to datetime |
| open | float64 | numeric | Opening price | > 0 | No | No negative or zero values |
| high | float64 | numeric | Daily high price | >= low and > 0 | No | Internally consistent in raw scan |
| low | float64 | numeric | Daily low price | > 0 and <= high | No | Internally consistent in raw scan |
| close | float64 | numeric | Closing price | > 0 | No | No negative or zero values |
| volume | int64 | integer | Daily traded share volume | >= 0 | No | 6 zero-volume rows observed |

**Notes:**

- Observed types reflect the raw dataset as loaded.
- No corrections are performed in PREPARE.
- The combined file includes sector labels; the per-ticker files omit the `sector` column and contain 7 columns instead of 8.

---

## 4. Missingness Overview

**Overall missing %:**  
0.00%

**Columns with missing values:**  
None

**Missingness pattern (MCAR / MAR / Structural / Unknown):**  
No explicit missing values observed in the combined dataset.

**Potential analytical bias risk:**  
Low from null-missingness perspective.  
Higher risk comes from unequal ETF inception dates rather than null fields.

**Columns with >5% missingness:**  
None

**Additional structural note:**  
Absence of observations before fund launch dates for XLC and XLRE should be treated as structural non-coverage, not standard missingness.

No imputation or correction is performed here.

---

## 5. Anomaly Scan (No Edits Performed)

**Duplicate rows detected:**  
- Full-row duplicates: 0
- Duplicate composite keys (`ticker`, `date`): 0

**Out-of-range values:**  
- Negative `open/high/low/close`: 0
- Negative `volume`: 0
- Zero `open/high/low/close`: 0
- Zero `volume`: 6 rows

**Timestamp inconsistencies:**  
- Date parse failures: 0
- Weekend-dated rows: 0

**Unexpected categories:**  
No unexpected ticker inflation detected.  
11 unique tickers and 11 unique sectors observed.

Observed tickers:
`XLB, XLC, XLE, XLF, XLI, XLK, XLP, XLRE, XLU, XLV, XLY`

**Extreme values (initial distribution scan):**
- Price fields remain positive throughout
- Volume ranges from 0 to 1,050,592,000
- Large volume outliers are present, but this stage does not classify them as erroneous

**Structural inconsistencies:**
- Unequal historical coverage across ETFs
- Combined file has 8 columns; per-ticker files have 7 columns because `sector` is omitted there
- 6 zero-volume rows exist; these require later validation but are not altered here
- Some zero-volume rows also show identical OHLC values, which may represent non-trading or source-specific handling rather than a confirmed error

**OHLC integrity checks (raw scan):**
- `high < open`: 0
- `high < close`: 0
- `low > open`: 0
- `low > close`: 0
- `high < low`: 0

Documented only. No correction performed.

---

## 6. Data Credibility Assessment

**Source reliability:**  
Moderate. The dataset is structurally coherent and internally consistent, but original vendor/source metadata is not embedded in the ZIP.

**Collection method (manual / automated / derived):**  
Likely automated export from a market-data source or scripted download pipeline.

**Known distortions:**  
- Possible use of adjusted or vendor-normalized price history cannot be confirmed from metadata alone
- ETF launch timing differs materially across sector funds
- Exchange holidays are not explicitly documented
- Zero-volume rows require downstream review

**Data freshness:**  
Latest observed date is 2024-06-24.

**Trust level:**  
Moderate to High

**Justification:**  
- no explicit missing values
- no duplicate keys
- date field parses cleanly
- OHLC consistency is intact
- sector-to-ticker mapping is stable

Confidence is reduced slightly by missing source provenance and unequal start dates.

---

## 7. Risks / Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| `ticker + date` is the correct primary key | One row appears to represent one ETF-day observation | Duplicate or conflicting records could distort return calculations | Uniqueness validation in PROCESS |
| Price fields are on a comparable basis across ETFs | Cross-sector analysis requires consistent price construction | Return and volatility comparisons may be biased if some series are adjusted and others are not | Source-method review and cross-file consistency checks in PROCESS |
| Zero-volume rows are rare structural edge cases, not widespread corruption | Only 6 rows observed with zero volume | Return series or event handling may be biased around those dates | Row-level inspection in PROCESS |
| Sector labels are correctly mapped to tickers | Each ticker maps to one sector in raw scan | Cross-sector grouping would be invalid if mapping is wrong | Validate one-to-one mapping in PROCESS |
| Later ETF start dates reflect true fund inception, not missing extraction | XLC and XLRE begin much later than legacy funds | Time-window comparisons could be distorted if interpreted incorrectly | Confirm launch-bound structural coverage in PROCESS / ANALYZE |
| Daily rows represent trading days only | No weekend rows observed | Frequency assumptions would be wrong if dates include non-trading placeholders | Trading-calendar consistency checks in PROCESS |

All assumptions remain testable.

---

## 8. Refined Analytical Questions

Derived strictly from ASK:

1. Over what common historical window can all 11 sector ETFs be compared without introducing unequal-history bias?
2. How does the analysis change when using:
   - full available history per ETF
   - common-window history across all ETFs
3. Are return-distribution and volatility comparisons stable across sectors once structural start-date differences are controlled?
4. Do rare zero-volume observations materially affect downstream return or volatility metrics?
5. Is the combined dataset sufficient as the canonical input, or should per-ticker files be treated only as reference/supporting extracts?

No directional or performance claims are made here.

---

## 9. Interpretation Guardrail (Mandatory)

The following are prohibited in PREPARE and are not used in this artifact:

- “This suggests…”
- “This implies…”
- “This shows that…”
- Performance comparisons
- Causal statements
- Predictive statements

Allowed content in this stage is limited to:

- structural observations
- schema documentation
- missingness documentation
- anomaly recording
- data integrity notes

This artifact remains within those boundaries.

---

## 10. Validation Checks Performed

| Check | Result |
|---|---|
| Row count confirmed | Yes — 61,448 |
| Column count confirmed | Yes — 8 in combined file |
| ZIP contents reviewed | Yes — 12 files total |
| Schema matches raw file load | Yes |
| Date parse check performed | Yes — 0 failures |
| Missing-value scan performed | Yes — no nulls found |
| Duplicate-key scan performed | Yes — 0 duplicate (`ticker`, `date`) rows |
| Weekend-date scan performed | Yes — 0 weekend rows |
| Basic OHLC rule validation performed | Yes — no raw rule breaks found |
| Random row spot-check performed | Yes |
| Data load errors encountered | No |

**Recommended additional validations for PROCESS:**

- verify whether prices are adjusted or unadjusted
- inspect all 6 zero-volume rows individually
- confirm one-to-one `ticker -> sector` mapping
- define canonical comparison window for all-sector analysis
- verify combined file against per-ticker files for row-count agreement

---

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

---

## 12. Assumptions

1. The combined dataset `all_sectors.csv` is the primary working file for lifecycle analysis.
2. Per-ticker files are supporting extracts unless reconciliation reveals conflicts.
3. Structural absence before ETF launch dates should not be treated as ordinary missing data.
4. The ASK artifact is sufficient to proceed into PREPARE because the business question, scope, and success criteria are already defined.

---

## 13. Limitations

1. Original data vendor/source is not explicitly identified inside the ZIP archive.
2. No metadata confirms whether price fields are adjusted for splits/dividends.
3. Trading-calendar completeness cannot be fully verified in PREPARE without a benchmark calendar.
4. This stage does not test return calculations, statistical properties, or modeling assumptions.
5. Zero-volume rows are recorded but not yet adjudicated as valid market records versus source artifacts.

---

## 14. Integrity Declaration

- No data transformation performed
- No hidden assumptions introduced
- No performance interpretation introduced
- Observations limited to structural properties