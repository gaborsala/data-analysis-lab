# ASK — EXECUTION SOP (v1.0)

Date: 2026-04-17  
Stage: ASK  
Purpose: Deterministic problem definition before any data interaction  

---

## 0. PURPOSE

This SOP defines the **exact execution steps** required to complete the ASK phase.

Goal:
- eliminate vague problem statements
- enforce decision-first thinking
- ensure analytical direction is testable and measurable

This stage must be completed **before any dataset is opened**.

---

## 1. CORE PRINCIPLE

ASK is not brainstorming.

ASK is:

> **Decision definition under constraints with measurable success criteria**

---

## 2. EXECUTION FLOW (STRICT ORDER)

Follow steps sequentially. Do not skip.

---

## STEP 1 — DEFINE THE DECISION QUESTION

### Action

Write a single sentence using this structure:

> “Should we [ACTION] for [POPULATION] based on [METRIC] over [TIMEFRAME]?”

---

### Constraints

- Must include:
  - action (buy, compare, allocate, evaluate, etc.)
  - population (who/what is affected)
  - metric (what is measured)
  - timeframe

---

### Validation

- [ ] Question is specific
- [ ] Question is measurable
- [ ] Question is answerable with data

---

### Stop Condition

If vague → rewrite until precise

---

## STEP 2 — DEFINE DECISION CONTEXT

### Action

Write:

- What decision will be made?
- Who is responsible?
- What happens if:
  - decision is correct
  - decision is wrong

---

### Example Structure

- Decision:
- Owner:
- If correct:
- If wrong:

---

### Validation

- [ ] Consequences clearly defined
- [ ] Decision impact understood

---

## STEP 3 — DEFINE OBJECTIVE (MEASUREMENT ONLY)

### Action

Write:

- What will be measured
- Between which groups (if applicable)
- Over what time horizon

---

### Rules

- No recommendations
- No conclusions
- No predictions

---

### Validation

- [ ] Objective is measurable
- [ ] No solution bias present

---

## STEP 4 — DEFINE SUCCESS CRITERIA

### Action

Write explicit measurable condition.

---

### Must include:

- numeric threshold
- condition

---

### Example

- “Detect ≥10% difference between groups”
- “Identify top 3 drivers explaining ≥60% variance”

---

### Validation

- [ ] Quantifiable
- [ ] Testable later in ANALYZE

---

### Stop Condition

If cannot measure success → ASK is invalid

---

## STEP 5 — DEFINE CONSTRAINTS

### Action

List all limitations:

- Time constraints
- Data availability
- Scope boundaries
- Resource limitations

---

### Validation

- [ ] Constraints are realistic
- [ ] Constraints are explicit

---

## STEP 6 — DEFINE ASSUMPTIONS (MANDATORY TABLE)

### Action

Create minimum 3 assumptions.

---

### Required structure

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|-----------|------------|--------------|------------------|

---

### Rules

- Must be testable later
- Must NOT include conclusions

---

### Validation

- [ ] Each assumption testable
- [ ] No hidden assumptions

---

## STEP 7 — DEFINE RISKS TO DECISION QUALITY

### Action

List risks:

- Data quality risk
- Measurement bias
- Confounding risk
- External validity risk

---

### Validation

- [ ] At least 3 risks identified
- [ ] Risks are relevant to decision

---

## STEP 8 — DEFINE OUT-OF-SCOPE

### Action

Explicitly exclude:

- unrelated metrics
- long-term forecasting (if excluded)
- causal claims (if not intended)
- implementation details

---

### Validation

- [ ] Scope boundaries clear
- [ ] Prevents scope creep

---

## STEP 9 — DEFINE DELIVERABLES

### Action

List:

- Primary artifact (e.g., ANALYZE report)
- Supporting outputs (tables, charts)
- Expected lifecycle outputs

---

### Validation

- [ ] Deliverables align with lifecycle
- [ ] Clear expectations defined

---

## 3. VALIDATION CHECKLIST (FINAL GATE)

ASK is complete ONLY if:

- [ ] Question is specific and measurable
- [ ] Decision context defined
- [ ] Objective measurable and unbiased
- [ ] Success criteria quantifiable
- [ ] Constraints listed
- [ ] Assumptions documented and testable
- [ ] Risks identified
- [ ] Out-of-scope defined
- [ ] Deliverables listed

---

## 4. ASSUMPTIONS

- User has a defined analytical topic
- Decision can be framed quantitatively
- Data will be available in later stages

---

## 5. LIMITATIONS

- Quality depends on clarity of thinking
- Poor ASK leads to weak entire pipeline
- Cannot validate assumptions until later stages

---

## 6. RECOMMENDED VALIDATION ACTIONS

- Re-read question after 10 minutes
- Try to falsify your own assumptions
- Check if another person could understand the decision clearly
- Ensure no data knowledge leaked into ASK

---

## 7. INTEGRITY DECLARATION

- No data inspected before defining problem
- No hidden assumptions
- No recommendations introduced
- Decision criteria defined before analysis

---

## 8. SUCCESS CONDITION

ASK is successful when:

> A third party can read it and immediately understand:
> - what decision is being made
> - how success will be measured
> - what constraints exist
