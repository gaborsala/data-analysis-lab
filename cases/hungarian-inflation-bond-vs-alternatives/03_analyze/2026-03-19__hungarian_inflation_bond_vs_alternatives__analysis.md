# ANALYZE — Hungarian Inflation Bond vs Alternatives

Date: 2026-03-19  
Topic/Dataset: Hungarian Inflation-Linked Government Bond vs Alternative Investments

## 1. Questions Answered

This analysis answers the following ASK-aligned questions:

1. How often did the ETF alternatives exceed a 5% annual threshold on a rolling 12-month basis?
2. Which ETFs had the highest and lowest historical threshold exceedance rates?
3. What were the historical volatility and maximum drawdown characteristics of each ETF?
4. How do conclusions differ between:
   - full-history mode
   - common-window mode
5. Does the historical evidence support the claim that some alternatives frequently exceeded the bond benchmark threshold?

## 2. Analytical Setup

### Modes used

Two analytical modes were run to handle unequal ETF inception histories:

- **Full-history mode**: each ETF evaluated over its maximum available history
- **Common-window mode**: all ETFs restricted to the overlapping valid period

This dual-mode design was required because:

- `XLC` starts later
- `XLRE` starts later

### Benchmark used

A constant threshold of **5% annual return** was used in decimal form:

- `threshold = 0.05`

Reason:

- no benchmark threshold column was available in the merged monthly analysis panel
- a constant 5% hurdle was consistent with the ASK framing
- benchmark interpretation therefore remains a simplification, not a full bond-cashflow model

## 3. Descriptive Statistics

### 3.1 Full-history summary

| Ticker | Valid windows | Mean rolling 12m return | Exceedance rate | Annualized volatility | Max drawdown |
|---|---:|---:|---:|---:|---:|
| XLY | 183 | 16.02% | 86.34% | 18.37% | -36.27% |
| XLK | 183 | 20.29% | 85.79% | 17.50% | -31.21% |
| SPY | 183 | 14.81% | 79.23% | 14.25% | -23.93% |
| XLV | 183 | 13.27% | 74.86% | 13.62% | -15.62% |
| XLC | 82 | 17.55% | 74.39% | 19.01% | -43.46% |
| XLU | 183 | 11.37% | 73.77% | 14.13% | -18.87% |
| XLI | 183 | 14.26% | 72.68% | 17.73% | -27.15% |
| XLF | 183 | 13.67% | 62.30% | 18.59% | -31.79% |
| XLB | 183 | 10.33% | 61.75% | 19.00% | -27.38% |
| XLE | 183 | 10.00% | 54.10% | 26.60% | -63.97% |
| XLRE | 114 | 7.48% | 47.37% | 16.97% | -32.25% |

### 3.2 Common-window summary

| Ticker | Valid windows | Mean rolling 12m return | Exceedance rate | Annualized volatility | Max drawdown |
|---|---:|---:|---:|---:|---:|
| XLK | 83 | 24.12% | 83.13% | 20.87% | -31.21% |
| XLY | 83 | 13.78% | 78.31% | 22.14% | -36.27% |
| SPY | 83 | 15.84% | 77.11% | 16.46% | -23.93% |
| XLC | 82 | 17.55% | 74.39% | 19.01% | -43.46% |
| XLI | 83 | 14.39% | 69.88% | 20.43% | -27.15% |
| XLU | 83 | 11.07% | 66.27% | 16.00% | -18.87% |
| XLV | 83 | 9.47% | 62.65% | 15.30% | -15.62% |
| XLF | 83 | 14.44% | 59.04% | 20.59% | -31.79% |
| XLE | 83 | 14.39% | 59.04% | 32.36% | -58.21% |
| XLB | 83 | 10.79% | 55.42% | 20.47% | -26.18% |
| XLRE | 83 | 8.02% | 51.81% | 18.22% | -32.25% |

## 4. Segmentation / Comparisons

### 4.1 Highest threshold exceedance rates

#### Full-history
- `XLY`: 86.34%
- `XLK`: 85.79%
- `SPY`: 79.23%

#### Common-window
- `XLK`: 83.13%
- `XLY`: 78.31%
- `SPY`: 77.11%

### 4.2 Lowest threshold exceedance rates

#### Full-history
- `XLRE`: 47.37%
- `XLE`: 54.10%
- `XLB`: 61.75%

#### Common-window
- `XLRE`: 51.81%
- `XLB`: 55.42%
- `XLE`: 59.04%

### 4.3 Risk comparison highlights

Lowest full-history drawdowns:
- `XLV`: -15.62%
- `XLU`: -18.87%
- `SPY`: -23.93%

Highest full-history drawdowns:
- `XLE`: -63.97%
- `XLC`: -43.46%
- `XLY`: -36.27%

Lowest full-history annualized volatility:
- `XLV`: 13.62%
- `XLU`: 14.13%
- `SPY`: 14.25%

Highest full-history annualized volatility:
- `XLE`: 26.60%
- `XLC`: 19.01%
- `XLB`: 19.00%

## 5. Relationship Exploration (Non-Causal)

This analysis is descriptive. No causal identification method was used.

Observed pattern:

- Higher average rolling returns often came with higher volatility and/or deeper drawdowns.
- `XLK` showed strong return and exceedance performance, but volatility was higher than `SPY`, `XLV`, and `XLU`.
- `XLE` had only moderate threshold exceedance performance despite very high upside windows, because downside severity was also large.
- `XLV` and `XLU` showed lower risk profiles than many cyclicals, but also lower exceedance rates than `XLK`, `XLY`, and `SPY`.

These are associations only. They do not establish that sector exposure causes better or worse outcomes.

## 6. Evidence Traceability Table

| Claim | Evidence reference | Strength of evidence | Alternative explanation considered |
|---|---|---|---|
| Some ETFs exceeded the 5% threshold in most rolling 12m windows | Exceedance rates in full-history and common-window tables | High | Threshold is simplified rather than bond-cashflow-specific |
| `XLK` was the strongest broad performer across both modes | Highest or near-highest mean rolling 12m return and top exceedance rate in both modes | High | Common-window period may favor growth-heavy sectors |
| `SPY` offered a strong balance of exceedance and lower drawdown than many sectors | SPY exceedance, volatility, and drawdown in both summaries | High | Broad-market diversification may reflect the selected sample period |
| `XLE` had large upside potential but materially higher risk | Mean return, max return window, annualized volatility, and max drawdown | High | Commodity/energy regime dependence |
| `XLRE` was the weakest threshold-exceedance candidate in this dataset | Lowest exceedance rate in both modes | Moderate | Shorter history and rate-sensitive recent period may affect result |

## 7. What the Data Supports

The data supports the following evidence-based statements:

1. Several ETF alternatives historically exceeded a 5% annual threshold in a majority of rolling 12-month windows.
2. `XLK`, `XLY`, and `SPY` were the strongest threshold-exceedance candidates in this analysis.
3. `SPY` showed a comparatively balanced profile:
   - high exceedance rate
   - lower volatility than many sectors
   - shallower drawdown than most sector ETFs
4. `XLV` and `XLU` had lower-risk historical profiles than most cyclicals, but also somewhat lower exceedance rates than the strongest return leaders.
5. `XLE` had the most severe downside profile in the study, which weakens any simple “high return therefore better alternative” interpretation.
6. Full-history and common-window results are directionally similar for the top and bottom groups, but the exact rankings and magnitudes change.

## 8. What the Data Does NOT Support

The data does **not** support the following claims:

1. That future ETF returns will exceed the bond hurdle.
2. That any ETF is categorically better than the inflation-linked bond for all investors.
3. That macro variables in the merged panel caused the observed return patterns.
4. That threshold exceedance alone is sufficient to justify switching out of the bond.
5. That full-history results are perfectly comparable across all tickers without adjustment for unequal inception dates.
6. That this simplified 5% threshold fully captures the real economic decision of redeeming a specific inflation-linked bond early.

## 9. Alternative Explanations

Several competing explanations remain plausible:

1. **Regime dependence**  
   Strong exceedance rates may reflect favorable historical equity regimes rather than durable superiority.

2. **Window selection effects**  
   Common-window results may differ because the overlapping period emphasizes more recent market structure.

3. **Inception bias**  
   `XLC` and `XLRE` have shorter histories, which reduces direct comparability in full-history mode.

4. **Benchmark simplification**  
   A constant 5% hurdle is analytically useful, but it is not equivalent to a full bond return path with inflation indexation, premium mechanics, and early-redemption timing.

5. **Proxy mismatch**  
   US sector ETFs are investable market proxies, but they are not one-to-one substitutes for a Hungarian inflation-linked government bond decision.

## 10. Limitations

### Data limitations
- The analysis uses ETF proxy history, not investor-specific realized portfolios.
- The benchmark was implemented as a constant 5% hurdle rather than a fully modeled bond cashflow series.
- Unequal ETF inception dates reduce comparability in full-history mode.

### Methodological limitations
- Results are based on rolling 12-month windows only.
- No statistical significance testing was required for the main descriptive objective.
- No transaction cost, tax, FX, or implementation friction was included for ETF switching.

### External validity limits
- Historical US ETF performance may not transfer directly to a Hungarian investor’s actual opportunity set.
- Future inflation, yields, and equity regimes may differ materially from the sample history.

### Sensitivity to assumptions
- Final interpretation is sensitive to the chosen bond hurdle.
- Results may change if the bond benchmark is redefined as:
  - net of redemption fee timing
  - inflation-linked realized carry
  - FX-adjusted local investor return target

## 11. Validation Checks Performed

Performed or confirmed from generated outputs:

- rolling 12-month return tables generated for both modes
- threshold exceedance tables generated for both modes
- volatility and drawdown tables generated for both modes
- combined comparison tables generated successfully
- mode comparison table generated successfully
- benchmark interpretation review table generated
- chart set generated successfully
- full ANALYZE run completed with success status

Recommended additional validation:

- manually spot-check one ticker’s rolling 12m return on a sample month
- manually verify one exceedance-rate calculation from detail windows
- review whether 5% should remain the final benchmark for ACT-stage recommendations
- confirm whether FX and switching frictions should be included in a later version

## 12. Analytical Confidence Level

**Overall confidence: Moderate**

### Justification
- Data quality and pipeline execution appear stable.
- The descriptive tables are internally consistent across modes.
- The main uncertainty is not computation quality; it is benchmark interpretation.
- Because the bond decision was simplified to a constant 5% hurdle, conclusions should remain proportional to that simplification.

## 13. Conclusion Summary

A cautious evidence-based summary is:

- Historical data supports that several ETF alternatives frequently exceeded a 5% annual hurdle over rolling 12-month windows.
- The strongest candidates in this analysis were `XLK`, `XLY`, and `SPY`.
- Among those, `SPY` appears to offer the most balanced historical trade-off between threshold exceedance and downside control.
- Defensive sectors such as `XLV` and `XLU` offered milder downside profiles, but generally weaker upside evidence than the strongest growth-led alternatives.
- High-upside sectors such as `XLE` carried materially higher realized risk, which limits their attractiveness as straightforward bond substitutes.
- Any final action recommendation must explicitly state that the benchmark is simplified and that historical exceedance is not a future guarantee.

## 14. ANALYZE Gate Checklist

- [x] Questions trace to ASK
- [x] Statistics reproducible from PROCESS outputs
- [x] Claims mapped to evidence
- [x] Causality not overstated
- [x] Alternative explanations considered
- [x] Limitations acknowledged
- [x] “What the data does NOT support” completed
- [x] Analytical confidence justified

Next stage allowed: **ACT**

## 15. Integrity Declaration

No conclusions were drawn beyond the generated evidence tables.

No causal claims were made.

No selective reporting was introduced.

Uncertainty around benchmark interpretation was explicitly retained.