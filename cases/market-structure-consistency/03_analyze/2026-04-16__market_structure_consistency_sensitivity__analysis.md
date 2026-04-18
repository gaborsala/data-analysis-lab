# ANALYZE — Sensitivity Review (v1.1 Hardened)

Date: 2026-04-16  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer) — Sensitivity Variants

---

## 1. Questions Answered

This review answers the following follow-up questions:

1. How much does the direction mix change when the block length changes from 3 weeks to 4 weeks to 6 weeks?
2. Does the current 4-week baseline appear materially unstable relative to nearby variants?
3. Can recommendation strength be upgraded based on the current sensitivity outputs?

---

## 2. Descriptive Statistics

### Table A. Direction-share comparison across block variants

| Direction | 3-week Share | 4-week Share | 6-week Share | Range (max-min) |
|---|---:|---:|---:|---:|
| HH/HL | 37.88% | 37.79% | 37.37% | 0.51 pts |
| LH/LL | 41.35% | 41.28% | 41.11% | 0.24 pts |
| TRANSITION | 20.77% | 20.93% | 21.52% | 0.75 pts |

### Table B. Ready-row totals by variant

| Block Variant | Ready Rows |
|---|---:|
| 3-week | 8,554 |
| 4-week | 8,532 |
| 6-week | 8,488 |

### Table C. Ready-row change relative to 4-week baseline

| Block Variant | Ready Rows | Difference vs 4-week |
|---|---:|---:|
| 3-week | 8,554 | +22 |
| 4-week | 8,532 | 0 |
| 6-week | 8,488 | -44 |

---

## 3. Segmentation / Comparisons

### Comparison 1: Direction-share stability

Observed differences:

- `HH/HL` remains tightly clustered between 37.37% and 37.88%.
- `LH/LL` remains tightly clustered between 41.11% and 41.35%.
- `TRANSITION` varies slightly more, but still only across a 0.75 percentage-point range.

### Comparison 2: Classification-ready row stability

Observed differences:

- Moving from 4-week to 3-week adds only 22 ready rows.
- Moving from 4-week to 6-week removes only 44 ready rows.
- The ready-row totals remain highly stable relative to the total classified weekly panel.

No inferential test is applied. These are descriptive robustness checks.

---

## 4. Relationship Exploration (Non-Causal Unless Proven)

| Variables | Method | Strength | Statistical Significance | Notes |
|---|---|---|---|---|
| Block length vs direction-share distribution | Variant comparison | High descriptive evidence | Not tested | Shares are very stable across 3w/4w/6w |
| Block length vs ready-row count | Variant comparison | High descriptive evidence | Not tested | Only minor changes in ready-row totals |
| Block length vs TRANSITION share | Variant comparison | Moderate descriptive evidence | Not tested | Longer block modestly increases TRANSITION share |

No causal interpretation is made.

---

## 5. Causality Gate (Mandatory)

No causal language is used.

This sensitivity review does not claim that:
- one block length causes better classification quality
- a longer block reveals a truer market state
- stable shares imply predictive validity

The review only assesses robustness of descriptive outputs under nearby rule changes.

---

## 6. Evidence Traceability Table (Mandatory)

| Claim | Evidence Reference | Strength of Evidence | Alternative Explanation Considered |
|---|---|---|---|
| Direction shares are stable across 3w/4w/6w variants | Table A | High | Nearby variants may be too close; larger rule changes could still matter |
| The 4-week baseline does not appear materially unstable | Tables A–C | High | Stability was checked only for block length, not weekly anchor |
| TRANSITION share increases slightly at 6 weeks | Table A | Moderate | This may reflect smoother directional thresholds rather than genuine regime change |
| Recommendation strength can be upgraded modestly, but not to strong | Tables A–C plus prior ANALYZE evidence | Moderate | Weekly-anchor sensitivity and local manual checks are still pending |

---

## 7. What the Data Supports

The sensitivity outputs support the following statements:

1. The 4-week baseline is robust against nearby 3-week and 6-week block variants at the direction-share level.
2. The state-ranking order remains unchanged across all tested variants:
   - LH/LL highest
   - HH/HL second
   - TRANSITION third
3. Ready-row totals remain very similar across all tested block lengths.
4. Current conclusions about descriptive state mix do not appear highly sensitive to this specific block-length variation.

---

## 8. What the Data Does NOT Support

The sensitivity outputs do **not** support the following claims:

1. They do not prove full robustness across all possible rule designs.
2. They do not test alternate weekly anchors.
3. They do not prove that the 4-week rule is optimal.
4. They do not establish predictive or economic validity.
5. They do not replace the remaining local manual spot-check items.

---

## 9. Alternative Explanations

Possible alternative explanations for the observed stability:

- The tested variants are relatively close to one another, so large differences were less likely.
- The broad historical sample may smooth smaller rule-design changes.
- Transition behavior and ticker-level run durations may still vary more than headline direction shares.

---

## 10. Limitations

### Data limitations
- This review uses generated sensitivity summary files only.
- It does not inspect all ticker-level variant outputs in detail.

### Methodological limitations
- Only 3-week, 4-week, and 6-week block variants were tested.
- Weekly-anchor sensitivity was not tested here.

### External validity limits
- Findings apply only to this SPDR-sector-vs-SPY framework.

### Sensitivity to assumptions
- Conclusions remain conditional on the same `W-FRI` resampling rule.
- Larger changes to classification design may still produce different results.

---

## 11. Analytical Confidence Level

**Overall confidence in the sensitivity conclusion: Moderate to High**

### Justification
- Direction-share stability is directly supported by the uploaded sensitivity summary files.
- The observed variation is small in absolute terms.
- Confidence is still capped below “High” for the overall framework because weekly-anchor sensitivity and a few local manual checks remain incomplete.

---

## 12. Validation Checks Performed

### Performed
- Reviewed `direction_share_summary_all_variants.csv`
- Reviewed `direction_share_comparison_pivot.csv`
- Confirmed all three valid directions are present across all variants
- Confirmed direction ranking order is unchanged across 3w/4w/6w
- Confirmed ready-row totals remain close across variants

### Recommended
- Compare ticker-level persistence outputs across 3w/4w/6w
- Run alternate weekly-anchor sensitivity
- Finish local manual checks 9–13
- Regenerate ACT artifact with updated recommendation strength wording

---

## 13. Conclusion

The sensitivity files indicate that the current 4-week baseline is **descriptively stable** relative to nearby 3-week and 6-week variants.

This supports:
- keeping the 4-week version as the repo baseline
- modestly increasing confidence in the state-mix conclusions
- keeping recommendation strength at **Moderate**, not Strong

A stronger claim would still require:
- weekly-anchor sensitivity
- completed local manual spot-checks
- ideally ticker-level variant comparisons for persistence and transitions

---

## 14. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Uploaded sensitivity files match the local generated outputs | Required for review validity | Review could reflect stale or mismatched files | Compare timestamps and rerun if needed |
| Direction-share stability is a meaningful robustness signal | Useful first-pass sensitivity check | Ticker-level instability could still exist | Compare duration and transition outputs by variant |
| Small percentage-point changes are not materially different for this use case | Appropriate for descriptive repo claims | External publishing may require stricter thresholds | Define explicit materiality rule in next version |

---

## 15. Integrity Declaration

- No causal claims introduced
- No conclusions beyond the uploaded sensitivity evidence
- Uncertainty remains explicit
- Claims are proportional to the observed variant stability