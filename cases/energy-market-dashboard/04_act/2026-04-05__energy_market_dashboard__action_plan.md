# ACT — Conclusions & Action Plan

Date: 2026-04-05  
Topic/Dataset: energy-market-dashboard

## 1. Evidence-Based Conclusion Mapping (Mandatory)

| Conclusion | Evidence Reference | Confidence | Risk if Wrong |
|---|---|---|---|
| The V1 dashboard should use the aligned panel as its analytical base dataset | `cases/energy-market-dashboard/outputs/process/aligned_panel.csv`, `process_audit_summary.csv` | High | Cross-instrument comparisons would become inconsistent if partial-coverage dates are used |
| The combined panel should be retained only for coverage diagnostics, not direct cross-instrument comparison | `cases/energy-market-dashboard/outputs/process/combined_panel.csv`, `date_coverage.csv`, `ticker_coverage_summary.csv` | High | Comparisons could mix unequal date availability and distort interpretation |
| `close` should be the default V1 metric basis for mixed-asset comparison | `close_vs_adjclose_comparison.csv` | Moderate | ETF total-return behavior would be understated relative to an ETF-only `adj_close` design |
| The V1 dashboard can support four core descriptive views reliably | `analysis_summary_close.csv`, chart outputs in `cases/energy-market-dashboard/outputs/analyze/charts/` | High | Overloading the dashboard with unsupported views would reduce clarity |
| Relative strength should be represented explicitly as `XLE / SPY` | `relative_strength_xle_vs_spy_close.png` | High | Omitting the benchmark-relative panel would weaken the sector-vs-market story |

## 2. Recommendations

### Recommendation 1
**Action:**  
Use `cases/energy-market-dashboard/outputs/process/aligned_panel.csv` as the only dataset feeding the V1 analytical dashboard.

**Rationale:**  
All five instruments are present on each aligned date, which preserves same-date comparability.

**Expected impact:**  
Cleaner and more defensible cross-instrument charts.

**Evidence strength:**  
High

**Operational feasibility:**  
High

---

### Recommendation 2
**Action:**  
Use `close` as the default dashboard metric basis in V1.

**Rationale:**  
`adj_close` is identical to `close` for the futures series, but materially different for `SPY` and `XLE`. For a mixed futures-and-ETF dashboard, `close` is the more internally consistent baseline.

This choice is specific to a mixed-asset (futures + ETF) dashboard and may differ in ETF-only use cases.

**Expected impact:**  
More coherent mixed-asset comparisons with less methodology drift.

**Evidence strength:**  
Moderate

**Operational feasibility:**  
High

---

### Recommendation 3
**Action:**  
Include exactly four mandatory V1 panels:
1. normalized performance  
2. rolling 20-day annualized volatility  
3. drawdown  
4. `XLE / SPY` relative strength

**Rationale:**  
These are directly supported by the processed aligned dataset and the completed analysis outputs.

**Expected impact:**  
A focused dashboard with strong explanatory value and low feature bloat.

**Evidence strength:**  
High

**Operational feasibility:**  
High

---

### Recommendation 4
**Action:**  
Use `cases/energy-market-dashboard/outputs/process/combined_panel.csv` only for diagnostics such as date coverage, ticker coverage, and pipeline audits.

**Rationale:**  
The combined panel contains dates without full ticker coverage and should not be the basis for direct comparative dashboard views.

**Expected impact:**  
Stronger methodological discipline and fewer misleading comparisons.

**Evidence strength:**  
High

**Operational feasibility:**  
High

---

### Recommendation 5
**Action:**  
Exclude the following from V1:
- forecasting widgets
- causal claims
- cross-asset volume comparison panels
- macro overlays
- sentiment/news layers

**Rationale:**  
These are not yet supported by the current evidence base or current processing pipeline.

**Expected impact:**  
Higher clarity, lower implementation risk, and a stronger portfolio narrative.

**Evidence strength:**  
High

**Operational feasibility:**  
High

## 3. Risk & Uncertainty Assessment

| Recommendation | Key Assumption | What Could Invalidate It | Sensitivity |
|---|---|---|---|
| Use aligned panel for dashboard analytics | Same-date comparability is the correct analytical priority | Future use case may require per-ticker full-history views | Moderate |
| Use `close` as V1 default | Mixed-asset consistency matters more than ETF total-return adjustment | A later ETF-focused mode may justify `adj_close` | Moderate |
| Keep four-panel V1 scope | Portfolio clarity is more valuable than feature breadth | User requirements may later require additional context panels | Low |
| Use combined panel only for diagnostics | Partial-coverage dates are analytically unsafe for direct comparison | A separate non-comparative history view could later use combined data | Low |

## 4. Monitoring & Validation Plan

| Metric / Check | Monitoring Frequency | Threshold for Reassessment | Trigger Condition for Rollback |
|---|---|---|---|
| Aligned panel row count | Every pipeline run | Any drop below expected full-coverage logic | Missing ticker coverage on aligned dates |
| Schema consistency | Every pipeline run | Any missing/extra columns | Pipeline failure or schema drift |
| `close` vs `adj_close` divergence | At each new version | Material changes in instrument behavior or project scope | Need for ETF-only total-return mode |
| Chart sanity review | Every major update | Visual mismatch vs summary tables | Chart output inconsistent with source tables |

## 5. Expected Impact

**Short-term effect:**  
A reproducible, portfolio-ready V1 dashboard specification grounded in completed PROCESS and ANALYZE work.

**Long-term effect:**  
A stable base for adding optional future modes such as ETF-only total-return view, broader energy coverage, or macro context overlays.

**Measurable KPI(s):**
- successful generation of all 4 V1 charts
- successful regeneration of aligned and audit outputs
- zero schema drift on rerun
- dashboard renders only supported panels

**Estimated magnitude:**  
High implementation value for portfolio presentation; no financial-performance claim is made.

## 6. Implementation Plan

**Owner:**  
Repository owner

**Timeline:**  
Immediate next build cycle

**Dependencies:**  
- `cases/energy-market-dashboard/outputs/process/aligned_panel.csv` (primary analytical dataset)
- `cases/energy-market-dashboard/outputs/process/combined_panel.csv` (diagnostics only)
- `analysis_summary_close.csv`
- `close_vs_adjclose_comparison.csv`
- chart outputs under `cases/energy-market-dashboard/outputs/analyze/charts/`
- `run_analyze_full.py`

**Required data or tooling:**  
- Python environment with `pandas`, `numpy`, `matplotlib`
- existing PREPARE and PROCESS pipeline outputs

**Review checkpoint date:**  
After first dashboard render and screenshot review

## 7. Scaling & Automation (If Applicable)

**Is repeatable pipeline logic required?**  
Yes

### Data requirements for automation
- stable raw fetch outputs for all five instruments
- stable aligned panel generation
- deterministic analytical summaries
- versioned chart outputs

### Tooling requirements
- `fetch_raw_data.py`
- `run_process_full.py`
- `run_analyze_full.py`
- future dashboard app entry point

### Governance considerations
- any change in metric basis (`close` vs `adj_close`) should trigger a version bump
- any expansion beyond the current five-instrument universe should trigger new PREPARE and PROCESS validation
- any new panel added to V1 should trace to explicit analytical evidence

## 8. Exact V1 Dashboard Panels

### Mandatory panels
1. **Normalized Performance (Close Basis)**  
   Purpose: compare path-level market behavior from a common starting point.

2. **Rolling 20-Day Annualized Volatility (Close Basis)**  
   Purpose: show short-horizon risk-state differences across instruments.

3. **Drawdown (Close Basis)**  
   Purpose: show downside depth and recovery structure.

4. **Relative Strength: XLE / SPY (Close Basis)**  
   Purpose: show energy sector performance versus broad equity benchmark.

### Supporting non-panel diagnostics
- date coverage summary
- ticker coverage summary
- raw file audit summary
- `close` vs `adj_close` comparison table

### Explicitly excluded from V1
- prediction/forecast panels
- macro indicator merge
- news/sentiment layer
- cross-asset volume comparison panel
- alert engine
- interactive recommendations

## 9. Recommendation Strength Classification

**Overall strength of recommendation:**  
Moderate

**Justification:**  
The evidence base is strong for descriptive dashboard design and dataset choice, but metric-basis choice remains a methodological design decision rather than a mathematically unique truth. The current recommendation is well-supported for V1, with clear boundaries and documented uncertainty.

## 10. Validation Checks Performed

Performed:
- confirmed ANALYZE uses `cases/energy-market-dashboard/outputs/process/aligned_panel.csv`
- compared `close` versus `adj_close`
- generated four V1 chart outputs
- retained `combined_panel.csv` only as a diagnostic input, not as a direct comparative base
- linked dashboard panel choices directly to completed analytical outputs

Recommended:
- render the first dashboard screen and verify titles, labels, and series ordering
- confirm chart visuals match the summary tables
- decide whether a future V2 should include an optional ETF-only `adj_close` mode

## 11. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Users of the dashboard need descriptive market structure, not forecasts | Current case scope is descriptive and portfolio-oriented | V1 may feel too narrow if expectations shift | Reassess project scope before V2 |
| Four panels are sufficient for V1 | Current evidence supports exactly these outputs | Dashboard may omit useful context | User review after first render |
| `close` is acceptable for mixed-asset structural comparison | It is the most consistent basis across futures and ETFs | Some users may expect total-return handling for ETFs | Compare V1 and optional ETF-only mode later |

## 12. Limitations

- This action plan does not claim investment usefulness or forecasting ability.
- The dataset mixes futures and ETFs, which limits interpretation scope.
- Metric-basis choice is defensible, but not uniquely mandatory for all future versions.
- V1 is intentionally narrow and excludes broader energy-system context.

## 13. Integrity Declaration

- All conclusions trace directly to ANALYZE stage evidence
- No causal overstatement introduced
- No recommendation exceeds evidence strength
- Risks explicitly acknowledged
- Uncertainty transparently communicated