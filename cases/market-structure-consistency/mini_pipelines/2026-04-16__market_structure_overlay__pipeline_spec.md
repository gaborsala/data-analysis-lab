# MINI PIPELINE — Market Structure Trading Overlay (v1.0)

Date: 2026-04-16  
Topic: Simple regime-based trading overlay using weekly structure classification

---

## 1. Objective

Define a minimal, testable overlay that uses Market Structure states (HH/HL, LH/LL, TRANSITION) to:

- filter trade direction
- adjust position sizing
- reduce exposure in unstable regimes

This overlay is NOT a standalone trading strategy.

---

## 2. Input Data

### Required datasets

| Dataset | Source | Purpose |
|---|---|---|
| historical_weekly_structure_classification.csv | PROCESS output | regime classification |
| SPY daily or weekly price | existing data | execution layer |

---

## 3. Core Logic

### Regime Mapping

| Direction | Interpretation | Trading Bias |
|---|---|---|
| HH/HL | upward relative strength | long bias |
| LH/LL | downward relative strength | short / defensive bias |
| TRANSITION | unstable regime | no directional edge |

---

## 4. Overlay Rules (v1.0 — Minimal)

### Rule 1 — Trade Direction Filter

```text
IF regime == HH/HL → allow LONG trades only
IF regime == LH/LL → allow SHORT trades only
IF regime == TRANSITION → NO NEW TRADES

### Rule 2 — Position Sizing

Regime	Position Size
HH/HL	100% base size
LH/LL	100% base size
TRANSITION	0% (flat) or max 25% if already in trade
Rule 3 — Exit Condition (Simple)
IF regime changes away from entry regime → exit position

Examples:

LONG opened in HH/HL → exit when TRANSITION or LH/LL appears
SHORT opened in LH/LL → exit when TRANSITION or HH/HL appears
Rule 4 — No Prediction Layer
No forecasting
No signal generation
Only filtering existing trade ideas
5. Example Workflow
Weekly structure classification is updated
Current regime is assigned
Trader evaluates setup (technical or discretionary)
Overlay filters decision:

Example:

Setup says “buy breakout”
Regime = TRANSITION
→ Trade is skipped
6. Validation Plan
Backtest (simple, honest)

Test 3 scenarios:

Scenario	Description
Baseline	strategy without overlay
Overlay	strategy with regime filter
Overlay + sizing	add position scaling

Measure:

win rate
max drawdown
trade frequency
7. Assumptions
Assumption	Why	Risk
Weekly regime reflects meaningful structure	Based on persistence + transition results	Could lag real-time shifts
TRANSITION is unstable	Supported by lower persistence (~43%)	Might still contain profitable trades
Directional regimes are usable filters	Supported by high persistence (~80%)	Could reduce opportunity too much
8. Limitations
No entry signal → depends on external strategy
Weekly lag → not suitable for intraday trading
No cost model included
No sensitivity to market volatility
9. Expected Behavior
What should improve:
fewer bad trades in unstable regimes
cleaner alignment with trend environments
What may worsen:
missed opportunities during transitions
lower trade frequency
10. Success Criteria

Overlay is useful if:

drawdown decreases
trade quality improves (not necessarily returns)
behavior becomes more consistent
11. Integrity Statement
This overlay does NOT claim alpha
It is a filtering mechanism only
All decisions remain dependent on external strategy