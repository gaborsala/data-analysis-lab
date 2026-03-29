# ASK — Problem Definition

Date: 2026-03-25  
Topic/Dataset: Superstore Retail Transactions  
Owner: Gabor Sala  

---

## 1. Business Question / Problem Statement

Which product categories, sub-categories, regions, and customer segments contribute most to revenue and profitability, and where do loss-making patterns appear within the dataset?

---

## 2. Decision Context

This analysis is intended to inform:

- product portfolio review
- regional performance review
- profitability-focused business investigation

If no review is performed:

- loss-making segments may remain unidentified
- resource allocation decisions may rely on incomplete performance visibility

Accountable stakeholder:

- Business analyst / decision maker (simulated portfolio case)

Risk tolerance:

- Moderate, because findings may influence prioritization and performance review, but no live operational decisions are being executed

---

## 3. Objective

The objective of this case is to measure revenue and profit distribution across:

- categories
- sub-categories
- regions
- customer segments

And to identify:

- high-performing groups
- low-performing groups
- loss-generating patterns

Time horizon:

- Full dataset period only
- No forecasting

---

## 4. Success Criteria

- Identify the highest-contributing categories, regions, and segments by total revenue
- Detect categories, sub-categories, regions, or segments with negative total profit
- Produce reproducible aggregation tables for the main business dimensions
- Generate clear visual summaries of revenue and profit distribution
- Document data quality issues relevant to interpretation

---

## 5. Constraints

Time:
- Limited; scoped as an EDA-focused case

Scope:
- No predictive modeling
- No causal inference
- No experimentation

Data:
- Single dataset (Superstore.csv)

Resources:
- Jupyter Notebook
- Python
- pandas
- matplotlib / seaborn

Ethical:
- No personal data sensitivity issues expected based on current dataset scope

---

## 6. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|----------|------------|--------------|------------------|
| Each row represents a transaction line | Common retail dataset structure | Aggregation errors | Validate row-level structure and candidate keys |
| Profit is recorded consistently | Required for profitability analysis | Misleading conclusions | Inspect distributions and outliers |
| Dates are valid and consistently formatted | Required for any time-based grouping | Temporal distortion | Parse and validate date fields |
| Duplicate transactions are absent or limited | Needed to avoid double counting | Inflated totals | Perform duplicate check |

---

## 7. Risks to Decision Quality

Data quality risks:
- Missing or invalid values in sales, profit, category, or date fields

Measurement bias:
- Discounts may affect profitability patterns without explaining root cause

Confounding:
- Region, segment, and product mix may interact in ways that simple grouped summaries do not isolate

External validity:
- This is a portfolio dataset and may not fully represent a live operating business

Overinterpretation risk:
- EDA can identify patterns, but not causal mechanisms

---

## 8. Out of Scope

This analysis will not cover:

- forecasting future sales or profit
- causal claims such as “discount causes loss”
- operational implementation decisions
- external benchmarking against competitors or market data
- predictive modeling

---

## 9. Deliverables

Primary artifact:
- Jupyter Notebook containing validation, exploration, and visual analysis

Supporting artifacts:
- PREPARE report
- PROCESS log
- ANALYZE report
- ACT summary

Outputs:
- Aggregation tables
- Visualizations for distribution and segmentation
- Structured written findings

---

## 10. ASK Gate Checklist

- [x] Question is specific and measurable  
- [x] Decision context is defined  
- [x] Objective is precise and bounded  
- [x] Success criteria are observable  
- [x] Constraints are acknowledged  
- [x] Assumptions are documented and testable  
- [x] Risks are identified  
- [x] Scope is clearly bounded  
- [x] No solution bias introduced  
- [x] Next stage allowed (PREPARE)  

---

## 11. Integrity Declaration

- No data was consulted prior to defining the question
- No hidden assumptions were intentionally embedded
- No recommendations were made before analysis
- Scope is explicitly bounded
- Decision criteria were defined before exploration