ANALYZE — Findings (v1.1 Hardened)

Date: YYYY-MM-DD
Topic/Dataset: <topic>

1. Questions Answered

Directly derived from ASK and refined in PREPARE.

List each question explicitly.

No new questions introduced without justification.

2. Descriptive Statistics

Provide structured summaries:

Key metrics (mean, median, std, counts)

Distribution overview

Segment-level summaries (if applicable)

Include table references.

Example structure:

Metric	Value	Notes

All statistics must be reproducible from PROCESS output.

3. Segmentation / Comparisons

Groups compared:

Metrics evaluated:

Observed differences:

Effect size (if applicable):

Statistical test used (if applicable):

No interpretive inflation beyond measured difference.

4. Relationship Exploration (Non-Causal Unless Proven)
Variables	Method	Strength	Statistical Significance	Notes

If correlation:

State correlation coefficient

State p-value (if available)

State limitations

If regression:

State model type

State assumptions

State goodness-of-fit metrics

Causal language prohibited unless identification method specified.

5. Causality Gate (Mandatory)

If using words such as:

causes

drives

impacts

leads to

You must explicitly state:

Identification method (experiment / natural experiment / time precedence / control variables)

Why alternative explanations are ruled out

If not satisfied → downgrade to association language.

Correlation ≠ causation must be acknowledged when relevant.

6. Evidence Traceability Table (Mandatory)

All major claims must be mapped.

Claim	Evidence Reference (table/metric/test)	Strength of Evidence	Alternative Explanation Considered
			

If a claim cannot be mapped → it must be removed.

7. What the Data Supports

Explicit, evidence-based statements.

No speculation.

8. What the Data Does NOT Support

Explicitly state:

Claims that cannot be made

Causal relationships not proven

Performance conclusions unsupported by data

Forecasting limits

This section is mandatory.

9. Alternative Explanations

For each major finding:

Possible confounders:

Data limitations affecting interpretation:

Competing hypotheses:

If none identified → explain why.

10. Limitations

Data limitations:

Methodological limitations:

External validity limits:

Sensitivity to assumptions:

Limitations must not be hidden in narrative.

11. Analytical Confidence Level

Overall confidence in findings:

Low

Moderate

High

Justification required based on:

Data quality

Sample size

Method robustness

Validation strength

12. ANALYZE Gate Checklist

 Questions trace to ASK

 Statistics reproducible from PROCESS

 Claims mapped to evidence

 Causality not overstated

 Alternative explanations considered

 Limitations acknowledged

 “What data does NOT support” section completed

 Analytical confidence justified

 Next stage allowed (ACT)

13. Integrity Declaration

No conclusions beyond evidence

No causal claims without identification

No selective reporting

All major claims traceable

Uncertainty explicitly acknowledged