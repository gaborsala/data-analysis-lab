# Superstore Retail Analysis — Portfolio Case

## Overview

This case presents a **structured exploratory data analysis (EDA)** of a retail transaction dataset.

The objective is to demonstrate a **disciplined analytical workflow** focused on:

- data validation
- structured exploration
- evidence-based findings

No predictive modeling or causal claims are made.

---

## Why this project matters

Many portfolio projects:

- skip data validation
- focus only on charts
- overstate conclusions

This project demonstrates:

- full **analytical lifecycle execution**
- explicit **validation before analysis**
- strict **non-causal reasoning**
- clear, structured **business-relevant observations**

---

## Analytical Objective

This analysis addresses the following descriptive questions:

1. Which categories, regions, and segments contribute most to sales and profit?
2. Where are loss-making patterns concentrated?
3. How are discount levels associated with profitability?

---

## Dataset

- ~10,000 retail transaction rows  
- 21 original columns  
- Time range: 2014–2017  

Each row represents a **transaction line item**.

---

## Methodology

This case follows a structured lifecycle:

ASK → PREPARE → PROCESS → ANALYZE → ACT

### PREPARE (Validation)
- Schema inspection  
- Missingness check  
- Duplicate detection  
- Range validation  
- Date consistency checks  

### PROCESS (Controlled Transformation)
- Date parsing  
- Time feature extraction  
- Shipping delay calculation  
- No destructive cleaning  

### ANALYZE (Descriptive Exploration)
- Category, region, segment aggregations  
- Loss concentration analysis  
- Discount–profit association  
- Time-based trends  

### ACT (Interpretation Layer)
- Structured interpretation of findings  
- Identification of investigation areas  
- Explicit analytical boundaries  

---

## Key Findings

### Revenue and Profit Structure

- Technology leads in both sales and profit  
- Furniture shows high sales with lower profitability  

→ Revenue and profit are not aligned across categories  

---

### Loss Concentration

- 1,871 transactions (~18.7%) are loss-making  

Losses are concentrated in specific sub-categories:

- Tables (largest loss contributor)  
- Bookcases (consistent negative profit)  

→ Loss patterns are structurally concentrated  

---

### Discount vs Profit (Descriptive)

- Low discount levels → positive average profit  
- Higher discount levels → negative average profit  

→ Higher discounts are associated with lower profitability  
→ No causal interpretation is made  

---

### Regional Performance

- West leads in both sales and profit  
- Central shows weaker profitability relative to sales  

---

### Customer Segments

- Consumer segment dominates revenue and profit  
- Corporate and Home Office follow  

---

### Time-Based Behavior

- Sales and profit vary over time  
- No trend forecasting applied  

---

## What This Analysis Supports

- Identification of high-performing categories  
- Detection of loss-driving sub-categories  
- Understanding of profitability distribution  
- Structural view of regional and segment performance  

---

## What This Analysis Does NOT Support

- Causal claims  
- Forecasting  
- Pricing decisions  
- Operational recommendations  

---

## Validation Summary

- Dataset successfully loaded  
- No missing values detected  
- No duplicate rows found  
- Row ID uniqueness confirmed  
- Numeric ranges validated  
- Dates parsed successfully  
- No data loss during processing  

---

## Repository Structure


cases/retail-sales-eda/
│
├── 00_ask/
├── 01_prepare/
├── 02_process/
├── 03_analyze/
├── 04_act/
│
├── notebook/
│ └── retail_sales_eda.ipynb
│
└── outputs/
  └── retail_sales_eda.html


---

## How to Run

1. Clone repository  
2. Create virtual environment  
3. Install dependencies  
4. Place dataset in:


data/raw/Sample - Superstore.csv


5. Run the notebook top-to-bottom  

---

## Outputs

- Jupyter Notebook (full analysis)  
- HTML report (shareable)  
- Structured lifecycle artifacts  

---

## Limitations

- Static dataset  
- No external benchmarks  
- No cost structure data  
- No causal inference  

---

## Analyst Note

This project prioritizes:

- structure over complexity  
- validation over speed  
- clarity over storytelling  

The goal is to reflect **real analytical workflow standards**, not just visual output.

---

## Summary

This case demonstrates:

- disciplined data validation  
- structured exploratory analysis  
- controlled interpretation  

It is designed to reflect **practical analyst-level thinking and execution**.