# PREPARE — EXECUTION SOP (v1.0)

Date: 2026-04-17  
Stage: PREPARE  
Purpose: Deterministic dataset understanding WITHOUT transformation  

---

## 0. PURPOSE

This SOP defines the **exact execution steps** required to complete the PREPARE phase.

Goal:
- fully understand dataset structure
- identify risks BEFORE cleaning
- prevent premature interpretation

This stage is **strictly observational**.

---

## 1. CORE PRINCIPLE

PREPARE is not analysis.

PREPARE is:

> **Structural observation of data without modifying it**

---

## 2. EXECUTION FLOW (STRICT ORDER)

Follow steps sequentially. Do not skip.

---

## STEP 1 — LOAD DATASET

### Action

```python
import pandas as pd

df = pd.read_csv(PATH)
df.head()
Validation
 Data loads without error
 Columns visible
 Data preview makes sense
Stop Condition

If load fails → fix path or encoding BEFORE continuing

STEP 2 — BASIC STRUCTURE
Action
df.shape
list(df.columns)
Write
Row count
Column count
Full column list
Validation
 Dimensions documented
 Column names captured correctly
STEP 3 — GRAIN (UNIT OF ANALYSIS)
Action

Ask:

One row represents what?
transaction?
daily record?
user?
aggregated metric?
Supporting Checks
df.head(10)
df.duplicated().sum()
Write
Primary interpretation of grain
Alternative possibility (if ambiguity exists)
Potential primary key column(s)
Validation
 Grain hypothesis stated clearly
 Potential key identified
STEP 4 — SCHEMA DOCUMENTATION
Action
df.dtypes
Write (table)

For EACH column:

Observed type (as-is)
Expected type (logical)
Meaning (basic, no interpretation)
Nullable (Yes/No)
Notes
Rules
No corrections allowed
No type casting here
Validation
 All columns documented
 Observed types match raw data
STEP 5 — MISSINGNESS ANALYSIS
Action
missing = df.isna().sum()
missing_pct = (missing / len(df)) * 100
Write
Overall missing %
Columns with missing values
Columns >5% missing
Missingness pattern (guess: MCAR / MAR / Structural / Unknown)
Validation
 Missingness quantified
 High-risk columns flagged
STEP 6 — ANOMALY SCAN (NO EDITS)
Action
df.describe(include='all')
df.duplicated().sum()
Check for
Duplicate rows
Negative values where impossible
Extreme values (outliers)
Invalid categories
Timestamp inconsistencies
Write
All anomalies detected
Potential risks
Validation
 At least one anomaly check performed
 Results documented (even if none found)
STEP 7 — DATA CREDIBILITY ASSESSMENT
Action

Write:

Source reliability (low / moderate / high)
Collection method:
manual
automated
derived
Data freshness
Known distortions
Assign

Trust level:

Low
Moderate
High

With justification

Validation
 Trust level justified
 Source described
STEP 8 — RISKS & ASSUMPTIONS
Action

Create table:

| Assumption | Why Assumed | Risk if Wrong | Detection Method |

Rules
Must be testable later
Must relate to data structure
Validation
 Minimum 3 assumptions
 Detection methods defined
STEP 9 — REFINED ANALYTICAL QUESTIONS
Action

Rewrite ASK questions with better precision using:

actual columns
actual structure
Rules
No answers
No directional language
Validation
 Questions aligned with dataset
 Still measurable
STEP 10 — VALIDATION CHECKS
Perform
 Row count confirmed
 Column count confirmed
 Schema matches expectations
 Random row spot-check (manual inspection)
 No load errors
Optional Code
df.sample(5)
3. HARD STOP RULES (CRITICAL)

The following are strictly forbidden:

“This suggests…”
“This implies…”
“This shows that…”
Any performance comparison
Any conclusion or interpretation
If any appear → PREPARE is INVALID

(Aligned with PREPARE governance rules)

4. ASSUMPTIONS
Dataset is tabular and loadable via pandas
Column names are interpretable
User has basic understanding of dataset context
5. LIMITATIONS
No corrections performed → issues remain unresolved
Interpretation intentionally restricted
Some anomalies may require domain knowledge to detect
6. RECOMMENDED VALIDATION ACTIONS
Manually inspect 10–20 random rows
Compare column names to dataset description (if available)
Check if row count matches expected source size
Re-run load step to ensure reproducibility
7. INTEGRITY DECLARATION
No data transformation performed
No assumptions hidden
No performance interpretation introduced
Observations limited to structure only
8. SUCCESS CONDITION

PREPARE is successful when:

A third party can understand:

what each row represents
what each column means
what data issues exist
what risks are present

WITHOUT needing to see the raw dataset