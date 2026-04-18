# ACT — Conclusions & Action Plan (v1.1 Hardened)

Date: 2026-04-06  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer)

---

## 1. Evidence-Based Conclusion Mapping (Mandatory)

| Conclusion | Evidence Reference | Confidence | Risk if Wrong |
|---|---|---|---|
| The weekly classification framework is operationally usable for historical consistency analysis | ANALYZE Table A; 9,339 weekly rows, 8,521 classification-ready rows | Moderate | Downstream interpretation could rely on a rule set that is structurally valid but not yet sensitivity-tested |
| Directional states (HH/HL and LH/LL) are materially more persistent than TRANSITION in adjacent classified weeks | ANALYZE Table H; HH/HL self-transition 80.63%, LH/LL self-transition 81.88%, TRANSITION self-transition 42.96% | Moderate | Persistence may change under alternative block lengths or weekly anchors |
| Direct HH/HL ↔ LH/LL jumps are rare relative to transitions through TRANSITION | ANALYZE Table H; HH/HL→LH/LL 3.76%, LH/LL→HH/HL 3.50%, larger directional→TRANSITION paths | Moderate | The residual definition of TRANSITION may mechanically increase intermediary-state counts |
| Full-history and common-window direction mixes are similar but not identical | Full-history ready shares: LH/LL 41.26%, HH/HL 37.81%, TRANSITION 20.92%; Common-window shares: LH/LL 42.76%, HH/HL 36.68%, TRANSITION 20.56% | Moderate | Small distribution shifts may become larger under alternate classification parameters |
| Cross-sector comparability is stricter in the common-window sample and should be used for external summaries when comparability matters most | ANALYZE Table C; common-window begins 2018-08-10 and includes full 11-sector weekly overlap | Moderate | Restricting to common-window excludes earlier history and may omit informative legacy regimes |

---

## 2. Explicit Full-History vs Common-Window Comparison Table

| Direction | Full-History Count | Full-History Share of Ready Rows | Common-Window Count | Common-Window Share | Common minus Full (pct pts) |
|---|---:|---:|---:|---:|---:|
| LH/LL | 3,516 | 41.26% | 1,891 | 42.76% | +1.50 |
| HH/HL | 3,222 | 37.81% | 1,622 | 36.68% | -1.13 |
| TRANSITION | 1,783 | 20.92% | 909 | 20.56% | -0.37 |

### Interpretation boundary
- The direction mix remains broadly similar across the two views.
- Common-window restriction modestly increases LH/LL share and modestly reduces HH/HL share.
- These are descriptive differences only. They do not prove that one view is more “true” than the other.

---

## 3. Recommendations

### Recommendation 1
**Action:** Keep the 4-week-vs-prior-4-week classification as the baseline specification for this repo version.  
**Rationale:** The pipeline is reproducible, produces a high share of analyzable rows, and yields interpretable persistence and transition outputs.  
**Expected impact:** Stable baseline for portfolio presentation and further validation.  
**Evidence strength:** Moderate  
**Operational feasibility:** High

### Recommendation 2
**Action:** Use the common-window companion outputs for recruiter-facing cross-sector comparison summaries.  
**Rationale:** The common-window panel removes unequal-history distortion from later-inception ETFs.  
**Expected impact:** Cleaner external communication of cross-sector comparability.  
**Evidence strength:** Moderate  
**Operational feasibility:** High

### Recommendation 3
**Action:** Keep full-history outputs for ticker-level persistence analysis and methodological transparency.  
**Rationale:** Full-history retains valid longer-run information for older ETFs and supports richer run-length analysis.  
**Expected impact:** Better auditability and stronger methodological depth.  
**Evidence strength:** Moderate  
**Operational feasibility:** High

### Recommendation 4
**Action:** Do not make strong public claims about robustness until 3-week and 6-week sensitivity variants are run and compared.  
**Rationale:** Current findings are rule-dependent and sensitivity testing is still pending.  
**Expected impact:** Better claim discipline and lower overstatement risk.  
**Evidence strength:** High  
**Operational feasibility:** High

### Recommendation 5
**Action:** Add SHA256 file hashing to the PROCESS layer before the next version bump.  
**Rationale:** This strengthens reproducibility and audit traceability.  
**Expected impact:** Better governance quality and stronger repo credibility.  
**Evidence strength:** Moderate  
**Operational feasibility:** High

---

## 4. Risk & Uncertainty Assessment

| Recommendation | Key assumption | What could invalidate it? | Sensitivity to data quality | Sensitivity to external factors |
|---|---|---|---|---|
| Keep 4-week baseline | Current block length is a reasonable default lens | 3-week or 6-week variants produce materially different state distributions or transitions | Moderate | Low |
| Use common-window for external comparisons | Common-window improves comparability more than it harms historical coverage | Common-window omits critical earlier regimes that materially change interpretation | Low to Moderate | Low |
| Keep full-history for ticker-level persistence | Preserved longer history is analytically useful despite unequal starts | Legacy history dominates the narrative too strongly relative to newer ETFs | Moderate | Low |
| Delay stronger claims pending sensitivity tests | Rule-dependence is material | Sensitivity tests show minimal differences, making the caveat less necessary | Low | Low |
| Add SHA256 hashing | File identity should be reproducible and auditable | None materially; this is governance-strengthening rather than analytical | Low | Low |

---

## 5. Monitoring & Validation Plan

| Metric to track | Monitoring frequency | Threshold for reassessment | Trigger for rollback |
|---|---|---|---|
| Direction-share differences across 3/4/6-week variants | Per sensitivity run | >5 percentage-point shift in any direction share | Refrain from publishing strong stability claims |
| Same-state transition share by direction | Per sensitivity run | >10 percentage-point shift for HH/HL or LH/LL self-transition | Reclassify recommendation strength downward |
| Common-window vs full-history direction-share gap | Per version | >3 percentage-point shift in any direction | Reframe external comparison narrative |
| Hash-manifest completeness | Every PROCESS revision | Any missing key output hash | Treat process audit as incomplete |
| Manual spot-check completion | Every release candidate | Incomplete validation note | Delay external publication |

---

## 6. Expected Impact

### Short-term effect
- Moves the repo from a raw classification engine to an auditable historical consistency framework.
- Supports recruiter-facing explanation of persistence, transition behavior, and comparability discipline.

### Long-term effect
- Establishes a foundation for confidence-layer development without jumping into forecasting or performance claims.

### Measurable KPI(s)
- Presence of full ASK → ACT chain
- Presence of reproducible duration, transition, and common-window outputs
- Completion of sensitivity and hashing steps
- Reduction in undocumented process risk

### Estimated magnitude
- Qualitative only at this stage. No defensible numerical business-impact estimate is available.

---

## 7. Implementation Plan

| Item | Owner | Timeline | Dependencies | Review checkpoint |
|---|---|---|---|---|
| Complete manual spot-check note | Gabor Sala | Immediate | Current outputs available | Same day |
| Add SHA256 hashing script and run it | Gabor Sala | Immediate next revision | File paths stable | Same day |
| Run 3-week and 6-week sensitivity variants | Gabor Sala | Immediate next revision | Sensitivity runner available | Same day |
| Compare variant outputs to 4-week baseline | Gabor Sala | After sensitivity runs | Sensitivity outputs generated | Next analysis pass |
| Publish refined ACT/ANALYZE version | Gabor Sala | After validation tasks | Spot-check + hashes + sensitivity complete | Release candidate |

---

## 8. Scaling & Automation

**Is repeatable pipeline logic required?**  
Yes.

### Data requirements for automation
- Stable raw ticker files in `data/raw`
- Stable processed outputs in `cases/market-structure-consistency/outputs/02_process`
- Deterministic classified weekly panel as the sensitivity input

### Tooling requirements
- Existing CLI scripts for download, audit, ratio build, and classification
- Hash-manifest generator
- Sensitivity runner
- Versioned output folders or filenames if multiple variants are preserved

### Governance considerations
- The 4-week block assumption must remain explicit in every downstream artifact
- Sensitivity outputs should not overwrite the baseline unless intentionally versioned
- Any material rule change should trigger a version bump for ANALYZE and ACT artifacts

---

## 9. Recommendation Strength Classification

**Overall strength of recommendation: Moderate**

### Justification
- Evidence is internally consistent and traceable.
- The pipeline is reproducible and produces interpretable persistence and transition outputs.
- However, recommendation strength is capped because sensitivity testing is still pending and manual/hashing validation needs to be completed.

---

## 10. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Small full-vs-common direction-share differences indicate reasonable stability | Current comparison gaps are modest | Variant runs may show larger instability | Run 3/4/6-week comparison table |
| Transition persistence is informative for regime-consistency framing | Transition counts are structurally meaningful | Rule design may dominate the pattern | Sensitivity testing across block lengths |
| Common-window is preferable for external cross-sector comparison | Equal coverage reduces comparability distortion | Loss of pre-2018 history may materially change narrative | Compare external summary both ways before publication |

---

## 11. Limitations

- Recommendation strength is constrained by pending sensitivity tests.
- Manual validation has not yet been fully logged in a completed note.
- File-level SHA256 hashes are not yet attached to the current PROCESS revision.
- No forecasting or performance linkage is established or recommended.

---

## 12. ACT Gate Checklist

- [x] Every conclusion mapped to evidence
- [x] Confidence level specified
- [x] Risks acknowledged
- [x] Monitoring plan defined
- [x] Impact measurable at process level
- [x] No speculative inflation
- [x] No causal claims beyond ANALYZE evidence
- [x] Next validation steps clearly defined

---

## 13. Integrity Declaration

- All conclusions trace directly to ANALYZE-stage evidence
- No causal overstatement introduced
- No recommendation exceeds evidence strength
- Risks are explicitly acknowledged
- Uncertainty is transparently communicated