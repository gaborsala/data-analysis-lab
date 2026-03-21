# ANALYZE — Findings

Date: 2026-03-12  
Dataset: SPDR Sector ETFs (Daily OHLCV)  
Stage: ANALYZE

---

# 1. Purpose

The purpose of this stage is to transform the cleaned dataset into **interpretable statistical evidence** that answers the research questions defined in the ASK phase.

The analysis focuses on:

1. Sector return characteristics
2. Sector volatility differences
3. Sector correlation structure
4. Drawdown behaviour
5. Cross-sectional dispersion across sectors

All results are based on the **PROCESS-stage cleaned dataset** and the **common-window rule** required for fair sector comparison.

---

# 2. Analytical Dataset

## Source


data/processed/all_sectors_clean.csv


## Structure

| Attribute | Value |
|---|---|
Tickers | 11 sector ETFs |
Total rows | 61,448 |
Columns | ticker, sector, date, open, high, low, close, volume |

## Full dataset date range


1998-12-22 → 2024-06-24


## Sector coverage


XLB Materials
XLC Communication Services
XLE Energy
XLF Financials
XLI Industrials
XLK Technology
XLP Consumer Staples
XLRE Real Estate
XLU Utilities
XLV Health Care
XLY Consumer Discretionary


---

# 3. Analytical Window Design

ETF inception dates differ across sectors.

Example:

| ETF | Approx inception |
|---|---|
XLK | 1998 |
XLRE | 2015 |
XLC | 2018 |

Using the full dataset would therefore create **unequal historical exposure**.

### Solution

Define a **strict common comparison window**.


Common window start: 2018-06-20
Common window end: 2024-06-24


Observations per sector in common window:


1512 trading days


This window is used for **fair cross-sector comparison**.

Full-history statistics remain available for sensitivity checks.

---

# 4. Return Computation

Daily returns were calculated using close-to-close percentage change.


r_t = (P_t / P_{t-1}) − 1


Annualized return is computed using **compounded annual growth rate (CAGR)**:


annual_return = (1 + r_1)(1 + r_2)...(1 + r_n) ^ (252 / n) − 1


Annualized volatility:


σ_annual = σ_daily * √252


---

# 5. Full-History Sector Summary

This table reflects the **entire available dataset**, not the strict comparison window.

| Ticker | Observations | Annual Return | Annual Volatility |
|---|---|---|---|
XLC | 1512 | ~9.3% | ~23.7% |
XLY | 6415 | ~8.0% | ~22.7% |
XLK | 6415 | ~7.9% | ~25.9% |
XLV | 6415 | ~7.2% | ~18.0% |
XLI | 6415 | ~6.7% | ~21.3% |
XLB | 6415 | ~5.9% | ~23.9% |
XLE | 6415 | ~5.5% | ~29.0% |
XLP | 6415 | ~4.3% | ~15.4% |
XLU | 6415 | ~3.4% | ~19.5% |
XLF | 6415 | ~3.1% | ~28.9% |
XLRE | 2190 | ~2.9% | ~21.3% |

Interpretation:

These values are informative but **not directly comparable** due to different ETF start dates.

---

# 6. Common-Window Sector Comparison

The common window provides a fair comparison across all sectors.

| Ticker | Annual Return | Annual Volatility |
|---|---|---|
XLK | ~20.9% | ~26.6% |
XLV | ~9.7% | ~18.0% |
XLC | ~9.3% | ~23.7% |
XLI | ~9.1% | ~22.4% |
XLY | ~8.5% | ~24.4% |
XLB | ~7.5% | ~23.1% |
XLP | ~7.4% | ~16.4% |
XLF | ~7.3% | ~25.1% |
XLU | ~5.8% | ~21.9% |
XLE | ~3.5% | ~34.5% |
XLRE | ~3.5% | ~23.6% |

### Observations

Technology (XLK) delivered the highest return during this period.

Energy (XLE) shows **the highest volatility** with weaker return.

Consumer Staples (XLP) exhibits **the lowest volatility**.

---

# 7. Sector Correlation Structure

Correlation was computed using the **common-window daily return matrix**.

Average sector correlation:


≈ 0.66


Interpretation:

Sector ETFs move together substantially because they share a **common market factor**.

However, dispersion remains meaningful.

Examples:

| Pair | Correlation |
|---|---|
XLB vs XLI | high |
XLE vs XLU | relatively low |

Correlation matrix exported:


common_window_correlation_matrix.csv


Visual heatmap exported:


correlation_heatmap.png


---

# 8. Sector Drawdown Behaviour

Drawdown was computed as:


Drawdown_t = (Cumulative_t − Peak_t) / Peak_t


Maximum drawdown example values:

| Sector | Approx Max DD |
|---|---|
XLE | ~−69% |
XLK | ~−34% |
XLP | ~−25% |

Drawdown panel exported:


common_window_drawdowns.csv


Visualization:


drawdown_curves.png


---

# 9. Cross-Sectional Dispersion

Cross-sectional dispersion measures the standard deviation of sector returns on each trading day.


dispersion_t = std(returns across sectors)


Summary statistics:

| Metric | Value |
|---|---|
Mean | ~0.0082 |
Median | ~0.0073 |
90th percentile | ~0.013 |
Maximum | ~0.0459 |

Maximum dispersion occurred:


2020-11-09


Export:


cross_sectional_dispersion.csv


Visualization:


cross_sectional_dispersion.png


Interpretation:

High dispersion events represent **large differences between sector returns**, which may create rotation opportunities.

---

# 10. What the Data Supports

The analysis supports the following observations:

1. Sector volatility differs materially across sectors.
2. Technology strongly outperformed in the post-2018 period.
3. Energy shows the most extreme volatility profile.
4. Consumer staples and healthcare exhibit relatively stable volatility characteristics.
5. Sector ETFs remain positively correlated but still exhibit meaningful dispersion.

---

# 11. What the Data Does NOT Support

The dataset does not support:

1. causal explanations for sector performance
2. prediction of future sector leadership
3. macroeconomic attribution
4. transaction-cost-aware portfolio optimization
5. factor decomposition or risk modeling

This stage is purely **descriptive statistical analysis**.

---

# 12. Assumptions

1. Close prices correctly reflect adjusted price behaviour.
2. Daily returns are sufficiently representative for sector comparison.
3. Annualization uses 252 trading days.
4. The common window is an appropriate fairness adjustment for ETF inception differences.

---

# 13. Limitations

1. The dataset contains only price and volume fields.
2. No benchmark ETF (e.g., SPY) was included in this stage.
3. Corporate-action adjustments cannot be verified directly.
4. Results depend on the selected common-window period.

---

# 14. Validation Checks

Validation steps performed:

- verified row counts after return computation
- verified common-window alignment across sectors
- confirmed 11-sector coverage in all exported tables
- checked correlation matrix symmetry
- confirmed drawdown values are ≤ 0
- verified dispersion column naming
- verified chart export generation

---

# 15. Analytical Confidence

Overall confidence level:


Moderate


Reason:

- dataset size is large
- processing pipeline is reproducible
- analysis is descriptive rather than predictive

However, causal claims are intentionally avoided.

---

# 16. Evidence Artifacts Produced

Numeric exports:


returns_summary_full_history.csv
returns_summary_common_window.csv
common_window_correlation_matrix.csv
common_window_drawdowns.csv
cross_sectional_dispersion.csv


Visual artifacts:


sector_return_boxplot.png
rolling_90d_volatility.png
correlation_heatmap.png
drawdown_curves.png
cross_sectional_dispersion.png


These artifacts allow full reproducibility of the analysis.

---

# 17. Decision Gate

The ANALYZE stage is complete.

The outputs are sufficiently consistent to proceed to:


ACT stage