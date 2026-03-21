PROCESS — Cleaning & Transformation Log (v1.1 Hardened)

Date: YYYY-MM-DD
Topic/Dataset: <topic>
Input snapshot: <file version / hash / commit ref>

1. Purpose

Document all transformations required to make the dataset reliable and analytically usable.

All changes must be:

Explicit

Justified

Validated

Reproducible

No silent filtering allowed.

2. Dataset Snapshot Integrity

Before any transformation:

Row count (raw):

Column count (raw):

File hash or version reference:

Load errors encountered (Yes/No):

This section anchors reproducibility.

3. Transformation Summary Table (Mandatory)
Metric	Before	After	Change	Justification
Row count				
Column count				
Missing value count				

If row count changes → explanation mandatory.

If rows removed without documented justification → PROCESS invalid.

4. Chronological Change Log
Step	Change	Rationale	Method (rule/code)	Validation Result

Each transformation must:

Describe exactly what changed

Provide rule or logic applied

State validation result

Vague entries are prohibited.

5. Missing Value Handling

For each affected column:

Missing % before:

Strategy applied:

Rationale:

Sensitivity risk:

Missing % after:

No imputation without explicit justification.

If dropping rows → quantify impact.

6. Type Corrections

For each corrected column:

Original observed type:

Corrected type:

Why required:

Risk if misclassified:

Validation performed:

Type changes must be traceable to PREPARE schema.

7. Deduplication Rules

Duplicate detection logic:

Criteria for removal:

Rows removed (count and %):

Validation of uniqueness after removal:

No deduplication without rule transparency.

8. Outlier / Extreme Value Treatment

If applicable:

Detection method:

Threshold definition:

Treatment applied (none / capped / removed / transformed):

Justification:

Sensitivity analysis performed? (Yes/No):

Outlier handling must not artificially strengthen findings.

9. Statistical Sanity Checks

Distribution before vs after:

Unexpected variance reduction? (Explain)

Mean / median shifts due to cleaning:

Integrity check on key metrics:

If distribution shifts materially → justification required.

10. Validation Checks

Row counts verified after each major step (Yes/No):

Range checks performed:

Constraint validation (e.g., no negative quantities where impossible):

Referential integrity checks (if applicable):

Random manual spot-check performed (Yes/No):

Validation results must be explicitly stated.

11. Reproducibility

Script location:

Version reference:

Deterministic steps confirmed (Yes/No):

Manual steps performed? (If yes, describe clearly):

If transformation cannot be reproduced → PROCESS invalid.

12. Remaining Data Quality Issues

For each unresolved issue:

Issue description:

Impact on analysis:

Risk level (Low/Moderate/High):

Mitigation plan in ANALYZE:

No hidden data debt.

13. PROCESS Gate Checklist

 Raw snapshot documented

 All transformations logged

 Row changes justified

 Validation performed and recorded

 No silent filtering

 No undocumented assumptions

 Remaining issues acknowledged

 Reproducibility confirmed

 Next stage allowed (ANALYZE)

14. Integrity Declaration

Cleaning choices do not artificially strengthen results

No selective filtering performed

No undocumented transformations applied

All changes reproducible

Data integrity preserved