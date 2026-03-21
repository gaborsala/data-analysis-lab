# PREPARE — Dataset Understanding

Date: 2026-03-15  
Topic/Dataset: Financial Decision Dataset Map — Bond vs Equity Allocation  
Source: Multiple public financial data providers  
Time range: Expected 2010–Present  
Rows/Cols: Not yet collected (dataset planning phase)

---

# 1. Context

This dataset map defines the **data architecture required to evaluate whether reallocating capital from a Hungarian inflation-linked government bond to equity investments can improve expected return**.

The dataset structure is designed to support a full analytical lifecycle:

ASK → PREPARE → PROCESS → ANALYZE → ACT

The goal of the dataset map is to:

- Identify required datasets
- Define dataset structure
- Clarify relationships between datasets
- Ensure analytical reproducibility

No financial performance interpretation is performed at this stage.

Reference lifecycle structure:  
Data Analysis Lab repository governance. :contentReference[oaicite:0]{index=0}

---

# 2. Grain / Unit of Analysis

Primary analysis grain:

**Time-series observation**

Typical row represents:


date × asset


Examples:

| date | asset | close_price |
|-----|------|------|
2024-01-01 | XLE | 89.21  
2024-01-01 | SPY | 470.15  

Expected primary key:


(date, asset)


Aggregation level:

Daily observations.

Secondary aggregated datasets:

- Monthly inflation
- Monthly bond return

Grain consistency expected across price datasets.

---

# 3. Dataset Architecture Map

The project requires **five core datasets**.

            ┌────────────────────────┐
            │  Inflation Dataset     │
            │  (Hungarian CPI)       │
            └────────────┬───────────┘
                         │
                         │
                ┌────────▼─────────┐
                │ Bond Return Model│
                │ (Inflation + 5%) │
                └────────┬─────────┘
                         │
                         │
  ┌──────────────────────▼─────────────────────┐
  │          Investment Decision Layer         │
  │   Compare Bond Return vs Equity Returns    │
  └───────────────┬───────────────┬────────────┘
                  │               │
         ┌────────▼───┐    ┌──────▼────────┐
         │ ETF Prices │    │ Market Index  │
         │ (SPDR ETFs)│    │ (SPY / World) │
         └────────────┘    └───────────────┘
                 │
                 │
          ┌──────▼───────┐
          │ News Engine  │
          │ Macro signals│
          └──────────────┘

Purpose:

To determine:

**Probability that equity returns exceed bond real return.**

---

# 4. Required Dataset List

## Dataset 1 — Hungarian Inflation (CPI)

Purpose:

Calculate bond real return.

Typical schema:

| Column | Type | Meaning |
|------|------|------|
date | date | observation date |
cpi | float | consumer price index |
inflation_rate | float | YoY inflation |

Frequency:

Monthly.

Possible sources:

- Hungarian Central Bank
- Hungarian Statistical Office
- OECD
- FRED

---

## Dataset 2 — Inflation-Linked Bond Specification

Purpose:

Model bond yield.

Example:

Hungarian bond **2033/I**

Schema:

| Column | Type | Meaning |
|------|------|------|
bond_id | string | bond series |
maturity_date | date | bond maturity |
inflation_link | bool | inflation indexed |
real_yield | float | fixed premium |
redemption_fee | float | early redemption cost |

Example:


bond_id: 2033/I
real_yield: inflation + 0.5%
redemption_fee: 1%


---

## Dataset 3 — ETF Historical Prices

Purpose:

Evaluate equity returns.

Universe:

SPDR sector ETFs.

| Ticker | Sector |
|------|------|
XLC | Communication |
XLY | Consumer Discretionary |
XLE | Energy |
XLF | Financials |
XLV | Healthcare |
XLI | Industrials |
XLB | Materials |
XLRE | Real Estate |
XLK | Technology |
XLU | Utilities |

Schema:

| Column | Type | Meaning |
|------|------|------|
date | date | trading date |
ticker | string | ETF ticker |
close | float | closing price |
volume | int | trading volume |

Frequency:

Daily.

Possible sources:

- Yahoo Finance
- Alpha Vantage
- Stooq
- Kaggle

---

## Dataset 4 — Market Benchmark

Purpose:

Reference performance.

Example:


SPY (S&P500 ETF)


Schema identical to ETF dataset.

---

## Dataset 5 — Macro / News Signals (Optional)

Purpose:

Contextual interpretation.

Derived from News Engine outputs.

Possible variables:

| Column | Meaning |
|------|------|
date | observation date |
macro_sentiment | macro score |
policy_event | binary |
commodity_shock | indicator |

This dataset is optional.

It provides **context but not causal claims**.

---

# 5. Missingness Overview

Expected missingness patterns:

| Dataset | Missingness Risk |
|------|------|
ETF price data | Low |
Inflation | Low |
Bond specification | None |
News signals | Moderate |

Potential bias risk:

Market holidays in price data.

---

# 6. Anomaly Scan (Planned)

Potential anomalies expected:

- Missing trading days
- ETF splits
- Inflation data revisions
- Bond rule changes

No corrections performed in this stage.

---

# 7. Data Credibility Assessment

| Dataset | Credibility |
|------|------|
ETF prices | High |
Inflation | High |
Bond spec | High |
News signals | Moderate |

Sources expected to be automated financial data providers.

---

# 8. Risks / Assumptions

| Assumption | Why | Risk | Detection |
|---|---|---|---|
ETF returns represent equity opportunity | ETF diversification | sector bias | compare benchmark |
Inflation data reliable | official statistics | revision risk | cross-source check |
Bond premium stable | based on documentation | rule change | verify issuer data |

---

# 9. Refined Analytical Questions

Derived from ASK stage.

Questions to evaluate later:

1. What is the historical distribution of annual returns for sector ETFs?
2. What probability exists that ETF returns exceed 5% annually?
3. What is the volatility and drawdown risk of these assets?
4. Under what conditions do sector ETFs outperform inflation-linked bonds?

No answers provided in this stage.

---

# 10. Validation Checks Planned

- Dataset row counts verified
- Schema validation performed
- Data source reliability verified
- Random row spot-check

---

# 11. PREPARE Gate Checklist

- [x] Dataset identity documented  
- [x] Grain clearly defined  
- [x] Schema documented  
- [x] Missingness analyzed  
- [x] Anomalies recorded  
- [x] Risks documented  
- [x] No transformations performed  
- [x] No interpretive language present  

Next stage allowed: **PROCESS**

---

# 12. Integrity Declaration

No dataset transformation performed.

Dataset map describes structural architecture only.

Observations limited to structural properties.

Interpretation intentionally excluded.