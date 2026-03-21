# ACT — Conclusions & Action Plan

Date: 2026-03-15  
Topic/Dataset: SPDR Sector ETFs (Daily OHLCV)

---

# 1. Evidence-Based Conclusion Mapping

All conclusions below are derived from the ANALYZE artifact and remain bounded by its stated limits: descriptive statistics only, no causal inference, no forecasting, and no transaction-cost-aware portfolio optimization.

| Conclusion | Evidence Reference | Confidence | Risk if Wrong |
|---|---|---|---|
| A strict common-window comparison is required for fair cross-sector ranking because ETF inception dates differ materially. | ANALYZE §3, common window 2018-06-20 to 2024-06-24, 1512 observations per sector | High | Cross-sector comparisons would be biased by unequal history length |
| XLK was the strongest return leader in the common window. | ANALYZE §6, XLK annual return ~20.9% | Moderate | A portfolio tilt toward recent leaders could overweight a period-specific winner |
| XLE carried the weakest risk-adjusted descriptive profile among the highlighted sectors because volatility was highest while return was comparatively low in the common window. | ANALYZE §6, XLE annual return ~3.5%, annual volatility ~34.5% | Moderate | XLE could improve materially in a different macro regime not captured by this window |
| XLP and XLV behaved as lower-volatility defensive sectors relative to the broader sector set. | ANALYZE §6, XLP volatility ~16.4%, XLV volatility ~18.0%; ANALYZE §10 | Moderate | Defensive behavior may not persist in all future regimes |
| Sector diversification exists, but diversification benefit is incomplete because average sector correlation remained materially positive. | ANALYZE §7, average sector correlation ≈ 0.66 | High | Overestimating diversification benefit could understate portfolio concentration risk |
| Drawdown differences are large enough to matter for position sizing and risk policy. | ANALYZE §8, example max drawdowns: XLE ~−69%, XLK ~−34%, XLP ~−25% | High | Ignoring drawdown asymmetry could lead to unsuitable allocations |
| Cross-sectional dispersion is meaningful and episodically high, so sector-rotation style monitoring is analytically justified. | ANALYZE §9, mean dispersion ~0.0082, max ~0.0459, peak on 2020-11-09 | Moderate | Dispersion alone does not guarantee tradable opportunity after costs |
| The current evidence base is suitable for descriptive portfolio research, but not yet sufficient for implementation-grade allocation rules. | ANALYZE §11, §13, §15 | High | Premature implementation could convert descriptive findings into unsupported live decisions |

---

# 2. Recommendations

## Recommendation 1 — Use the common-window dataset as the default comparison baseline

**Action:**  
Treat `returns_summary_common_window.csv` as the primary ranking table for any sector comparison work.

**Rationale:**  
The ANALYZE stage established that differing ETF inception dates make full-history rankings non-comparable across all 11 sectors.

**Expected impact:**  
Improves fairness and auditability of sector ranking and prevents misleading conclusions from unequal lookback windows.

**Evidence strength:**  
High

**Operational feasibility:**  
High

---

## Recommendation 2 — Separate sectors into exploratory risk buckets before any portfolio logic

**Action:**  
Create three descriptive buckets for downstream analysis:

- Growth/High-return candidate: XLK
- Defensive/Lower-volatility candidates: XLP, XLV
- High-risk/high-instability candidate: XLE

**Rationale:**  
This grouping is directly supported by the common-window return, volatility, and drawdown outputs.

**Expected impact:**  
Improves interpretability and creates a cleaner structure for later benchmark-relative or rules-based work.

**Evidence strength:**  
Moderate

**Operational feasibility:**  
High

---

## Recommendation 3 — Do not use raw return ranking alone for allocation decisions

**Action:**  
Require any future allocation proposal to include at least:

- annual return
- annual volatility
- maximum drawdown
- average correlation to peer sectors or benchmark
- transaction-cost assumptions

**Rationale:**  
The analysis shows meaningful differences across return, volatility, and drawdown dimensions, while the dataset does not yet support optimization-grade allocation decisions.

**Expected impact:**  
Reduces the risk of choosing sectors only because of headline performance.

**Evidence strength:**  
High

**Operational feasibility:**  
High

---

## Recommendation 4 — Add a benchmark-relative extension before making any investment-style claim

**Action:**  
Next iteration should add SPY and compute:

- excess return vs SPY
- rolling correlation vs SPY
- relative strength series
- relative drawdown vs SPY

**Rationale:**  
The current stage explicitly notes that no benchmark ETF was included, limiting practical interpretation for portfolio use.

**Expected impact:**  
Converts the project from sector-only description into benchmark-aware market structure analysis.

**Evidence strength:**  
High

**Operational feasibility:**  
Moderate

---

## Recommendation 5 — Use dispersion as a monitoring feature, not as a standalone signal

**Action:**  
Track daily and rolling cross-sectional dispersion, but do not treat it as a tradable rule by itself.

**Rationale:**  
The analysis confirms meaningful dispersion, but it does not test persistence, tradability, turnover, or transaction costs.

**Expected impact:**  
Provides a disciplined bridge toward later rotation research without overstating what dispersion can do.

**Evidence strength:**  
Moderate

**Operational feasibility:**  
High

---

# 3. Risk & Uncertainty Assessment

| Recommendation | Assumption That Must Hold | What Could Invalidate It | Sensitivity to Data Quality Issues | Sensitivity to External Factors |
|---|---|---|---|---|
| Common-window baseline | Common window is the fairest shared comparison set | A different shared window materially changes rankings | Moderate | Moderate |
| Risk buckets | Historical descriptive profiles are stable enough to group sectors | Regime shift changes volatility/drawdown relationships | Moderate | High |
| Multi-metric allocation discipline | Risk metrics remain relevant to decision quality | Allocation objective ignores drawdown or volatility | Low | Moderate |
| Add SPY benchmark | SPY is an appropriate market proxy | Another benchmark is better aligned to objective | Low | Low |
| Dispersion monitoring only | Dispersion contains useful state information | Dispersion is noisy and not linked to persistent rotation | Low | High |

---

# 4. Monitoring & Validation Plan

| Item to Monitor | Key Metric(s) | Monitoring Frequency | Threshold for Reassessment | Trigger for Rollback |
|---|---|---|---|---|
| Cross-sector ranking stability | Rank order by annual return and volatility in rolling windows | Monthly or quarterly | Top-3 ranking changes materially across adjacent windows | If rankings prove highly unstable, stop using static bucket labels |
| Defensive bucket validity | Rolling 90-day volatility and max drawdown for XLP, XLV | Monthly | Volatility materially exceeds peer median for sustained period | Remove defensive label from affected sector |
| XLE risk characterization | Rolling volatility, max drawdown, downside tail frequency | Monthly | Risk metrics normalize relative to sector median | Remove high-risk label |
| Diversification assumption | Average correlation and stress-period correlation | Monthly | Average correlation rises further or converges toward 1 during stress | Reduce diversification claims |
| Dispersion usefulness | Rolling mean/percentile of cross-sectional dispersion | Weekly or monthly | Dispersion spikes fail to align with meaningful sector differentiation in later studies | Drop dispersion from priority monitoring set |

---

# 5. Expected Impact

## Short-term effect
Create a disciplined descriptive framework for sector comparison using a fair common window and multi-metric risk review.

## Long-term effect
Provide a defensible foundation for a benchmark-relative sector rotation research pipeline.

## Measurable KPI(s)

| KPI | Target |
|---|---|
| Use of common-window comparison in downstream files | 100% of cross-sector ranking artifacts |
| Inclusion of return + volatility + drawdown in future decision tables | 100% |
| Addition of benchmark-relative layer in next analysis iteration | Completed in next cycle |
| Explicit statement of non-causal scope in future writeups | 100% |

## Estimated magnitude
No defensible performance uplift can be estimated from the current evidence because the analysis is descriptive and does not test implementable portfolio rules.

---

# 6. Implementation Plan

| Item | Owner | Timeline | Dependencies | Required Data or Tooling | Review Checkpoint |
|---|---|---|---|---|---|
| Freeze current ACT artifact | Analyst | Immediate | ANALYZE complete | Markdown repo structure | Same day |
| Add SPY benchmark dataset | Analyst | Next iteration | Data sourcing and schema alignment | SPY daily OHLCV | At benchmark ingest completion |
| Build benchmark-relative scripts | Analyst | Next iteration | SPY available | Python, pandas, plotting utilities | After script validation |
| Add risk-adjusted comparison table | Analyst | Next iteration | Benchmark metrics available | Existing processed dataset + SPY | After new ANALYZE stage |
| Re-run full lifecycle if methods change materially | Analyst | As needed | Updated method or data | Versioned artifacts | At each stage gate |

---

# 7. Scaling & Automation

**Is repeatable pipeline logic required?**  
Yes.

## Data requirements for automation

- Cleaned sector ETF daily dataset
- Benchmark ETF dataset (recommended: SPY)
- Stable ticker metadata
- Deterministic common-window selection logic

## Tooling requirements

- Python pipeline for returns, drawdowns, rolling volatility, and correlation
- Standardized output folder for CSV and PNG artifacts
- Version-controlled scripts
- Re-runnable validation checks after each stage

## Governance considerations

- Preserve stage separation: PROCESS outputs must remain distinct from ANALYZE and ACT artifacts
- Version bump required for material dataset, method, or conclusion changes
- No automation output should bypass evidence review before ACT decisions are written

---

# 8. Recommendation Strength Classification

**Overall strength of recommendation: Moderate**

## Justification

The recommendation set is supported by consistent descriptive evidence across return, volatility, drawdown, correlation, and dispersion outputs. However, confidence is not high enough for implementation-grade portfolio decisions because:

- no benchmark ETF is included in the current stage
- no transaction-cost model is included
- no predictive testing is included
- no causal identification is attempted
- conclusions are sensitive to the chosen 2018-06-20 to 2024-06-24 common window

---

# 9. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| The common window is the correct fairness rule for comparison | It equalizes sector history length | Relative sector ranking may change under another shared window | Re-run rankings on alternative shared windows |
| Close prices are suitable for return computation | Used in ANALYZE methodology | Return estimates may be biased if prices are not properly adjusted | Verify adjusted-price treatment in source data |
| Annualized metrics using 252 trading days are appropriate | Standard convention in the analysis | Minor metric distortion | Recompute with actual observed trading-day assumptions if needed |
| Benchmark-relative extension will improve actionability | Current stage lacks SPY | Future ACT could still remain descriptive only | Validate whether benchmark metrics change decisions materially |

---

# 10. Limitations

1. This ACT stage inherits all ANALYZE limitations, including absence of benchmark ETF context and inability to verify corporate-action adjustments directly.
2. Recommendations are analytical and workflow-oriented, not live investment advice.
3. The evidence is descriptive and historical; it does not establish future sector leadership.
4. No Sharpe ratio, turnover, slippage, or transaction-cost-aware optimization was computed.
5. Example drawdown values and volatility profiles may change under different windows or updated data.

---

# 11. Validation Checks

Validation checks performed or recommended for this ACT stage:

- verified that each conclusion maps to a specific ANALYZE section
- removed any recommendation that would require causal or predictive evidence
- aligned recommendations with stated dataset limitations
- confirmed that benchmark addition is framed as a next-step requirement, not as a supported current finding
- confirmed that no recommendation exceeds moderate strength
- recommended re-validation after SPY integration and any method revision

---

# 12. Referenced Output Files

The ANALYZE stage produced the following reusable outputs for this ACT stage: `returns_summary_full_history.csv`, `returns_summary_common_window.csv`, `common_window_correlation_matrix.csv`, `common_window_drawdowns.csv`, `cross_sectional_dispersion.csv`, `sector_return_boxplot.png`, `rolling_90d_volatility.png`, `correlation_heatmap.png`, `drawdown_curves.png`, and `cross_sectional_dispersion.png`.

---

# 13. ACT Gate Checklist

- [x] Every conclusion mapped to evidence
- [x] Confidence level specified
- [x] Risks acknowledged
- [x] Monitoring plan defined
- [x] Impact made measurable where defensible
- [x] No speculative inflation introduced
- [x] No causal claims beyond ANALYZE evidence
- [x] Next stage clearly defined

---

# 14. Integrity Declaration

All conclusions trace directly to the ANALYZE stage evidence.  
No causal overstatement has been introduced.  
No recommendation exceeds the strength of the available evidence.  
Risks and uncertainty are explicitly acknowledged.
