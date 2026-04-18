# ANALYZE — Findings (v1.1 Hardened)

Date: 2026-04-06  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer)

---

## 1. Questions Answered

This analysis answers the following questions derived from ASK and refined in PREPARE:

1. What is the historical weekly structure-state distribution under the current classification rule?
2. What are the persistence characteristics of HH/HL, LH/LL, and TRANSITION states by sector?
3. What does the transition structure look like across classified weekly observations?
4. How does the latest run length compare with each ticker’s own historical average for the same state?
5. What changes when analysis is restricted to a stricter common-window dataset?

No new questions are introduced.

---

## 2. Descriptive Statistics

### Table A. Core weekly panel summary

| Metric | Value | Notes |
|---|---:|---|
| Weekly rows | 9,339 | Full weekly panel |
| Classification-ready rows | 8,521 | Rows with sufficient valid history for 4-week block comparison |
| Non-ready rows | 818 | `NO_RATIO` + `INSUFFICIENT_HISTORY` |
| Ready share | 91.24% | 8,521 / 9,339 |
| Weekly rule | W-FRI | Friday anchor |
| Block rule | 4-week block vs prior 4-week block | Deterministic structure rule |

### Table B. Direction distribution — full weekly panel

| Direction | Count | Share of all weekly rows | Share of ready rows |
|---|---:|---:|---:|
| LH/LL | 3,516 | 37.65% | 41.26% |
| HH/HL | 3,222 | 34.50% | 37.81% |
| TRANSITION | 1,783 | 19.09% | 20.92% |
| NO_RATIO | 741 | 7.93% | N/A |
| INSUFFICIENT_HISTORY | 77 | 0.82% | N/A |

### Table C. Common-window companion dataset

| Metric | Value | Notes |
|---|---:|---|
| Daily common-window rows | 21,626 | 11 sectors × shared daily overlap |
| Weekly common-window rows | 4,422 | 11 sectors × shared weekly overlap |
| Implied common-window weekly dates | 402 | 4,422 / 11 |
| Common-window start | 2018-08-10 | First weekly date with all 11 sectors classification-ready |
| Common-window regime | Stricter comparability | Removes later-inception partial-history distortion |

All statistics above are reproducible from PROCESS and ANALYZE script outputs.

---

## 3. Segmentation / Comparisons

### Comparison 1: Full-history readiness vs structural unavailability

| Segment | Count | Share |
|---|---:|---:|
| Classification-ready | 8,521 | 91.24% |
| Not ready | 818 | 8.76% |

Observed difference:
- Most weekly rows are analyzable under the current classification rule.
- The non-ready share is concentrated in pre-inception and warmup periods rather than general data failure.

### Comparison 2: Direction mix among ready rows

| Direction | Count | Share of ready rows |
|---|---:|---:|
| LH/LL | 3,516 | 41.26% |
| HH/HL | 3,222 | 37.81% |
| TRANSITION | 1,783 | 20.92% |

Observed differences:
- LH/LL is the most frequent ready-state in the full-history run.
- HH/HL is close in magnitude.
- TRANSITION remains material but lower than both directional states.

### Comparison 3: Transition stability vs directional change

From `weekly_structure_transition_matrix.csv`:

| From State | To Same State | Same-State Share | Changed-State Share |
|---|---:|---:|---:|
| HH/HL | 2,598 | 80.63% | 19.37% |
| LH/LL | 2,879 | 81.88% | 18.12% |
| TRANSITION | 766 | 42.96% | 57.04% |

Observed differences:
- HH/HL and LH/LL show high one-step persistence.
- TRANSITION is materially less stable than either directional state.

No statistical significance test is applied. These are descriptive comparisons only.

---

## 4. Relationship Exploration (Non-Causal Unless Proven)

| Variables | Method | Strength | Statistical Significance | Notes |
|---|---|---|---|---|
| Structure state vs next-state persistence | Transition count and share | High descriptive evidence | Not tested | Directional states show stronger next-step persistence than TRANSITION |
| Latest run length vs historical average for same direction | Ticker-level duration comparison | Moderate descriptive evidence | Not tested | Useful for current-context benchmarking |
| Coverage window vs comparability | Full-history vs common-window dataset design | High structural evidence | Not tested | Common-window panel improves cross-sector comparability |
| Rule design vs state output | Deterministic classification logic | High methodological dependence | Not applicable | Outputs depend directly on 4-week block assumption |

No causal interpretation is made.

---

## 5. Causality Gate (Mandatory)

No causal language is used in this artifact.

This analysis does **not** claim that:
- a structure state causes future performance
- persistence causes market outcomes
- transition frequency drives future regime behavior
- the 4-week rule identifies a true underlying market mechanism

All statements remain descriptive and rule-dependent.

---

## 6. Evidence Traceability Table (Mandatory)

| Claim | Evidence Reference (table/metric/test) | Strength of Evidence | Alternative Explanation Considered |
|---|---|---|---|
| Most weekly rows are classification-ready | Table A; 8,521 of 9,339 rows | High | Readiness rate depends on block size and weekly anchor |
| LH/LL is the most frequent ready-state in the full-history sample | Table B | High | Ranking may change under common-window restriction |
| Directional states are more persistent week-to-week than TRANSITION | Table in Section 3, Comparison 3; transition matrix | High | Persistence levels may shift under alternate block lengths |
| TRANSITION is the least stable state in one-step transitions | Transition matrix and transition shares | High | State definitions are rule-driven, not independent market truth |
| Cross-sector comparability improves under common-window restriction | Table C; common-window rows and dates | High | Common-window sacrifices long-history information |

---

## 7. What the Data Supports

The generated outputs support the following statements:

1. The historical weekly classification pipeline ran successfully and produced a usable full-history classified panel and a stricter common-window companion panel.
2. Most weekly rows are classification-ready under the current 4-week-vs-prior-4-week rule.
3. In the full-history ready sample, LH/LL is the most frequent state, followed by HH/HL, then TRANSITION.
4. HH/HL and LH/LL exhibit strong one-step persistence, each remaining in the same state more than 80% of the time in adjacent classified observations.
5. TRANSITION is materially less stable than either directional state, with changed-state transitions exceeding same-state transitions.
6. The common-window dataset begins materially later than the full-history dataset, confirming that later-inception ETFs affect direct full-period comparability.
7. Duration outputs are structurally usable for ticker-level persistence analysis because run tables, summaries, and recent-vs-historical comparisons were all generated successfully.

---

## 8. What the Data Does NOT Support

The current outputs do **not** support the following claims:

1. They do not prove that LH/LL is inherently more important than HH/HL.
2. They do not prove that persistent states predict future return behavior.
3. They do not justify forecasting, timing rules, or alpha claims.
4. They do not establish causality between ETF coverage windows and structure-state frequencies.
5. They do not prove that the 4-week block rule is optimal.
6. They do not yet show whether common-window direction shares materially differ from full-history shares unless that comparison is calculated explicitly.
7. They do not prove robustness across alternative resampling anchors or block lengths.

This section is mandatory and complete.

---

## 9. Alternative Explanations

### Finding: LH/LL is the most frequent ready-state
Possible alternative explanations:
- full-history sample composition
- 4-week block design
- Friday resampling anchor
- inclusion of longer bearish episodes in the sample history

### Finding: HH/HL and LH/LL are highly persistent
Possible alternative explanations:
- state definition itself favors adjacent-state continuity
- weekly sampling smooths short-term reversals
- persistence may be lower under shorter blocks or stricter common-window comparison

### Finding: TRANSITION is least stable
Possible alternative explanations:
- TRANSITION is defined as a residual category
- mixed conditions may naturally create shorter runs
- this instability may be partly a classification artifact rather than a standalone market property

### Finding: Common-window restriction improves comparability
Possible alternative explanations:
- improved comparability comes at the cost of excluding earlier market history
- later sample start may alter directional-state mix and transition structure

---

## 10. Limitations

### Data limitations
- XLC and XLRE have materially shorter histories than the older sector ETFs.
- The common-window sample necessarily excludes earlier history.

### Methodological limitations
- Classification depends on a deterministic 4-week block comparison.
- Weekly anchor is fixed at `W-FRI`.
- Duration and transition summaries are descriptive, not inferential.

### External validity limits
- Findings apply only to the 11 SPDR sector ETFs relative to SPY.
- Results should not be generalized to individual stocks, other regions, or intraday structure.

### Sensitivity to assumptions
- State distribution may change under alternate block lengths.
- Persistence and transition counts may change under alternate resampling anchors.
- Common-window and full-history conclusions may diverge in later comparison work.

---

## 11. Analytical Confidence Level

**Overall confidence in current findings: Moderate**

### Justification
- **Data quality:** Moderate to High. Raw ingestion and audit passed cleanly.
- **Sample size:** High. The full weekly panel contains 9,339 rows and the common-window panel contains 4,422 rows.
- **Method robustness:** Moderate. The workflow is deterministic, but outputs are sensitive to explicit rule design.
- **Validation strength:** Moderate. Structural outputs are internally consistent, but alternative-rule sensitivity testing has not yet been performed.

Confidence is appropriate for descriptive historical consistency statements only.

---

## 12. Persistence Findings

### Table D. Duration output integrity

| Output | Rows | Interpretation |
|---|---:|---|
| `weekly_structure_duration_runs.csv` | 2,289 | Distinct same-state runs across tickers |
| `weekly_structure_duration_summary.csv` | 33 | 11 tickers × 3 valid directions |
| `weekly_structure_recent_vs_historical_duration.csv` | 11 | One latest-vs-history comparison per ticker |

### Table E. Sample persistence characteristics

From `weekly_structure_duration_summary.csv`:
- XLB HH/HL: max run 15 weeks
- XLB LH/LL: max run 18 weeks
- XLB TRANSITION: max run 5 weeks

This pattern is directionally consistent with the transition matrix:
- directional states can persist for materially longer runs
- TRANSITION runs tend to be shorter

### Table F. Recent vs historical comparison integrity

The recent-vs-historical file contains 11 rows, one per ticker, confirming that each sector has:
- a latest classified run
- a historical average duration for the same direction
- a difference vs that historical average

Example:
- XLB latest run duration is 0.85 weeks below its own historical average for the same direction
- XLC latest run duration is 2.40 weeks below its own historical average for the same direction

These examples demonstrate that the output is structurally correct and interpretable at ticker level.

---

## 13. Transition Findings

### Table G. One-step transition matrix

| From \ To | HH/HL | LH/LL | TRANSITION |
|---|---:|---:|---:|
| HH/HL | 2,598 | 121 | 503 |
| LH/LL | 123 | 2,879 | 514 |
| TRANSITION | 500 | 517 | 766 |

### Table H. Transition-share summary

| From State | To State | Count | Share from State |
|---|---|---:|---:|
| HH/HL | HH/HL | 2,598 | 80.63% |
| HH/HL | LH/LL | 121 | 3.76% |
| HH/HL | TRANSITION | 503 | 15.61% |
| LH/LL | HH/HL | 123 | 3.50% |
| LH/LL | LH/LL | 2,879 | 81.88% |
| LH/LL | TRANSITION | 514 | 14.62% |
| TRANSITION | HH/HL | 500 | 28.04% |
| TRANSITION | LH/LL | 517 | 29.00% |
| TRANSITION | TRANSITION | 766 | 42.96% |

### Table I. Changed transitions only

`weekly_structure_changed_transitions_only.csv` contains 6 rows, confirming that only genuine state changes are isolated there.

Observed pattern:
- direct HH/HL ↔ LH/LL jumps are rare relative to same-state persistence
- directional states more often move into TRANSITION than directly into the opposite directional state

This is descriptive evidence consistent with a regime-change process that often passes through a mixed state, but it is not causal proof.

---

## 14. Validation Checks Performed or Recommended

### Performed
- Duration outputs generated successfully
- Transition outputs generated successfully
- Common-window outputs generated successfully
- Transition matrix dimensions are correct for the three valid states
- Duration summary row count is correct for 11 tickers × 3 directions
- Recent-vs-historical output has one row per ticker
- Common-window classified panel has 4,422 rows, implying full 11-sector overlap across 402 weekly dates

### Recommended
- Compare full-history vs common-window direction shares explicitly
- Compute ticker-level transition summaries
- Run sensitivity checks for 3-week and 6-week block variants
- Run sensitivity checks for alternate weekly anchors
- Complete and save the manual spot-check note
- Add SHA256 hashes in the next PROCESS iteration

---

## 15. ANALYZE Gate Checklist

- [x] Questions trace to ASK
- [x] Statistics reproducible from PROCESS and ANALYZE outputs
- [x] Claims mapped to evidence
- [x] Causality not overstated
- [x] Alternative explanations considered
- [x] Limitations acknowledged
- [x] “What the Data Does NOT Support” section completed
- [x] Analytical confidence justified
- [x] Next stage allowed (ACT), with recommendation strength limited to exploratory-to-moderate because sensitivity testing is still pending

---

## 16. Integrity Declaration

- No conclusions beyond available evidence
- No causal claims without identification
- No selective reporting
- All major claims are traceable
- Uncertainty is explicitly acknowledged