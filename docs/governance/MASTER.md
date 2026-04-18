# MASTER — Data Analysis Lab Governance (v1.1)

## 0. Purpose

Defines:
- lifecycle structure
- folder mapping
- naming rules
- quality gates

This file is the **single source of truth**.

---

## 1. Lifecycle (Non-Negotiable)

ASK → PREPARE → PROCESS → ANALYZE → ACT

Rules:
- no skipping
- no merging (unless explicitly allowed)
- no renaming

---

## 2. Folder Mapping

| Stage     | Folder        | Artifact suffix |
|----------|--------------|----------------|
| ASK      | 00_ASK/      | __ask.md       |
| PREPARE  | 01_PREPARE/  | __prepare.md   |
| PROCESS  | 02_PROCESS/  | __process_log.md |
| ANALYZE  | 03_ANALYZE/  | __analysis.md  |
| ACT      | 04_ACT/      | __action_plan.md |

---

## 3. Naming Convention

Format:

YYYY-MM-DD__topic__stage.md

Example:

2026-04-17__retail_sales__analysis.md

---

## 4. Stage Responsibilities

### ASK
- define decision problem
- no data allowed

### PREPARE
- understand structure
- no transformation
- no interpretation

### PROCESS
- clean and transform
- full logging required

### ANALYZE
- produce evidence
- no causal overstatement

### ACT
- map conclusions to evidence
- define recommendations

---

## 5. Quality Gates

Each stage must pass before continuing.

---

## 6. Integrity Rules

- no silent filtering
- no undocumented changes
- no unsupported claims
- no recommendation beyond evidence

---

## 7. Success Definition

System is successful if:

- full lifecycle exists
- conclusions are traceable
- artifacts are reproducible