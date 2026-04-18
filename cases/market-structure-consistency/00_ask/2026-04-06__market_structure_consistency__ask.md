# ASK — Problem Definition (v1.1 Precision Hardened)

Date: 2026-04-06  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer)  
Owner: Gabor Sala  

---

## 1. Business Question / Problem Statement

Should the current Market Structure classification system be considered reliable for decision support, based on its historical consistency, persistence, and transition behavior across SPDR sector ETFs relative to SPY over the period 2010–present?

---

## 2. Decision Context

This analysis informs:

- Whether the Market Structure Brief outputs can be trusted as a stable analytical framework
- Whether additional validation layers (e.g., confidence scoring) are required before scaling usage

If no action is taken:

- The system may be used without understanding its reliability limits
- Structural classifications may be misinterpreted as stable signals

Accountable party:
- Repository owner (Gabor Sala)

Acceptable risk level:
- Moderate

Rationale:
- This is a portfolio-facing analytical system; incorrect conclusions reduce credibility but do not create direct financial loss

---

## 3. Objective

Quantify the historical behavior of Market Structure classifications by:

- Measuring persistence (duration) of structural states (e.g., HH/HL, LH/LL, TRANSITION)
- Measuring transition frequency between structural states
- Comparing recent structure behavior to historical baseline patterns

Time horizon:
- Full available historical dataset (expected: 2010–present)

Comparison structure:
- Cross-sector comparison (XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY, XLC, XLRE)
- State-based comparison (HH/HL vs LH/LL vs TRANSITION)

No recommendations or predictions included at this stage.

---

## 4. Success Criteria (Mandatory & Measurable)

The analysis is considered successful if it produces:

1. Persistence Metrics:
   - Average and median duration of each structural state per sector
   - Minimum threshold: computed for ≥95% of observations

2. Transition Matrix:
   - Frequency and percentage of transitions between all structural states
   - Coverage: all state combinations observed in dataset

3. Consistency Assessment:
   - Quantified comparison between recent (last 12 weeks) vs historical averages
   - Defined deviation metric (e.g., % difference)

4. Data Integrity:
   - ≥98% valid classification coverage after processing
   - No undocumented data loss

No statistical significance requirement assumed at this stage (descriptive analysis).

---

## 5. Constraints

Time limitations:
- Target completion within current Now Zone 2 phase

Scope boundaries:
- No return-based backtesting
- No predictive modeling
- No strategy optimization

Data availability limits:
- Dependent on ETF historical price availability (yfinance / stooq fallback)

Resource limitations:
- Single analyst execution
- Local compute environment

Ethical / compliance constraints:
- No financial advice generation
- No investment recommendation claims

---

## 6. Assumptions (Explicit and Testable)

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|------------|------------|--------------|-----------------|
| Historical ETF price data is sufficiently complete | Required for time-series continuity | Missing periods bias persistence metrics | Missingness analysis in PREPARE |
| Classification logic is stable across time | Same rules applied historically | Inconsistent classification invalidates comparison | Re-run classification on full dataset |
| Weekly aggregation is appropriate for structure detection | Matches current system design | Misalignment with true structure duration | Sensitivity check (daily vs weekly) |
| Structural states are mutually exclusive per observation | Required for transition matrix | Overlapping states distort transitions | Validation rule in PROCESS |

---

## 7. Risks to Decision Quality

Data quality risks:
- Missing ETF data
- Inconsistent time alignment across sectors

Measurement bias risk:
- Classification rules may introduce systematic lag

Confounding risk:
- Market regime changes (e.g., crisis periods) affecting comparability

External validity risk:
- Findings limited to SPDR sector ETF universe

Overfitting risk:
- Not applicable (no modeling)

---

## 8. Out-of-Scope (Explicit Exclusions)

This analysis will NOT cover:

- Return prediction or performance forecasting
- Strategy backtesting
- Alpha generation
- Individual stock-level analysis
- Intraday structure analysis

---

## 9. Deliverables

Primary artifact:
- 03_ANALYZE/2026-04-06__market_structure_consistency__analysis.md

Supporting artifacts:
- 01_PREPARE/2026-04-06__market_structure_consistency__prepare.md
- 02_PROCESS/2026-04-06__market_structure_consistency__process_log.md

Expected outputs:
- Persistence tables
- Transition matrices
- Comparative summaries (recent vs historical)

Format requirements:
- Markdown artifacts (repository standard)
- Reproducible tables derived from processed dataset

---

## 10. ASK Gate Checklist

- [x] Question specific and measurable  
- [x] Decision context defined  
- [x] Objective precise and unbiased  
- [x] Success criteria quantifiable  
- [x] Constraints acknowledged  
- [x] Assumptions documented and testable  
- [x] Risks identified  
- [x] Scope clearly bounded  
- [x] No solution bias introduced  
- [x] Next stage allowed (PREPARE)  

---

## 11. Integrity Declaration

- No data consulted prior to defining the question  
- No hidden assumptions  
- No embedded recommendations  
- Scope explicitly bounded  
- Decision criteria defined before analysis  