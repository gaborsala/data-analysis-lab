# ASK — Problem Definition

Date: 2026-03-15  
Topic/Dataset: Hungarian Inflation-Linked Government Bond vs Alternative Investments  
Owner: Data Analysis Lab Case Study

---

# 1. Business Question / Problem Statement

Should an investor holding a Hungarian inflation-linked government bond (e.g., 2033/I series) **sell the bond early (paying a 1% redemption fee)** and reallocate capital to alternative assets (sector ETFs or equities) **in order to achieve a higher expected annual return than the bond's inflation-adjusted yield (~5% annually)?**

Scope:

Population:
- Hungarian inflation-linked government bond holders

Metric of interest:
- Annualized return (%)

Time horizon:
- Medium-term investment horizon (12–36 months)

Decision to be informed:
- Hold the bond vs redeem and allocate capital to alternative investments.

---

# 2. Decision Context

Decision impacted:

Capital allocation between:

- Inflation-protected government bonds
- Equity sector ETFs
- Individual equities

If no action is taken:

Capital remains invested in the inflation-linked bond until maturity or later redemption.

Accountable decision-maker:

Investor / portfolio manager.

Acceptable risk level:

Moderate.

The decision trades off **capital protection vs higher return potential**.

---

# 3. Objective

Measure whether **historical and current market conditions provide evidence that reallocating capital from the inflation-linked bond to equity sector investments can reasonably exceed a 5% annual return threshold.**

Specifically:

- Compare bond real return vs equity sector return distribution.
- Estimate probability that equity investments exceed 5% annualized return.
- Evaluate volatility and drawdown risks relative to bond returns.

---

# 4. Success Criteria (Mandatory & Measurable)

The analysis is considered useful if it can:

1. Estimate probability that alternative investments exceed 5% annualized return.
2. Quantify volatility and drawdown risk for alternatives.
3. Identify whether historical evidence shows ≥5% return achievable with moderate risk.

Minimum statistical thresholds:

- Minimum sample period: ≥10 years (if available)
- Probability estimate confidence interval reported
- Volatility and drawdown metrics calculated

---

# 5. Constraints

Time constraints:
- Analytical project intended as portfolio case study.

Scope boundaries:

This analysis will examine:

- Historical market data
- Inflation and interest rate environment
- Equity sector performance

Data limitations:

Future market returns cannot be predicted with certainty.

Resource limitations:

Only publicly available datasets will be used.

Ethical constraints:

None.

---

# 6. Assumptions (Explicit and Testable)

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
Bond real return ≈ 5% annually | Based on current bond structure | Inflation adjustment differs | Verify bond formula and historical inflation |
Equity returns historically exceed 5% | Based on long-term market returns | Sample period bias | Compare multiple time windows |
Sector ETFs represent investable alternatives | Proxy for market exposure | Individual stock selection differs | Sensitivity analysis |
Transaction cost ≈ 1% | Redemption cost assumption | Cost differs by platform | Validate with bond redemption rules |

---

# 7. Risks to Decision Quality

Data quality risks:

- ETF data gaps
- Bond yield misinterpretation
- Inflation calculation differences

Measurement bias:

Using US ETFs as proxy for global equities.

Confounding risk:

Market regimes (high inflation vs low inflation).

External validity risk:

Past performance may not represent future performance.

Overfitting risk:

Small time window analysis.

---

# 8. Out-of-Scope (Explicit Exclusions)

This analysis will NOT include:

- Precise market timing models
- Short-term trading strategies
- Prediction of future inflation
- Personalized financial advice
- Portfolio optimization algorithms

---

# 9. Deliverables

Primary artifact:

Full lifecycle analysis following the repository architecture:

ASK → PREPARE → PROCESS → ANALYZE → ACT

Supporting outputs:

Dataset documentation

Statistical analysis tables

Sector ETF performance comparison

Return probability estimation

Expected format:

Markdown artifacts following repository standards.

Lifecycle discipline enforced as defined in repository governance. :contentReference[oaicite:0]{index=0}

---

# 10. ASK Gate Checklist

- [x] Question specific and measurable  
- [x] Decision context defined  
- [x] Objective precise and unbiased  
- [x] Success criteria quantifiable  
- [x] Constraints acknowledged  
- [x] Assumptions documented and testable  
- [x] Risks identified  
- [x] Scope clearly bounded  
- [x] No solution bias introduced  

Next stage allowed: **PREPARE**

---

# 11. Integrity Declaration

No dataset inspected prior to defining the analytical question.

No recommendations embedded in the problem definition.

All assumptions explicitly stated.

Decision criteria defined prior to analysis.

Structure follows lifecycle governance. :contentReference[oaicite:1]{index=1}