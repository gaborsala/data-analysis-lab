# FULL LIFECYCLE SOP — EXECUTION SYSTEM (v1.0)

Date: 2026-04-17  
Scope: End-to-end execution across all lifecycle stages  

---

## 0. PURPOSE

This document defines how to execute the full analytical lifecycle:

ASK → PREPARE → PROCESS → ANALYZE → ACT

It connects phase-level SOPs into a **single deterministic workflow**.

---

## 1. SYSTEM ARCHITECTURE

Three layers:

1. GOVERNANCE (rules)
   - MASTER.md

2. TEMPLATES (output structure)
   - docs/templates/

3. EXECUTION (how work is done)
   - docs/sop/

---

## 2. CORE EXECUTION LOOP

Every stage follows:

OBSERVE → WRITE → VALIDATE → STOP

No stage skipping allowed.

---

## 3. STAGE TRANSITION LOGIC

### ASK → PREPARE

Condition:
- Question is measurable
- Success criteria defined

If not → STOP

---

### PREPARE → PROCESS

Condition:
- Schema documented
- Missingness analyzed
- No interpretation present

If violated → REWRITE PREPARE

---

### PROCESS → ANALYZE

Condition:
- All transformations logged
- Validation checks passed
- Reproducibility confirmed

If not → FIX PROCESS

---

### ANALYZE → ACT

Condition:
- All claims mapped to evidence
- No causal overstatement
- Limitations documented

If not → FIX ANALYZE

---

## 4. EXECUTION MODE

### Rule 1 — One stage at a time

Never:
- mix stages
- jump ahead

---

### Rule 2 — One step at a time

Within a stage:

- execute one SOP step
- write result
- validate

---

### Rule 3 — No parallel thinking

Do NOT:
- analyze during PREPARE
- recommend during ANALYZE

---

## 5. FILE CREATION FLOW

For each stage:

1. Execute SOP
2. Collect outputs
3. Fill template
4. Save artifact

---

## 6. ERROR HANDLING SYSTEM

If stuck:

### Step 1

Identify stage

---

### Step 2

Identify SOP step number

---

### Step 3

Do ONLY that step

---

### Step 4

Ignore rest of template

---

## 7. COMMON FAILURE MODES

### 1. Blank page paralysis

Cause:
- trying to fill template directly

Fix:
- return to SOP step 1

---

### 2. Overthinking

Cause:
- mixing stages

Fix:
- enforce stage boundaries

---

### 3. Hidden assumptions

Cause:
- skipping documentation

Fix:
- fill assumption tables early

---

### 4. Overconfident conclusions

Cause:
- weak ANALYZE discipline

Fix:
- enforce evidence mapping

---

## 8. DAILY EXECUTION PROTOCOL (NZ2 ALIGNED)

Session start:

1. Identify current stage
2. Open corresponding SOP
3. Execute first step only

---

Session end:

1. Complete current step
2. Save progress
3. Log next step

---

## 9. ASSUMPTIONS

- User follows lifecycle discipline
- Phase SOPs are used correctly
- No stage skipping occurs

---

## 10. LIMITATIONS

- No automated enforcement
- Requires manual discipline
- Learning curve initially high

---

## 11. VALIDATION CHECKS

System is working if:

- No stage confusion
- No blank page moments
- Outputs reproducible
- Artifacts align with templates

---

## 12. INTEGRITY DECLARATION

- No stage skipping
- No hidden transformations
- No premature interpretation
- No recommendation beyond evidence

---

## 13. SUCCESS CONDITION

System is successful when:

> The user can execute any dataset from ASK → ACT
> without confusion, hesitation, or structural errors.
