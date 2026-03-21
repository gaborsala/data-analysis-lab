# Data Analysis Lab

A structured repository for end-to-end financial data analysis case studies.

This project demonstrates how datasets move through a complete analytical lifecycle:

**ASK → PREPARE → PROCESS → ANALYZE → ACT**

Each case study documents the full reasoning process, data transformations, and outputs required to move from raw data to a decision-oriented conclusion.

The goal is to demonstrate **deterministic, reproducible analytical workflows**, similar to those used in professional data analyst and financial research roles.

For a detailed explanation of the framework:

→ `docs/ANALYTICAL_METHOD.md`

---

# Repository Structure

```
data-analysis-lab/
│
├─ cases/
│  ├─ spdr-sector-etfs/
│  │   ├─ 00_ask/
│  │   ├─ 01_prepare/
│  │   ├─ 02_process/
│  │   ├─ 03_analyze/
│  │   ├─ 04_act/
│  │   └─ outputs/
│  │
│  └─ hungarian-inflation-bond-vs-alternatives/
│      ├─ 00_ask/
│      ├─ 01_prepare/
│      ├─ 02_process/
│      ├─ 03_analyze/
│      ├─ 04_act/
│      └─ outputs/
│
├─ data/
│  ├─ archive/
│  ├─ interim/
│  ├─ processed/
│  ├─ raw/              # (not fully tracked – see reproducibility note)
│  └─ README.md
│
├─ docs/
│  ├─ templates/
│  ├─ ANALYTICAL_METHOD.md
│  └─ RUN_GUIDE.md
│
├─ learning/
│  └─ cheatsheets/
│
├─ src/
│  ├─ adhoc/
│  ├─ cases/
│  └─ common/
│
├─ README.md
├─ LICENSE
└─ requirements.txt
```

---

# Analytical Lifecycle

Each case follows the same structured workflow.

## 1. ASK

Define the analytical problem:

* What question is being answered?
* What decision depends on this analysis?
* What dataset is required?

Output: clearly defined analytical objective.

---

## 2. PREPARE

Validate dataset structure before transformation:

* schema checks
* missing values
* duplicates
* date parsing
* column validation

Output: dataset ready for processing.

---

## 3. PROCESS

Transform raw data into analysis-ready format:

* cleaning inconsistencies
* aligning time series
* normalization
* merging datasets

All transformations are explicitly logged.

---

## 4. ANALYZE

Perform structured analysis:

* return calculations
* volatility analysis
* correlation structure
* benchmark comparison
* structural pattern detection

Outputs include:

* tables
* logs
* charts

---

## 5. ACT

Translate analysis into decision-level output:

* structural observations
* risk interpretation
* benchmark comparison
* limitations

This phase connects data analysis to decision-making.

---

# Case Studies

## 1. SPDR Sector ETFs

Analyzes relative performance of US sector ETFs.

Includes:

* sector dispersion analysis
* volatility regimes
* correlation with SPY
* structural leadership classification

This case demonstrates **cross-sectional market structure analysis**.

---

## 2. Hungarian Inflation Bond vs Alternatives

Evaluates inflation-linked bonds against alternative investments.

Includes:

* CPI integration
* real return calculation
* benchmark comparison logic
* scenario-based analysis

This case demonstrates **macro + investment decision modeling**.

---

# Code Organization

## src/common/

Reusable components:

* data validation
* I/O utilities
* shared transformations

---

## src/cases/

Case-specific pipeline logic.

Example:

```
src/cases/hungarian-inflation-bond-vs-alternatives/
```

Contains:

* prepare scripts
* process pipelines
* analysis runners
* act-stage logic

---

## src/adhoc/

Temporary scripts used during development.

Not part of the core pipeline.

---

# Reproducibility

This repository focuses on **structural reproducibility**, not raw data distribution.

Important:

* Some raw datasets are not included
* Processed outputs and final artifacts are tracked
* Each phase is documented in Markdown
* Python pipelines mirror the documented lifecycle

---

## Environment Setup

Install dependencies:

```
pip install -r requirements.txt
```

---

## Example Run (Hungarian Case)

```
python src/cases/hungarian-inflation-bond-vs-alternatives/process/run_process_full.py
python src/cases/hungarian-inflation-bond-vs-alternatives/analyze/run_analyze_full.py
```

---

# Purpose

This repository demonstrates:

* structured analytical thinking
* reproducible data pipelines
* financial data analysis
* decision-oriented reporting

It is designed as a **portfolio project for data analyst / financial analyst roles**.

---

# License

This project is licensed under the MIT License.
