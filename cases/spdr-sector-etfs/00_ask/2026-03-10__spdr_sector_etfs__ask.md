# ASK — Problem Definition

Date: 2026-03-10  
Topic/Dataset: SPDR Sector ETFs  
Owner: Gabor Sala  

---

## 1. Business Question / Problem Statement

Should sector allocation be adjusted within the SPDR sector ETF universe based on measurable differences in historical return dispersion and volatility structure over a defined time window?

Scope:
- Population: SPDR sector ETFs
- Metric: Return distribution, volatility metrics, cross-sector dispersion
- Time frame: To be confirmed in PREPARE (dependent on dataset range)

This question is testable using historical price data.

---

## 2. Decision Context

Decision to be informed:
Whether systematic sector overweight/underweight decisions are defensible based on measurable structural differences.

If no action is taken:
Capital remains equally allocated or passively allocated.

Accountable party:
Portfolio allocator / analyst (Owner).

Acceptable risk level:
Moderate — evidence must be statistically defensible but exploratory analysis acceptable.

---

## 3. Objective

- Measure historical return characteristics of each sector ETF.
- Quantify volatility and dispersion across sectors.
- Compare sector-level behavior across identical time horizons.
- Identify structural differences in distributional properties.

No recommendation or allocation bias introduced at this stage.

---

## 4. Success Criteria (Mandatory & Measurable)

Analysis is considered useful if it:

- Quantifies return and volatility metrics for all sectors.
- Identifies statistically significant differences (if applicable) at p < 0.05.
- Explains ≥60% of cross-sectional variance in dispersion drivers (if modeling applied).
- Provides reproducible evidence traceable to processed dataset.

Acceptable margin of uncertainty:
Clearly reported confidence intervals or statistical significance levels.

---

## 5. Constraints

Time limitations:
Single-session exploratory cycle.

Scope boundaries:
- Historical data only.
- No macro overlays.
- No forecasting beyond dataset range.

Data availability limits:
Dependent on dataset completeness inside ZIP archive.

Resource limitations:
Local processing environment.

Ethical / compliance constraints:
Publicly available market data assumed.

---

## 6. Assumptions (Explicit and Testable)

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|------------|-------------|---------------|-----------------|
| Dataset contains historical price data | Based on dataset title | Inability to compute returns | Schema validation in PREPARE |
| Data frequency is consistent | Required for comparability | Distorted volatility estimates | Timestamp consistency check |
| ETFs represent full sector coverage | SPDR standard structure | Biased dispersion estimate | Verify sector completeness |

All assumptions testable in PREPARE.

---

## 7. Risks to Decision Quality

Data quality risks:
Missing timestamps or price fields.

Measurement bias risk:
Using adjusted vs unadjusted prices inconsistently.

Confounding risk:
Macro regime shifts embedded in dataset.

External validity risk:
Past structure may not generalize.

Overfitting risk:
If modeling cross-sectional drivers.

---

## 8. Out-of-Scope (Explicit Exclusions)

This analysis will NOT cover:

- Long-term forecasting
- Macroeconomic causal drivers
- Tactical trading signals
- Intraday data
- Transaction cost modeling

---

## 9. Deliverables

Primary artifact:
Full lifecycle chain (ASK → ACT).

Supporting artifacts:
- Structural summary tables
- Statistical comparison tables
- Evidence traceability table

Expected stage outputs:
PREPARE structural audit → PROCESS cleaning log → ANALYZE statistical findings → ACT allocation implications.

Format:
Repository-compliant markdown artifacts.

---

## 10. ASK Gate Checklist

✔ Question specific and measurable  
✔ Decision context defined  
✔ Objective precise and unbiased  
✔ Success criteria quantifiable  
✔ Constraints acknowledged  
✔ Assumptions documented and testable  
✔ Risks identified  
✔ Scope clearly bounded  
✔ No solution bias introduced  
✔ Next stage allowed (PREPARE)

---

## 11. Integrity Declaration

No data consulted prior to defining the question.  
No hidden assumptions introduced.  
No recommendations embedded.  
Scope explicitly bounded.  
Decision criteria defined before analysis.