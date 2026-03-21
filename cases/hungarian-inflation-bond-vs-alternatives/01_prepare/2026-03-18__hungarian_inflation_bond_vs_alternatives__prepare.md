# PREPARE — Dataset Understanding

Date: 2026-03-18  
Topic/Dataset: Hungarian Inflation-Linked Government Bond vs Alternative Investments  
Source: User-provided raw dataset package and ASK artifact  
ASK reference: `00_ASK/2026-03-15__hungarian_inflation_bond_vs_alternatives__ask.md`

## 1. Context

This PREPARE stage documents the structure, coverage, and initial integrity of the collected dataset package for the decision defined in ASK:

- retain a Hungarian inflation-linked bond
- or redeem early with a 1% fee
- and compare that decision against alternative investments such as ETFs or equities

The uploaded ASK is decision-specific, measurable, and stage-valid for a full lifecycle case. It defines the return threshold, decision context, assumptions, and scope boundaries clearly enough to justify PREPARE. :contentReference[oaicite:0]{index=0}

The raw dataset package contains four analytical inputs:

- `etf_prices_daily.csv`
- `hungary_cpi_yoy.csv`
- `hungary_10y_yield.csv`
- `bond_reference_template.csv`

Based on the generated PREPARE outputs, all four files were loadable, all expected candidate keys were structurally valid, and metadata files were present for all datasets. The main data quality issue detected in PREPARE is non-trivial missingness in the ETF close-price field. No transformation or interpretation is introduced at this stage.

---

## 2. Grain / Unit of Analysis

| File | One row represents | Expected unique identifier | Potential primary key | Aggregation level | Grain consistent? |
|---|---|---|---|---|---|
| `etf_prices_daily.csv` | one ETF ticker on one trading date | `Date + ticker` | `(Date, ticker)` | daily | Yes |
| `hungary_cpi_yoy.csv` | one CPI YoY observation on one date | `date` | `date` | monthly | Yes |
| `hungary_10y_yield.csv` | one Hungary 10Y yield observation on one date | `date` | `date` | monthly | Yes |
| `bond_reference_template.csv` | one bond specification record | `bond_id` | `bond_id` | static reference | Yes |

### Notes

- ETF data is the highest-frequency source and is expected to drive return-series construction later.
- CPI and 10Y yield are lower-frequency macro series and will require explicit frequency alignment in PROCESS.
- The bond reference file is a parameter table, not a historical series.

---

## 3. Dataset Inventory

| File | Rows | Columns | Full-row duplicates | Candidate key valid? | Metadata found? |
|---|---:|---:|---:|---|---|
| `etf_prices_daily.csv` | 44,814 | 3 | 0 | Yes | Yes |
| `hungary_cpi_yoy.csv` | 184 | 2 | 0 | Yes | Yes |
| `hungary_10y_yield.csv` | 325 | 2 | 0 | Yes | Yes |
| `bond_reference_template.csv` | 1 | 5 | 0 | Yes | Yes |

### File hash snapshot

| File | SHA256 |
|---|---|
| `etf_prices_daily.csv` | `ed9eeb3b64a84747c843643794bd3f4b2735da8aa37b5e63bfbc6887ca1b2a0b` |
| `hungary_cpi_yoy.csv` | `518c0fbbc95d37be632f368f32433cfaba62ea2eab1d93078eedf9581f30925c` |
| `hungary_10y_yield.csv` | `0176713cc0be1ea3884b71dc20a868db867e30dbe8888ed2963b60f5c7456c98` |
| `bond_reference_template.csv` | `8d7a4ad2afb9f34ab4f87ea25382f7accb7163d2913f3d046c10cb98973d4145` |

---

## 4. Schema

### `etf_prices_daily.csv`

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| `Date` | `datetime64[us]` | datetime | trading date | valid trading dates | No | parsed successfully |
| `ticker` | `str` | string | ETF ticker | known symbols | No | 11 unique tickers |
| `close` | `float64` | float | close price | `> 0` when present | Yes | 3,580 nulls detected |

### `hungary_cpi_yoy.csv`

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| `date` | `datetime64[us]` | datetime | observation date | valid monthly dates | No | parsed successfully |
| `cpi_yoy` | `float64` | float | YoY CPI (%) | plausible macro range | No | min/max plausible |

### `hungary_10y_yield.csv`

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| `date` | `datetime64[us]` | datetime | observation date | valid monthly dates | No | parsed successfully |
| `yield_10y` | `float64` | float | Hungary 10Y yield (%) | plausible rate range | No | min/max plausible |

### `bond_reference_template.csv`

| Column | Type (Observed) | Expected Type | Meaning | Valid Range | Nullable | Notes |
|---|---|---|---|---|---|---|
| `bond_id` | `str` | string | bond identifier | non-empty | No | value observed: `2033/I` |
| `country` | `str` | string | issuing country | known country | No | `Hungary` |
| `type` | `str` | string | bond type | non-empty | No | `Inflation Linked` |
| `premium` | `str` | numeric or percent string | premium over inflation | percent-like | No | currently stored as `0.5%` |
| `redemption_fee` | `str` | numeric or percent string | early redemption fee | percent-like | No | currently stored as `1%` |

---

## 5. Coverage Overview

| Dataset | Earliest date | Latest date | Distinct dates / values | Notes |
|---|---|---|---:|---|
| ETF prices | 2010-01-04 | 2026-03-16 | 4,074 dates | daily market series |
| CPI YoY | 2010-01-01 | 2025-04-01 | 184 dates | monthly macro series |
| Hungary 10Y yield | 1999-02-01 | 2026-02-01 | 325 dates | monthly macro series |
| Bond template | n/a | n/a | 1 record | static parameter table |

### Structural coverage notes

- ETF history is long enough for rolling-window return analysis.
- CPI coverage begins in 2010, which is sufficient for medium-term inflation context.
- 10Y yield history extends earlier than the rest of the analytical package.
- The four datasets are not at the same frequency and must not be merged without explicit alignment rules in PROCESS.

---

## 6. Missingness Overview

| Dataset | Total missing values | Key observation |
|---|---:|---|
| `etf_prices_daily.csv` | 3,580 | all missingness concentrated in `close` |
| `hungary_cpi_yoy.csv` | 0 | no missing values detected |
| `hungary_10y_yield.csv` | 0 | no missing values detected |
| `bond_reference_template.csv` | 0 | no missing values detected |

### Column-level missingness of concern

| File | Column | Null count | Null % |
|---|---|---:|---:|
| `etf_prices_daily.csv` | `close` | 3,580 | 7.9886% |

### Missingness pattern assessment

Likely pattern:

- ETF non-null issue is currently classified as **Unknown / needs PROCESS validation**
- It may reflect:
  - incomplete ticker histories
  - data collection gaps
  - pre-inception rows
  - failed fetches
  - market/non-trading structural behavior encoded incorrectly

At PREPARE stage, the cause is not yet determined and no correction is allowed.

### Potential analytical bias risk

If the ETF nulls are not handled correctly later:

- return calculations may become biased
- rolling-window probabilities may be distorted
- some tickers may appear weaker or shorter-lived than they are
- cross-ticker comparisons may become inconsistent

No imputation or correction performed.

---

## 7. Anomaly Scan (No Edits Performed)

### `etf_prices_daily.csv`
Observed:
- no full-row duplicates
- valid composite key structure on `(Date, ticker)`
- 11 unique tickers
- positive price range when values are present:
  - min observed `7.0435`
  - max observed `695.49`

Potential anomalies requiring PROCESS validation:
- cause and distribution of 3,580 null `close` values
- unequal ticker start dates
- unequal ticker end dates
- possible sparse segments by ticker
- whether any nulls appear after ticker inception

### `hungary_cpi_yoy.csv`
Observed:
- no missing values
- no duplicate dates
- value range:
  - min `-1.442123`
  - max `25.73415`

Potential anomalies:
- none obvious structurally; range appears plausible for Hungarian inflation history

### `hungary_10y_yield.csv`
Observed:
- no missing values
- no duplicate dates
- value range:
  - min `1.83`
  - max `11.65`

Potential anomalies:
- none obvious structurally; rate range appears plausible

### `bond_reference_template.csv`
Observed:
- single-row table
- no missing values
- no duplicate key
- percent fields stored as strings

Potential anomalies:
- numeric percentage fields are not yet standardized
- bond assumptions still need official-term validation before later analysis

---

## 8. Data Credibility Assessment

| Dataset | Source reliability | Collection method | Known distortions | Freshness | Trust level |
|---|---|---|---|---|---|
| ETF prices | Moderate to High | likely automated export | adjustment methodology unknown; null cause unresolved | recent through 2026-03-16 | Moderate |
| CPI YoY | Moderate to High | macroeconomic series export | official-series revision risk | latest observed 2025-04-01 | Moderate to High |
| Hungary 10Y yield | Moderate to High | market/macro series export | source-definition mismatch risk | latest observed 2026-02-01 | Moderate |
| Bond template | Moderate | manual reference entry | not an official rules extract | static | Moderate |

### Credibility note

The package is structurally usable for a portfolio case study, but the bond template and ETF null pattern both require explicit validation before downstream interpretation. That is a normal PROCESS-stage task, not a PREPARE failure.

---

## 9. Risks / Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| ETF close nulls are explainable and manageable | the rest of the ETF structure is coherent | distorted return estimates | profile nulls by ticker and date in PROCESS |
| ETF prices are adjusted consistently enough for comparison | common export pattern | biased cross-ETF return comparison | inspect metadata and extreme return jumps |
| CPI YoY is an appropriate inflation context input | ASK frames bond return through inflation-linked logic | bond comparison model misaligned | verify bond payoff formula before ANALYZE |
| 10Y yield is benchmark context, not direct bond payoff input | likely intended macro reference | misuse in later argumentation | restrict its role explicitly in PROCESS/ANALYZE |
| Bond template values represent the intended instrument setup | single-row table was supplied as reference | decision benchmark may be wrong | validate against the actual bond specification |
| Parsed dates are semantically correct | dates converted cleanly | hidden monthly alignment errors | validate chronology and monthly continuity |

---

## 10. Refined Analytical Questions

Derived strictly from ASK:

1. What rolling annualized return windows are observable for each ETF after valid price series are cleaned?
2. What proportion of valid historical ETF windows exceed the bond threshold used in ASK?
3. How do volatility and drawdown vary across the ETF alternatives once missing values are resolved?
4. Are CPI and 10Y yield series structurally aligned well enough to serve as macro context for later comparison?
5. Can the bond template be converted into a reproducible parameter input without ambiguity?

No directional answer is introduced here.

---

## 11. Interpretation Guardrail

The following have **not** been done in PREPARE:

- no statement that equities outperform the bond
- no estimate that alternatives exceed 5%
- no volatility judgment
- no recommendation to hold or redeem
- no causal or predictive claim

This artifact remains structural only, consistent with repository governance in MASTER and PREPARE stage rules. :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2}

---

## 12. Validation Checks Performed

| Check | Status | Evidence |
|---|---|---|
| Raw files loadable | Yes | all four CSVs profiled |
| Row counts confirmed | Yes | generated in file profile |
| Column counts confirmed | Yes | generated in file profile |
| Date parsing performed in profiling step | Yes | all expected date columns detected |
| Full-row duplicate check | Yes | 0 duplicates in all files |
| Candidate primary key validation | Yes | all four datasets valid |
| Metadata presence check | Yes | all four datasets marked `meta_found = True` |
| Column-level null profiling | Yes | ETF `close` nulls detected |
| Random row inspection | Implicit via profiling workflow | recommended to supplement manually |
| Source-authority verification | No | deferred to PROCESS |

---

## 13. PREPARE Gate Checklist

- [x] Dataset identity documented
- [x] Grain clearly defined
- [x] Schema documented
- [x] Missingness analyzed
- [x] Anomalies recorded
- [x] Risks documented
- [x] No transformations performed
- [x] No interpretive language present
- [x] Next stage allowed: PROCESS

---

## 14. Assumptions

- The uploaded zip output is the authoritative PREPARE run for this case.
- The metadata files correspond correctly to each raw CSV.
- The ETF ticker universe is intended to represent alternative investment candidates for the case.
- The bond template is a helper parameter table rather than a legally complete instrument definition.

---

## 15. Limitations

- PREPARE does not yet explain the root cause of ETF `close` missingness.
- Ticker-level start/end coverage has not yet been profiled.
- Frequency harmonization across daily and monthly datasets has not been performed.
- No official bond-document verification has been completed yet.
- No source-lineage assessment beyond metadata presence has been completed.
- No transformation, imputation, or return calculation is allowed at this stage.

---

## 16. Integrity Declaration

No data transformation performed.

No hidden assumptions introduced.

No performance interpretation introduced.

Observations limited to structural dataset properties.