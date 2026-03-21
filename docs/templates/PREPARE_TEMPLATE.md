PREPARE — Dataset Understanding (v1.1 Hardened)

Date: YYYY-MM-DD
Topic/Dataset: <topic>
Source: <source>
Time range: <...>
Rows/Cols: <...>

1. Context

Why does this dataset exist?

What real-world process generated it?

What decision context (from ASK) does it relate to?

No interpretation of performance or outcomes allowed.

2. Grain / Unit of Analysis

One row represents:

Expected unique identifier:

Potential primary key:

Aggregation level (transaction / daily / monthly / etc.):

Is grain consistent across dataset? (Yes/No — explain if No)

3. Schema
Column	Type (Observed)	Expected Type	Meaning	Valid Range	Nullable	Notes

Notes:

Observed type must reflect raw dataset.

No corrections performed here.

4. Missingness Overview

Overall missing %:

Columns with missing values:

Missingness pattern (MCAR / MAR / Structural / Unknown):

Potential analytical bias risk:

Columns with >5% missingness (if any):

No imputation or correction allowed.

5. Anomaly Scan (No Edits Performed)

Duplicate rows detected:

Out-of-range values:

Timestamp inconsistencies:

Unexpected categories:

Extreme values (initial distribution scan):

Structural inconsistencies (e.g., negative quantities where impossible):

Document only. Do not correct.

6. Data Credibility Assessment

Source reliability:

Collection method (manual / automated / derived):

Known distortions:

Data freshness:

Trust level (Low / Moderate / High) with justification:

7. Risks / Assumptions
Assumption	Why Assumed	Risk if Wrong	Detection Method
			

Assumptions must be testable in PROCESS or ANALYZE.

8. Refined Analytical Questions

Derived strictly from ASK.

Clarify scope without answering.

No directional language.

9. Interpretation Guardrail (Mandatory)

The following are prohibited in PREPARE:

“This suggests…”

“This implies…”

“This shows that…”

Performance comparisons

Causal statements

Predictive statements

Allowed:

Structural observations

Distribution description

Missingness documentation

Data integrity notes

If interpretive language appears → PREPARE is invalid.

10. Validation Checks Performed

Row count confirmed:

Column count confirmed:

Schema matches source documentation (Yes/No):

Random row spot-check performed (Yes/No):

Data load errors encountered (Yes/No):

11. PREPARE Gate Checklist

 Dataset identity documented

 Grain clearly defined

 Schema documented

 Missingness analyzed

 Anomalies recorded

 Risks documented

 No transformations performed

 No interpretive language present

 Next stage allowed (PROCESS)

12. Integrity Declaration

No data transformation performed

No assumptions hidden

No performance interpretation introduced

Observations limited to structural properties