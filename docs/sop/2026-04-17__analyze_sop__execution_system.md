# ANALYZE — EXECUTION SOP (v1.0)

Date: 2026-04-17  
Stage: ANALYZE  
Purpose: Deterministic extraction of evidence from processed data  

---

## 0. PURPOSE

This SOP defines the **exact execution steps** required to complete the ANALYZE phase.

Goal:
- transform processed data into structured, defensible evidence
- ensure all claims are traceable to data
- prevent interpretation beyond what data supports

---

## 1. CORE PRINCIPLE

ANALYZE is not storytelling.

ANALYZE is:

> **Evidence generation with explicit traceability**

Every statement must answer:
- What is the evidence?
- Where does it come from?
- How strong is it?

---

## 2. EXECUTION FLOW (STRICT ORDER)

Follow steps sequentially. Do not skip.

---

## STEP 1 — RE-STATE QUESTIONS

### Action

Copy directly from ASK / PREPARE:

- List each question explicitly

---

### Validation

- [ ] All questions trace back to ASK
- [ ] No new questions introduced

---

### Stop Condition

If new question appears → justify or remove

---

## STEP 2 — LOAD PROCESSED DATA

### Action

```python
import pandas as pd

df = pd.read_csv(PROCESSED_PATH)
df.head()
Validation
 Matches PROCESS output
 No missing critical columns
STEP 3 — BUILD CORE DESCRIPTIVE STATISTICS
Action
df.describe()
Extend with:
df.groupby("group_column")["metric"].agg(["mean", "median", "std", "count"])
Write
Key metrics
Distribution overview
Segment summaries
Validation
 Metrics reproducible
 Values make sense
STEP 4 — SEGMENTATION / COMPARISON
Action

Compare groups:

group_means = df.groupby("group")["metric"].mean()
Compute
absolute difference
percentage difference
Write
Observed differences
Effect size (if relevant)
Rules
No interpretation beyond measured difference
Validation
 Comparisons correctly computed
 No inflated language
STEP 5 — RELATIONSHIP ANALYSIS
Action
df.corr(numeric_only=True)
If needed:

Regression:

# example (conceptual)
Write
Variables tested
Method used
Strength (e.g., correlation coefficient)
Statistical significance (if available)
Rules
Correlation ≠ causation
No causal language unless proven
Validation
 Relationship clearly defined
 Limitations acknowledged
STEP 6 — BUILD EVIDENCE TRACEABILITY
Action

For each claim:

Create mapping:

| Claim | Evidence (table/metric) | Strength | Alternative Explanation |

Validation
 Every claim has evidence
 No unsupported statements
Stop Condition

If claim cannot be mapped → REMOVE

STEP 7 — WHAT THE DATA SUPPORTS
Action

Write:

clear, evidence-based statements
strictly derived from computed results
Validation
 Statements traceable to data
 No speculation
STEP 8 — WHAT THE DATA DOES NOT SUPPORT
Action

Explicitly state:

claims that cannot be made
causal relationships not proven
limits of analysis
Validation
 At least 2–3 limitations stated
 Prevents overinterpretation
STEP 9 — ALTERNATIVE EXPLANATIONS
Action

For each major finding:

list possible confounders
competing hypotheses
Validation
 Alternatives considered
 Not ignored
STEP 10 — LIMITATIONS
Action

List:

data limitations
methodological limits
external validity issues
Validation
 Clearly stated
 Not hidden
STEP 11 — ANALYTICAL CONFIDENCE
Action

Assign:

Low
Moderate
High
Based on:
data quality
sample size
method robustness
Write justification
Validation
 Confidence level justified logically
3. HARD RULES (CRITICAL)

Forbidden:

Causal language without identification method
Selective reporting
Ignoring conflicting evidence
Claims without traceability
Causality Rule

If using words like:

causes
drives
impacts

Then MUST include:

identification method
explanation of alternative elimination

Otherwise → downgrade to association

4. ASSUMPTIONS
PROCESS output is reliable
Metrics computed correctly
Dataset represents population adequately
5. LIMITATIONS
Observational analysis cannot prove causality
Results sensitive to cleaning decisions
External validity may be limited
6. RECOMMENDED VALIDATION ACTIONS
Recompute key metrics manually
Cross-check group comparisons
Validate correlations with subset samples
Ensure consistency across tables
7. INTEGRITY DECLARATION
No conclusions beyond evidence
No causal overstatement
No selective reporting
All claims traceable
8. SUCCESS CONDITION

ANALYZE is successful when:

A third party can:

trace every claim to data
understand how results were computed
see both strengths and limitations
trust that no overstatement occurred