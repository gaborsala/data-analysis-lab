# ACT — Hungarian Inflation Bond vs Alternatives (v3 Merged)

Date: 2026-03-21  
Decision Context: Allocation decision between Hungarian inflation-linked government bond vs ETF-based alternatives  
Version: v3 (Merged — Analytical + Decision Layer)

---

## 1. Decision Objective

Determine whether capital should be allocated to:

- Hungarian inflation-linked bond (baseline, inflation-protected)
vs
- ETF-based alternatives

Using:
- return exceedance vs benchmark
- volatility and drawdown risk
- robustness across time windows

---

## 2. Evidence-Based Conclusion Mapping

| Conclusion | Evidence Reference | Confidence | Risk if Wrong |
|---|---|---|---|
| Some ETFs exceed the 5% hurdle frequently | ANALYZE Sections 3, 4 | Moderate | Overstates attractiveness if benchmark is misdefined |
| SPY is the most balanced candidate | ANALYZE Sections 4, 7 | Moderate | Future regimes may reduce its stability |
| XLK / XLY offer higher upside with higher risk | ANALYZE Sections 3, 7 | Moderate | Growth regime reversal |
| XLV / XLU behave defensively | ANALYZE Sections 4 | Moderate | Defensive properties may change |
| XLE has excessive downside risk for bond replacement | ANALYZE Sections 4, 13 | Moderate | Energy cycle could change |
| Benchmark simplification (5%) is the largest uncertainty | ANALYZE Sections 2, 8–12 | High | All conclusions may shift |

---

## 3. Instrument Classification (from evidence)

### Balanced benchmark
- SPY → best trade-off between return and risk

### Upside candidates
- XLK, XLY → strong exceedance, higher volatility/drawdown

### Defensive comparators
- XLV, XLU → lower risk, weaker upside

### Excluded as bond substitute
- XLE → high downside volatility

---

## 4. Decision Framework (Portfolio Layer)

### 4.1 Base allocation logic

| Profile | Allocation |
|--------|----------|
| Risk-averse | 70–90% bond / 10–30% ETF |
| Balanced | 40–60% bond / 40–60% ETF |
| Return-seeking | 10–30% bond / 70–90% ETF |

---

### 4.2 Tactical rules (evidence-constrained)

#### Stay in bond when:
- ETF drawdown > -15%
- volatility elevated
- inflation rising

#### Shift toward ETFs when:
- exceedance rate persistently high
- volatility stable/declining
- no recent deep drawdowns

#### Always:
- avoid 100% allocation
- maintain diversification buffer

---

## 5. Evidence → Decision Bridge (critical layer)

| Metric | Observed Pattern | Decision Impact |
|------|----------------|----------------|
| Exceedance frequency | High but unstable | Supports partial ETF allocation |
| Drawdown | Large for many ETFs | Limits allocation size |
| Volatility | Regime-dependent | Requires dynamic allocation |
| Benchmark uncertainty | High | Forces moderate confidence |

---

## 6. Risk & Uncertainty Assessment

### Structural risks

| Area | Risk |
|------|------|
| Benchmark | Simplified 5% hurdle |
| Regime | Future ≠ past |
| ETF behavior | Sector instability |
| Execution | Timing and discipline |

---

### Recommendation dependency (critical)

> All recommendations are conditional on benchmark definition

If benchmark changes:
→ entire ACT must be revalidated

---

## 7. Monitoring & Validation Plan

| Metric | Frequency | Trigger |
|------|----------|--------|
| Exceedance rate | Monthly | Drop below threshold |
| Drawdown | Monthly | Breach -20% |
| Volatility | Monthly | Spike |
| Benchmark validity | Version-based | Model update |

---

## 8. Recommendation Strength

**Overall strength: MODERATE**

### Why:
- Strong relative comparisons
- BUT:
  - benchmark not fully modeled
  - regime uncertainty

---

## 9. Final Decision Statement

- Bond = **stable base layer**
- ETFs = **opportunistic return layer**

### Therefore:

> Optimal strategy = **hybrid allocation with dynamic adjustment**

NOT:
- full bond
- full ETF

---

## 10. Implementation Plan

### Immediate
- Use SPY as benchmark comparator
- Define allocation profile

### Next iteration
- Build modeled bond benchmark
- rerun ANALYZE
- update ACT

---

## 11. Assumptions

- 5% threshold approximates bond return
- ETF data is clean
- rolling 12M captures relevant behavior
- no costs/taxes included

---

## 12. Limitations

- No predictive model
- Historical-only analysis
- FX and tax ignored
- behavioral execution risk

---

## 13. Validation Checks

- Conclusions mapped to ANALYZE
- No overclaiming
- Risks explicit
- Decision logic consistent with evidence

---

## 14. Governance Notes

- Benchmark must be versioned
- Any change → ANALYZE + ACT update required
- Recommendation strength must downgrade if unresolved

---

## 15. Strategic Insight

This is not an asset selection problem.

It is a **portfolio construction problem under uncertainty**.

---

## 16. Evolution Path

Next upgrade:
- pipeline decision engine
- benchmark modeling
- automated monitoring

---

## 17. Definition of Done

- Evidence mapped
- Decision usable
- Risks acknowledged
- Monitoring defined
- No unsupported claims