# ACT — EXECUTION SOP (v1.0)

Date: 2026-04-17  
Stage: ACT  
Purpose: Convert validated evidence into controlled, risk-aware decisions  

---

## 0. PURPOSE

This SOP defines the **exact execution steps** required to complete the ACT phase.

Goal:
- translate ANALYZE evidence into actionable decisions
- ensure all recommendations are justified, measurable, and monitored
- prevent overreach beyond evidence strength

---

## 1. CORE PRINCIPLE

ACT is not “giving advice”.

ACT is:

> **Decision construction constrained by evidence and uncertainty**

Every recommendation must answer:
- What evidence supports this?
- How confident are we?
- What happens if we are wrong?

---

## 2. EXECUTION FLOW (STRICT ORDER)

Follow steps sequentially. Do not skip.

---

## STEP 1 — EXTRACT VALID CONCLUSIONS

### Action

From ANALYZE:

- List ONLY statements that are:
  - supported by evidence
  - traceable to metrics/tables

---

### Validation

- [ ] Each conclusion exists in ANALYZE
- [ ] No new ideas introduced

---

### Stop Condition

If conclusion is not traceable → REMOVE

---

## STEP 2 — BUILD EVIDENCE MAPPING TABLE

### Action

Create table:

| Conclusion | Evidence Reference | Confidence | Risk if Wrong |
|-----------|-------------------|-----------|---------------|

---

### Requirements

- Evidence must point to:
  - specific table
  - metric
  - statistical test

---

### Assign Confidence

- Low → weak evidence / high uncertainty  
- Moderate → consistent evidence / some limitations  
- High → strong evidence / minimal uncertainty  

---

### Validation

- [ ] All conclusions mapped
- [ ] Confidence justified
- [ ] Risks explicitly stated

---

## STEP 3 — DEFINE RECOMMENDATIONS

### Action

For EACH conclusion:

Write:

- Action:
- Rationale (linked to conclusion):
- Expected impact:
- Evidence strength:

---

### Rules

- Must derive directly from conclusions
- No speculative ideas

---

### Validation

- [ ] Recommendation linked to evidence
- [ ] No leap beyond ANALYZE

---

### Stop Condition

If recommendation feels “intuitive” but not evidence-based → REMOVE

---

## STEP 4 — RISK & UNCERTAINTY ASSESSMENT

### Action

For each recommendation:

Write:

- Required assumption(s)
- What could invalidate it
- Sensitivity to:
  - data quality
  - external factors

---

### Validation

- [ ] At least one failure scenario identified
- [ ] Assumptions clearly stated

---

## STEP 5 — MONITORING & VALIDATION PLAN

### Action

Define:

- Key metric(s) to track
- Monitoring frequency
- Threshold for reassessment
- Trigger for rollback

---

### Example

- Metric: conversion rate
- Frequency: weekly
- Threshold: <5% drop
- Action: revert decision

---

### Validation

- [ ] Metrics measurable
- [ ] Threshold defined
- [ ] Clear trigger exists

---

### Stop Condition

If cannot monitor → downgrade recommendation strength

---

## STEP 6 — EXPECTED IMPACT

### Action

Write:

- Short-term effect
- Long-term effect
- KPI(s)
- Estimated magnitude (if defensible)

---

### Rules

- No exaggeration
- No unsupported forecasts

---

### Validation

- [ ] Impact tied to metrics
- [ ] Magnitude justified (if included)

---

## STEP 7 — IMPLEMENTATION PLAN

### Action

Define:

- Owner
- Timeline
- Dependencies
- Required data/tools
- Review checkpoint

---

### Validation

- [ ] Execution feasible
- [ ] Responsibility clear

---

## STEP 8 — SCALING & AUTOMATION (IF APPLICABLE)

### Action

Answer:

- Is repeatable pipeline required? (Yes/No)

If Yes:
- Data requirements
- Tooling requirements
- Governance considerations

---

### Validation

- [ ] Automation justified
- [ ] Requirements realistic

---

## STEP 9 — RECOMMENDATION STRENGTH CLASSIFICATION

### Action

Assign:

- Weak  
- Moderate  
- Strong  

---

### Based on:

- evidence consistency
- data quality
- risk level

---

### Validation

- [ ] Strength aligned with confidence
- [ ] No overstatement

---

## 3. HARD RULES (CRITICAL)

Forbidden:

- Recommendations without evidence
- Ignoring uncertainty
- Overstating impact
- Introducing new conclusions not in ANALYZE

---

### If violated → ACT is INVALID

---

## 4. ASSUMPTIONS

- ANALYZE stage is valid and complete
- Evidence mapping is accurate
- Decision context remains unchanged

---

## 5. LIMITATIONS

- Recommendations depend on data quality
- External conditions may invalidate results
- Implementation feasibility may vary

---

## 6. RECOMMENDED VALIDATION ACTIONS

- Re-check evidence mapping manually
- Challenge each recommendation:
  - “What if I’m wrong?”
- Ensure monitoring plan is realistic
- Verify no hidden assumptions

---

## 7. INTEGRITY DECLARATION

- All conclusions trace to ANALYZE
- No causal overstatement introduced
- No recommendation exceeds evidence strength
- Risks explicitly acknowledged

---

## 8. SUCCESS CONDITION

ACT is successful when:

> A third party can:
> - understand what action to take
> - see exactly why (evidence)
> - evaluate risk clearly
> - monitor whether it works

WITHOUT needing additional explanation