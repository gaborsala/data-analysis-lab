# Data Analysis Lab

A **process-driven data analysis portfolio** demonstrating how raw datasets are transformed into structured, evidence-based insights.

This repository focuses on **analytical discipline, reproducibility, and decision-oriented thinking**.

---

## Core Framework

All case studies follow a consistent lifecycle:

**ASK → PREPARE → PROCESS → ANALYZE → ACT**

Each phase is explicitly documented to reflect real-world analytical workflows.

The goal is not to showcase tools, but to demonstrate **how analytical systems are designed and executed in a controlled, reproducible manner**.

---

## Repository Architecture (System Design)

This repository is structured as a layered analytical system to ensure clarity, reproducibility, and disciplined execution.

### Layers

- **Framework (WHY)**  
  `docs/framework/`  
  High-level analytical methodology and lifecycle explanation  

- **Governance (RULES)**  
  `docs/governance/`  
  Defines lifecycle constraints, naming conventions, and quality gates  

- **Execution SOP (HOW — analytical)**  
  `docs/sop/`  
  Step-by-step procedures for executing each lifecycle phase  

- **Technical Execution (HOW — environment)**  
  `docs/setup/`  
  Instructions for running pipelines and scripts  

- **Templates (WHAT)**  
  `docs/templates/`  
  Standardized output formats for each lifecycle stage  

---

### Lifecycle Enforcement

All work follows a strict sequence:

**ASK → PREPARE → PROCESS → ANALYZE → ACT**

Rules:
- No stage skipping  
- No mixing of stages  
- No interpretation before validation  
- No recommendation without evidence  

---

### Key Principle

- Templates define **WHAT** to produce  
- SOP defines **HOW** to produce it  
- Governance defines **RULES**  
- Framework explains **WHY**

This separation ensures that analytical work is:

- reproducible  
- auditable  
- structurally consistent  

---

## What This Repository Demonstrates

- structured problem definition  
- rigorous data validation  
- controlled data transformation  
- clear exploratory analysis  
- disciplined interpretation (non-causal)  

---

## Getting Started

For a structured walkthrough of the system:

→ See: `docs/START_HERE.md`

Typical workflow:

1. Understand methodology → `docs/framework/`
2. Review rules → `docs/governance/`
3. Execute analysis → `docs/sop/`
4. Use templates → `docs/templates/`
5. Run code → `docs/setup/`

---

## Interactive Dashboard (V1)

The repository includes a Streamlit-based analytical dashboard:

**Energy Market Dashboard — V1**

- Built from aligned daily dataset  
- Uses consistent `close` price basis  
- Strictly descriptive (no forecasting)  
- Reproducible from pipeline outputs  

### Panels:
- Normalized Performance  
- Rolling Volatility (20-day annualized)  
- Drawdown  
- XLE / SPY Relative Strength  

Example view:

![Energy Market Dashboard](cases/energy-market-dashboard/docs/dashboard_screenshot.png)

---

## How to Read This Repository

If you are reviewing this as a recruiter or collaborator:

1. Open any case in `/cases/`
2. Follow the lifecycle:
   - `00_ask/` → problem definition  
   - `01_prepare/` → dataset validation  
   - `02_process/` → transformations  
   - `03_analyze/` → structured findings  
   - `04_act/` → interpretation and boundaries  
3. Optionally review the notebook or dashboard  

Each case is designed to be **traceable from question → conclusion**.

---

## Repository Structure


data-analysis-lab/
│
├─ cases/
│ ├─ energy-market-dashboard/
│ ├─ spdr-sector-etfs/
│ ├─ hungarian-inflation-bond-vs-alternatives/
│ ├─ retail-sales-eda/
│
├─ data/
│ ├─ raw/
│ ├─ processed/
│ ├─ interim/
│ └─ archive/
│
├─ docs/
│ ├─ framework/
│ ├─ governance/
│ ├─ sop/
│ ├─ setup/
│ └─ templates/
│
├─ src/
│ ├─ common/
│ ├─ cases/
│ └─ adhoc/
│
├─ requirements.txt
├─ LICENSE
└─ README.md


---

## Analytical Lifecycle

### 1. ASK — Problem Definition
- Define the analytical question  
- Clarify decision context  
- Establish scope and constraints  

**Output:** clearly defined objective  

---

### 2. PREPARE — Data Validation
- Schema validation  
- Missingness checks  
- Duplicate detection  
- Data integrity verification  

**Output:** validated dataset ready for transformation  

---

### 3. PROCESS — Controlled Transformation
- Minimal, explicit data transformations  
- Feature engineering where necessary  
- Preservation of raw data  

**Output:** analysis-ready dataset  

---

### 4. ANALYZE — Structured Exploration
- Aggregations and distributions  
- Comparative analysis (categories, segments, time)  
- Pattern identification  

**Outputs:**
- tables  
- charts  
- structured findings  

---

### 5. ACT — Interpretation Layer
- Translate findings into structured implications  
- Identify areas for further investigation  
- Define analytical boundaries  

**Important:**
- No causal claims  
- No forecasting  
- No overinterpretation  

---

## Case Studies

### Energy Market Dashboard
- Multi-asset analysis: Brent, WTI, Natural Gas, XLE, SPY  
- Aligned daily panel construction  
- Metric validation (`close` vs `adj_close`)  
- Interactive Streamlit dashboard  

**Focus:** cross-asset energy market structure (descriptive, non-causal)

---

### SPDR Sector ETFs
- Relative performance analysis  
- Market structure classification  
- Sector leadership dynamics  

**Focus:** cross-sectional financial analysis  

---

### Hungarian Inflation Bond vs Alternatives
- Real return comparison  
- CPI integration  
- Scenario-based evaluation  

**Focus:** macro + investment analysis  

---

### Retail Sales EDA
- Revenue and profit distribution  
- Loss concentration analysis  
- Discount–profit association  

**Focus:** transaction-level exploratory analysis  

---

## Code Organization

### `src/common/`
Reusable utilities:
- validation  
- I/O  
- shared transformations  

---

### `src/cases/`
Case-specific pipelines:
- prepare scripts  
- process pipelines  
- analysis logic  

---

### `src/adhoc/`
Temporary development scripts  
(not part of production workflow)

---

## Reproducibility

This repository emphasizes **structural reproducibility**:

- analytical steps are documented in Markdown  
- code reflects each lifecycle phase  
- raw datasets may not be included  
- outputs can be regenerated from scripts or dashboards  

---

## Environment Setup

```bash
pip install -r requirements.txt
Example Run
python src/cases/hungarian-inflation-bond-vs-alternatives/process/run_process_full.py
python src/cases/hungarian-inflation-bond-vs-alternatives/analyze/run_analyze_full.py

Run dashboard:

streamlit run cases/energy-market-dashboard/app/app.py
Purpose

This repository demonstrates:

disciplined analytical workflows
reproducible data pipelines
structured thinking under constraints
translation of analysis into decision-ready outputs

It serves as a portfolio for data analyst and financial analyst roles.

License

MIT License