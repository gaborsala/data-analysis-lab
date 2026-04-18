# ANALYZE — Backtest Evaluation (Long/Short Overlay) (v1.1 Hardened)

Date: 2026-04-16  
Topic/Dataset: Market Structure Long/Short Overlay Backtest on SPY

---

## 1. Questions Answered

This analysis evaluates:

1. Does adding a short-side rule (LH/LL → short) improve performance relative to baseline?
2. How does the long/short overlay affect return, drawdown, and volatility?
3. Is the sector-based market structure signal suitable for directional short exposure on SPY?

---

## 2. Descriptive Statistics

### Table A. Strategy comparison summary

| Metric | Baseline (Always Long SPY) | Overlay (Long/Short) |
|---|---:|---:|
| Final Equity | 8.235 | 0.220 |
| Total Return (%) | 723.54% | -78.00% |
| Annualized Return (%) | 13.85% | -8.90% |
| Annualized Volatility (%) | ~18% | ~higher (strategy unstable) |
| Max Drawdown (%) | -33.72% | -80.80% |
| Invested Share (%) | 100% | 83.37% |

---

### Table B. Position distribution

| Position | Days | Share |
|---|---:|---:|
| LONG | — | 37.31% |
| SHORT | — | 46.06% |
| FLAT | — | 16.63% |

---

## 3. Segmentation / Comparisons

### Comparison 1: Return vs Drawdown

| Metric | Observation |
|---|---|
| Total Return | Overlay collapses performance |
| Drawdown | Overlay significantly worse than baseline |
| Volatility | Increased instability vs baseline |

Observed difference:

- The long/short overlay produces both **lower return** and **higher drawdown**, indicating structural failure of the strategy design.

---

### Comparison 2: Exposure Behavior

| Metric | Observation |
|---|---|
| Short exposure | ~46% of time |
| Long exposure | ~37% of time |
| Flat exposure | ~17% of time |

Observed difference:

- The system is short more often than long.
- This is misaligned with SPY’s long-term upward drift.

---

## 4. Relationship Exploration (Non-Causal Unless Proven)

| Variables | Method | Strength | Notes |
|---|---|---|---|
| Regime → Position mapping | Direct rule application | High | Deterministic mapping |
| Short exposure → performance degradation | Strategy comparison | High descriptive evidence | Strong negative impact observed |
| Market drift vs regime-based shorting | Structural reasoning | Moderate | SPY upward bias conflicts with frequent shorting |

No causal claims are made.

---

## 5. Causality Gate (Mandatory)

This analysis does NOT claim:

- That LH/LL causes negative returns in SPY
- That sector weakness implies index-level short opportunities
- That the overlay predicts price direction

The overlay is a **rule-based exposure transformation**, not a predictive model.

---

## 6. Evidence Traceability Table (Mandatory)

| Claim | Evidence | Strength | Alternative Explanation |
|---|---|---|---|
| Overlay produces negative return | Table A | High | Excessive short exposure drives result |
| Drawdown increases significantly | Table A | High | Compounding losses during incorrect shorts |
| Short exposure dominates behavior | Table B | High | Rule mapping overweights LH/LL |
| Strategy misaligned with SPY drift | Table A + B | Moderate | Could differ in other assets |

---

## 7. What the Data Supports

The backtest supports:

1. The long/short overlay significantly underperforms the baseline.
2. Short exposure is too frequent relative to SPY’s structural upward bias.
3. The regime classification is not directly usable as a short signal on SPY.
4. The overlay logic amplifies losses instead of reducing risk.

---

## 8. What the Data Does NOT Support

The backtest does NOT support:

1. That LH/LL is a valid standalone short signal for SPY.
2. That adding short exposure improves performance.
3. That the current regime logic can be used as a directional strategy.
4. That this system has positive expectancy as implemented.

---

## 9. Alternative Explanations

### Finding: Negative performance
- Could be due to:
  - frequent short exposure during long-term uptrend
  - lagging weekly regime signal
  - sector-based signal not aligned with index behavior

### Finding: Increased drawdown
- Could be due to:
  - compounding losses during incorrect short periods
  - volatility mismatch between signal and execution

---

## 10. Limitations

### Data limitations
- Single asset (SPY)
- No transaction costs or short borrow costs

### Methodological limitations
- Weekly lag in signal
- No risk management layer (stop loss, sizing)
- Binary full exposure (-1, 0, +1)

### External validity limits
- Results may differ for:
  - sector rotation strategies
  - non-trending markets
  - other asset classes

---

## 11. Analytical Confidence Level

**Overall confidence: Moderate to High (for failure diagnosis)**

### Justification
- Strong and consistent negative result
- Mechanism of failure is structurally explainable
- Behavior aligns with known market bias (equity index upward drift)

---

## 12. Validation Checks Performed

### Performed
- Output files generated successfully
- Position distribution verified
- Equity curve behavior consistent with summary
- No data integrity issues detected

### Recommended
- Test reduced short exposure variants
- Test long-only overlay vs long/short side-by-side
- Apply to different asset classes (e.g., commodities)

---

## 13. Key Insight

> The market structure system is **not symmetric**:
> 
> It may support **long filtering**, but not **short generation**.

---

## 14. Interpretation Summary

- The long/short extension breaks the system
- The core issue is **misuse of regime classification as a directional signal**
- The original system remains valid as a **risk filter**, not a full trading system

---

## 15. Assumptions

| Assumption | Why | Risk |
|---|---|---|
| SPY has long-term upward drift | Empirical market behavior | Short strategies structurally disadvantaged |
| Weekly regime reflects structure | Based on earlier analysis | Lag may distort timing |
| Equal weighting of long and short | Simplifies system | Unrealistic risk symmetry |

---

## 16. Integrity Declaration

- No performance exaggeration
- Negative result reported transparently
- No attempt to optimize or hide failure
- All conclusions traceable to output data