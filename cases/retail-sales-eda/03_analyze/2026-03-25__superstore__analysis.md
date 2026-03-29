# EXPLORATORY DATA ANALYSIS

Date: 2026-03-25  
Dataset: Superstore Retail Transactions  

---

## 1. Dataset Overview

- Total rows: 9,994  
- Total columns: 21 (raw), 26 (processed)  
- Time range: 2014-01-03 → 2017-12-30  
- Unique orders: 5,009  
- Unique customers: 793  
- Unique products: 1,862  

Key metrics:

- Total sales: 2,297,200.86  
- Total profit: 286,397.02  
- Average sales per row: 229.86  
- Average profit per row: 28.66  
- Negative profit rows: 1,871  

---

## 2. Sales Distribution

Observations:

- Sales are unevenly distributed across product categories  
- High-value transactions contribute significantly to total revenue  
- Presence of large-value outliers is consistent with retail transaction data  

---

## 3. Category Performance

Sales ranking:

1. Technology  
2. Furniture  
3. Office Supplies  

Profitability:

- Technology generates the highest total profit  
- Office Supplies shows stable profitability  
- Furniture shows significantly lower profit relative to sales  

Observation:

→ Revenue and profit are not aligned across categories  

---

## 4. Sub-Category Concentration (Pareto)

Top contributors:

- Phones  
- Chairs  
- Storage  
- Tables  

Top ~20% of sub-categories contribute ~47% of total sales.

Observation:

→ Revenue is concentrated in a limited number of product groups  

---

## 5. Loss-Making Patterns

Lowest-performing sub-categories:

- Tables (largest loss contributor)  
- Bookcases  
- Supplies  

Observation:

→ Some high-revenue sub-categories are simultaneously loss-making  

---

## 6. Segment-Level Insights

Customer segments:

- Consumer (highest sales and profit)  
- Corporate  
- Home Office  

Observation:

→ Consumer segment dominates revenue contribution  

Loss concentration:

- Negative profit patterns appear across multiple segments  
- Tables show losses across all segments  

---

## 7. Regional Performance

Sales ranking:

1. West  
2. East  
3. Central  
4. South  

Observation:

- West region leads both sales and profit  
- Central region shows weaker profitability relative to sales  

---

## 8. Regional Loss Concentration

Loss-making patterns are concentrated in:

- Tables across multiple regions  
- Central region shows repeated loss patterns across sub-categories  

Observation:

→ Losses are not isolated; they are structurally distributed  

---

## 9. Discount and Profitability Association

Discount bands:

- 0–10% → positive average profit  
- 20–30% → negative average profit  
- 30%+ → strongly negative average profit  

Observation:

→ Higher discount levels are associated with lower average profitability  

Important:

→ This is a descriptive association, not a causal conclusion  

---

## 10. Correlation Analysis

Key relationships:

- Sales vs Profit: moderate positive correlation (~0.48)  
- Discount vs Profit: negative correlation (~ -0.22)  
- Quantity vs Profit: weak relationship  

Observation:

→ Discount is negatively associated with profitability  
→ Sales alone does not fully explain profit variation  

---

## 11. Time-Based Trends

- Sales show variability across months  
- Profit fluctuates more than sales  
- No structural trend conclusion is made  

Observation:

→ Temporal variability exists but is not interpreted beyond description  

---

## 12. Revenue Concentration Metrics

- Top category share: ~36%  
- Top 2 regions: ~61% of revenue  
- Top 2 segments: ~81% of revenue  

Observation:

→ Revenue is concentrated across limited dimensions  

---

## 13. Key Patterns

- Revenue concentration exists at category and sub-category level  
- Profitability is inconsistent across similar revenue levels  
- Certain sub-categories (e.g., Tables) generate persistent losses  
- Higher discounts are associated with lower profitability  
- Regional and segment distributions are uneven  

---

## 14. Data Quality Considerations

- No missing values detected  
- No duplicate rows detected  
- All date fields successfully parsed  
- Dataset is structurally consistent  

---

## 15. Interpretation Boundary

This analysis:

- Identifies patterns and associations  
- Does NOT establish causality  
- Does NOT provide forecasts  
- Does NOT prescribe business actions  

---

## 16. Summary

The dataset shows:

- Concentrated revenue across categories and segments  
- Misalignment between revenue and profitability  
- Persistent loss patterns at sub-category level  
- Negative association between discount levels and profit  

All findings are descriptive and based on observed data structure.