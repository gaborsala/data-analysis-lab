# PREPARE — Dataset Understanding (v1.1 Hardened)

Date: 2026-04-06  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer)  
Source: SPDR Sector ETF daily adjusted price data (via yfinance), processed into a ratio panel relative to SPY  
Time range: 2010-01-04 to 2026-04-06 (ticker-specific coverage varies)  
Rows/Cols:  
- Wide panel: 4,088 rows × 13 columns  
- Long panel: 44,968 rows × 5 columns  

---

## 1. Context

This dataset exists to evaluate the historical consistency of a deterministic Market Structure classification system.

The real-world process:

1. Daily adjusted prices for SPDR sector ETFs and SPY are collected.
2. Data is aligned on a common date index.
3. Relative-strength ratios vs SPY are computed.
4. The resulting panel will later be used for structural classification and consistency analysis.

Decision context (from ASK):

- Determine whether the Market Structure system produces stable and consistent structural signals over time.
- Determine whether additional validation layers are required before relying on outputs for analytical decision support.

No interpretation of performance or outcomes is included.

---

## 2. Grain / Unit of Analysis

**One row represents:**  
One ticker on one calendar date.

**Expected unique identifier:**  
`ticker + date`

**Potential primary key:**  
`ticker + date`

**Aggregation level:**  
Daily (derived from daily price data)

**Is grain consistent across dataset?**  
Yes, at the dataset level.  
However, coverage differs by ticker due to ETF inception dates.

---

## 3. Schema

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| date | datetime | datetime64[ns] | Observation date | Valid trading dates | No | Derived from raw Date column |
| ticker | string | string | Sector ETF identifier | Canonical SPDR set | No | Excludes SPY in long panel |
| adj_close | float | float | ETF adjusted close price | > 0 | Yes | Null before ETF inception |
| spy_adj_close | float | float | SPY adjusted close price | > 0 | No | Benchmark series |
| ratio_value | float | float | Relative strength vs SPY | > 0 | Yes | Null where adj_close is null |

### Notes

- Schema reflects processed ratio panel (`historical_ratio_panel.csv`)
- No corrections are performed in PREPARE
- Observed types reflect actual loaded dataset

---

## 4. Missingness Overview

**Overall missing %:**  
Driven by ETF inception gaps (structural missingness)

**Columns with missing values:**  
- `adj_close`
- `ratio_value`

**Missingness pattern:**  
Structural (due to ETF inception timing)

**Coverage summary (non-null ratio values):**

| Ticker | Non-null ratio_value | Total rows | Missing % |
|---|---:|---:|---:|
| XLB | 4,088 | 4,088 | 0.0% |
| XLE | 4,088 | 4,088 | 0.0% |
| XLF | 4,088 | 4,088 | 0.0% |
| XLI | 4,088 | 4,088 | 0.0% |
| XLK | 4,088 | 4,088 | 0.0% |
| XLP | 4,088 | 4,088 | 0.0% |
| XLU | 4,088 | 4,088 | 0.0% |
| XLV | 4,088 | 4,088 | 0.0% |
| XLY | 4,088 | 4,088 | 0.0% |
| XLC | 1,959 | 4,088 | 52.08% |
| XLRE | 2,637 | 4,088 | 35.49% |

**Potential analytical bias risk:**

- Cross-sector comparisons over full history may be biased by unequal coverage
- Later-inception ETFs may appear less stable if not handled properly

**Columns with >5% missingness:**
- XLC (`ratio_value`)
- XLRE (`ratio_value`)

No imputation or correction is applied.

---

## 5. Anomaly Scan (No Edits Performed)

**Duplicate rows detected:**  
None detected in raw audit

**Out-of-range values:**  
No non-positive adjusted close values detected (validated in build script)

**Timestamp inconsistencies:**  
None detected; all dates parsed successfully

**Unexpected categories:**  
Not applicable (no categorical fields in this dataset stage)

**Extreme values:**  
Not evaluated in PREPARE

**Structural inconsistencies:**  
None observed at schema level

---

## 6. Data Credibility Assessment

**Source reliability:**  
Moderate to High  
- Based on widely used market data provider (yfinance)

**Collection method:**  
Automated (script-based ingestion)

**Known distortions:**
- ETF inception-date differences
- Potential provider-specific adjustments
- Market holidays and non-trading days

**Data freshness:**  
Up to 2026-04-06 (latest available date)

**Trust level:**  
Moderate  

**Justification:**
- Automated pipeline increases reproducibility
- External data source introduces dependency risk
- Structural integrity validated via audit script

---

## 7. Risks / Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Adjusted close is appropriate for ratio construction | Standard practice for total-return comparability | Ratio distortions if adjustments incorrect | Compare with raw close or alternative sources |
| SPY is consistent benchmark across full period | Required for relative comparison | Benchmark inconsistency invalidates ratios | Validate SPY coverage and continuity |
| Outer merge preserves full valid history | Ensures no silent data loss | May introduce structural nulls that affect analysis | Coverage summary and null distribution checks |
| No duplicate dates per ticker | Required for time-series integrity | Duplicate records distort duration metrics | Duplicate check in raw audit |
| Ratio calculation is numerically stable | Simple division operation | Division errors if SPY data invalid | Validate non-null and positive SPY values |

---

## 8. Refined Analytical Questions

1. What is the distribution of structural state duration across sectors?
2. How frequently do structural states transition between categories?
3. How does recent structural behavior compare to historical patterns?
4. Do sectors exhibit materially different persistence characteristics?
5. How does unequal data coverage affect structural consistency metrics?

No directional or interpretive language is introduced.

---

## 9. Interpretation Guardrail (Mandatory)

The following are prohibited in PREPARE:

- “This suggests…”
- “This implies…”
- “This shows that…”
- Performance comparisons
- Causal statements
- Predictive statements

Allowed:

- Structural observations
- Missingness documentation
- Data integrity notes

No interpretive language is present.

---

## 10. Validation Checks Performed

**Row count confirmed:**  
Yes  
- Wide: 4,088 rows  
- Long: 44,968 rows  

**Column count confirmed:**  
Yes  
- Wide: 13 columns  
- Long: 5 columns  

**Schema matches expectations:**  
Yes

**Random row spot-check performed:**  
Recommended; not yet formally documented

**Data load errors encountered:**  
No

### Additional validation checks performed

- Raw data audit: all 12 files status = ok
- Required columns present in all files
- Date parsing successful
- No duplicate dates per ticker
- Positive adjusted-close values enforced

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

## 12. Limitations

- Coverage varies across tickers due to ETF inception dates
- Dataset does not include structural classification yet
- No common-date subset has been defined yet
- External data provider may introduce inconsistencies not visible in this stage
- Manual validation (spot-check) is not yet formally recorded

---

## 13. Integrity Declaration

- No data transformation performed in this stage
- No assumptions hidden
- No performance interpretation introduced
- Observations limited to structural dataset properties