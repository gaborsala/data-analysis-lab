# PROCESS — EXECUTION SOP (v1.0)

Date: 2026-04-17  
Stage: PROCESS  
Purpose: Deterministic, auditable data cleaning and transformation  

---

## 0. PURPOSE

This SOP defines the **exact execution steps** required to complete the PROCESS phase.

Goal:
- convert raw data into reliable analytical dataset
- ensure all transformations are explicit, justified, and reproducible
- eliminate silent errors and undocumented changes

---

## 1. CORE PRINCIPLE

PROCESS is not “cleaning casually”.

PROCESS is:

> **Controlled transformation with full traceability**

Every change must answer:
- What changed?
- Why?
- How validated?

---

## 2. EXECUTION FLOW (STRICT ORDER)

Follow steps sequentially. Do not skip.

---

## STEP 1 — SNAPSHOT BASELINE (RAW STATE)

### Action

```python
import pandas as pd

df = pd.read_csv(PATH)

df.shape
df.dtypes
Write
Raw row count
Raw column count
File reference (path / version)
Validation
 Matches PREPARE stage
 No load errors
Stop Condition

If mismatch with PREPARE → investigate BEFORE proceeding

STEP 2 — DEFINE CLEANING PLAN (BEFORE EDITING)
Action

Based on PREPARE, list:

Missing value strategy
Type corrections
Duplicate handling
Outlier handling
Write

Simple plan:

Column X → drop / impute
Column Y → convert type
Duplicates → remove based on rule
Validation
 Plan exists BEFORE any change
 Each action justified
STEP 3 — APPLY TRANSFORMATIONS (ONE-BY-ONE)
Rule

⚠️ NEVER apply multiple changes at once

Example
df = df.dropna(subset=["sales"])
Immediately log:
Step number
Change description
Rationale
Code used
Validation
 Change documented BEFORE next step
STEP 4 — VALIDATE AFTER EACH CHANGE
Action
df.shape
df.isna().sum()
Check
Row count change
Missingness change
Unexpected data loss
Write
Before vs after
Impact of change
Stop Condition

If unexpected change → revert and investigate

STEP 5 — MISSING VALUE HANDLING
Action

For each column:

df["col"].isna().sum()
Apply strategy
drop rows
fill values
leave as-is (if justified)
Write
Missing % before
Strategy used
Reason
Risk introduced
Validation
 Missingness reduced OR justified
 Impact quantified
STEP 6 — TYPE CORRECTIONS
Action
df["date"] = pd.to_datetime(df["date"])
df["value"] = df["value"].astype(float)
Write
Original type
New type
Why required
Validation
df.dtypes
 Conversion successful
 No unintended coercion
STEP 7 — DEDUPLICATION
Action
df.duplicated().sum()

If removing:

df = df.drop_duplicates(subset=["key_columns"])
Write
Rule used
Rows removed (count + %)
Validation
 No duplicates remain
 Rule is logical
STEP 8 — OUTLIER / EXTREME VALUE HANDLING
Action
df.describe()
Decide
keep
cap
remove
Write
Detection method
Threshold
Action taken
Justification
Validation
 No artificial distortion
 Changes explained
STEP 9 — STATISTICAL SANITY CHECK
Action
df.describe()
Compare
Before vs after distributions
Mean / median shifts
Write
Any major changes
Whether expected
Validation
 No unexplained shifts
 Key metrics stable unless justified
STEP 10 — FINAL VALIDATION
Checklist
 Row counts tracked across steps
 No negative/impossible values remain
 Constraints satisfied
 Random spot-check performed
Optional
df.sample(5)
STEP 11 — REPRODUCIBILITY CHECK
Action
Ensure all steps can be rerun
No manual edits
Write
Script location
Version reference
Validation
 Deterministic execution confirmed
3. HARD RULES (CRITICAL)

Forbidden:

Silent filtering
Undocumented row deletion
Hidden assumptions
“Cleaning to improve results”
If violated → PROCESS is INVALID

(Aligned with PROCESS governance rules)

4. ASSUMPTIONS
PREPARE stage correctly identified issues
Dataset size manageable in memory
Transformations can be applied in pandas
5. LIMITATIONS
Cleaning choices may influence results
Some decisions subjective (e.g., outliers)
No guarantee all data issues resolved
6. RECOMMENDED VALIDATION ACTIONS
Save intermediate snapshots (optional)
Compare raw vs processed distributions
Log all transformations in chronological order
Re-run script from scratch to confirm reproducibility
7. INTEGRITY DECLARATION
All transformations explicitly documented
No selective filtering performed
No undocumented assumptions introduced
Data integrity preserved
8. SUCCESS CONDITION

PROCESS is successful when:

A third party can:

reproduce the dataset exactly
understand every transformation
verify that no hidden manipulation occurred