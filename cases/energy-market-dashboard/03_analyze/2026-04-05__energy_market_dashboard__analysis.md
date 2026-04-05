# ANALYZE — Energy Market Dashboard

Date: 2026-04-05  
Topic/Dataset: energy-market-dashboard

## 1. Questions Answered

This analysis answers the following questions derived from ASK and refined in PREPARE:

1. What is the correct aligned daily comparison window across WTI, Brent, Natural Gas, XLE, and SPY?
2. Which processed price field should be used consistently for dashboard metrics: `close` or `adj_close`?
3. What structural dashboard views are supportable from the cleaned aligned panel?
4. How different are the selected instruments in normalized performance, rolling volatility, drawdown, and relative strength structure?

## 2. Descriptive Statistics

### Analysis basis

Primary dataset used:  
`cases/energy-market-dashboard/outputs/process/aligned_panel.csv`

The aligned dataset contains:

- 5 instruments
- 1,256 common trading dates
- common comparison window: 2021-04-05 to 2026-04-02

Primary analysis field selected for dashboard metrics: **`close`**

### Metric selection rationale

`adj_close` is not methodologically consistent across the five instruments:

- for futures (`CL=F`, `BZ=F`, `NG=F`), `adj_close = close`
- for ETFs (`XLE`, `SPY`), `adj_close` materially differs from `close`

Because this dashboard is intended to compare market price structure across mixed asset types, `close` is the more consistent primary field for V1 dashboard analytics.

### Instrument summary (`close` basis)

Source: `analysis_summary_close.csv`

| Ticker | Start Price | End Price | Normalized End Index | Total Return % | Last 20D Ann. Vol % | Max Drawdown % | Aligned Obs |
|---|---:|---:|---:|---:|---:|---:|---:|
| BZ=F | 62.15 | 109.05 | 175.46 | 75.46 | 106.43 | -53.96 | 1,256 |
| CL=F | 58.65 | 112.06 | 191.07 | 91.07 | 99.89 | -55.32 | 1,256 |
| NG=F | 2.51 | 2.81 | 111.79 | 11.79 | 56.28 | -83.73 | 1,256 |
| SPY | 406.36 | 655.83 | 161.39 | 61.39 | 19.01 | -25.36 | 1,256 |
| XLE | 24.56 | 59.25 | 241.30 | 141.30 | 22.41 | -26.86 | 1,256 |

All comparative metrics are conditional on the selected aligned window and may differ under alternative start/end dates.

## 3. Segmentation / Comparisons

### A. Normalized performance comparison

Observed normalized end-index ranking on `close` basis:

1. XLE — 241.30
2. CL=F — 191.07
3. BZ=F — 175.46
4. SPY — 161.39
5. NG=F — 111.79

Observed difference:
- XLE ended the window with the highest normalized gain.
- SPY outperformed Natural Gas on normalized end value.
- WTI and Brent both ended above SPY but below XLE.

### B. Volatility comparison

Using last available 20-day rolling annualized volatility on `close` basis:

1. Brent — 106.43%
2. WTI — 99.89%
3. Natural Gas — 56.28%
4. XLE — 22.41%
5. SPY — 19.01%

Observed difference:
- commodity futures exhibit higher rolling volatility in the observed 20-day window
- XLE volatility is closer to SPY than to the commodity contracts

### C. Drawdown comparison

Maximum drawdown on `close` basis:

1. Natural Gas — -83.73%
2. WTI — -55.32%
3. Brent — -53.96%
4. XLE — -26.86%
5. SPY — -25.36%

Observed difference:
- Natural Gas experienced materially deeper historical downside than all other instruments
- XLE and SPY had similar drawdown scale relative to the commodity futures

### D. Relative strength comparison

Relative strength view constructed as:

- `XLE / SPY` on `close` basis

Observed structure:
- XLE/SPY relative strength is a valid dashboard panel because it directly represents sector performance against the broad market benchmark
- the ratio series is structurally interpretable and suitable for charting in V1

## 4. Relationship Exploration (Non-Causal Unless Proven)

| Variables | Method | Strength | Statistical Significance | Notes |
|---|---|---|---|---|
| XLE vs SPY | Price ratio (`XLE / SPY`) | Structurally useful | Not tested | Appropriate for benchmark-relative dashboard view |
| Each ticker vs itself over time | Normalized index | Strong descriptive use | Not applicable | Supports comparative path visualization |
| Daily price path vs rolling volatility | Rolling window descriptive metric | Structurally useful | Not tested | Useful for risk-state observation |
| Price path vs drawdown path | Drawdown transformation | Structurally useful | Not tested | Useful for downside context |

No causal interpretation is introduced.

## 5. Causality Gate (Mandatory)

No causal language is used in this analysis.

This report does **not** claim that one instrument causes, drives, impacts, or leads another.

All findings are descriptive and comparative.

## 6. Evidence Traceability Table (Mandatory)

| Claim | Evidence Reference | Strength of Evidence | Alternative Explanation Considered |
|---|---|---|---|
| The common aligned window is 2021-04-05 to 2026-04-02 | PROCESS aligned panel row/date summary | High | None material; directly measured |
| `close` is a more consistent V1 dashboard metric than `adj_close` | `close_vs_adjclose_comparison.csv` | Moderate | Total-return use case could justify `adj_close` for ETF-only views |
| XLE has the highest normalized end index in this aligned window | `analysis_summary_close.csv` normalized end index | High | Result depends on chosen start/end window |
| Commodity futures exhibit higher rolling volatility in the observed 20-day window | `analysis_summary_close.csv` last 20D annualized volatility | Moderate | Different windows may change ordering somewhat |
| Natural Gas has the deepest maximum drawdown in the aligned window | `analysis_summary_close.csv` max drawdown | High | Magnitude depends on chosen historical window |

## 7. What the Data Supports

The data supports the following statements:

- A common aligned daily comparison window exists across all five instruments.
- `close` is the more internally consistent primary field for a mixed-asset structural dashboard in V1.
- XLE delivered the highest normalized end value over the aligned window on `close` basis.
- Commodity futures exhibit higher rolling volatility in the observed 20-day window.
- Natural Gas has the deepest historical drawdown in the aligned window among the five instruments.
- XLE/SPY relative strength is a suitable benchmark-relative dashboard view.

## 8. What the Data Does NOT Support

The data does **not** support the following claims:

- that energy commodities cause XLE moves
- that XLE will continue outperforming in the future
- that recent volatility rankings will persist
- that this dashboard can forecast energy-market turning points
- that `adj_close` should never be used; only that it is less consistent for mixed-asset V1 comparison
- that volume is directly comparable across futures and ETFs without additional normalization

## 9. Alternative Explanations

### Finding: XLE finished with the highest normalized end value
Possible alternatives:
- result is window-sensitive
- sector composition and equity market structure differ from direct commodity price behavior
- use of `adj_close` for ETF-only total-return analysis would change magnitude

### Finding: commodities show higher rolling volatility
Possible alternatives:
- current ranking depends on a 20-day window
- contract-specific market conditions may dominate recent volatility
- volatility comparisons may differ under different annualization windows

### Finding: Natural Gas has the deepest drawdown
Possible alternatives:
- natural gas is structurally more prone to extreme cyclical moves
- drawdown depth is path-dependent and strongly start/end-window sensitive
- futures contract structure may influence long-horizon comparability

## 10. Limitations

### Data limitations
- data is sourced from `yfinance`, which is acceptable for portfolio analysis but not an institutional market-data standard
- futures and ETFs are not methodologically identical instruments
- volume fields are not directly comparable across all asset types

### Methodological limitations
- no inferential statistics were used
- volatility summary uses a 20-day rolling annualized snapshot, which is window-sensitive
- normalized performance is dependent on chosen start date

### External validity limits
- findings describe this selected instrument set only
- findings should not be generalized to the entire energy market without additional coverage

### Sensitivity to assumptions
- conclusions depend on the aligned-date approach
- metric interpretation depends on the choice of `close` rather than `adj_close`

## 11. Analytical Confidence Level

**Overall confidence: Moderate**

### Justification
- data quality is good at the raw structural level
- aligned panel integrity is strong
- descriptive metrics are reproducible
- metric selection for mixed asset types is defensible
- conclusions remain descriptive and appropriately bounded
- confidence is not high because source methodology and cross-asset comparability still impose limits

## 12. ANALYZE Gate Checklist

- [x] Questions trace to ASK
- [x] Statistics reproducible from PROCESS
- [x] Claims mapped to evidence
- [x] Causality not overstated
- [x] Alternative explanations considered
- [x] Limitations acknowledged
- [x] “What data does NOT support” section completed
- [x] Analytical confidence justified
- [x] Next stage allowed (ACT)

## 13. Validation Checks Performed

Performed:
- confirmed aligned dataset has 1,256 common dates across all five tickers
- generated normalized performance chart
- generated rolling 20-day annualized volatility chart
- generated drawdown chart
- generated XLE/SPY relative strength chart
- compared `close` vs `adj_close` total-return impact by ticker

Recommended:
- spot-check a sample of chart dates against raw CSV values
- test whether dashboard should include optional ETF-only total-return mode using `adj_close`
- validate whether front-month futures behavior is acceptable for the project narrative

## 14. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| `close` is the best primary V1 metric | It is structurally consistent across mixed asset types | Dashboard may understate ETF total-return behavior | Compare dashboard outputs under `close` vs `adj_close` modes |
| aligned-date comparison is preferable to full-history per-ticker views | Cross-asset comparison requires same-date alignment | Some instrument-specific information is lost | Compare aligned vs full-history chart behavior |
| 20-day rolling volatility is sufficient for V1 risk view | It is common and interpretable | Window may be too short for stable comparisons | Test additional windows such as 60-day |

## 15. Integrity Declaration

- No conclusions beyond evidence
- No causal claims without identification
- No selective reporting
- All major claims traceable
- Uncertainty explicitly acknowledged