# PROCESS SUPPORT — Manual Spot Check Note

Date: 2026-04-06  
Topic/Dataset: Market Structure Historical Analysis (Consistency Layer)

## Purpose

Document a short manual validation spot-check across raw summary information, processed daily outputs, and weekly classified outputs.

This note supplements automated validation already recorded in the PROCESS log.

---

## Spot-Check Scope

Reviewed or targeted rows:

1. Raw summary reference for `XLB`
2. Raw summary reference for `XLC`
3. `historical_ratio_panel_common_window.csv`
4. `historical_weekly_structure_classification_common_window.csv`
5. Process-level timing and coverage outputs

---

## Manual Spot-Check Results

| Check ID | File / Source | Exact row or date reviewed | Expected condition | Result | Notes |
|---|---|---|---|---|---|
| 1 | Raw download summary | `XLB` start/end = `2010-01-04` to `2026-04-06` | Full-history ETF should span full baseline range | Pass | Confirmed from successful download log |
| 2 | Raw download summary | `XLC` start/end = `2018-06-19` to `2026-04-06` | Later-inception ETF should start later than baseline | Pass | Confirms structural coverage gap |
| 3 | `historical_weekly_structure_classification_common_window.csv` | `2018-08-10`, `XLB` | Row should be classification-ready with valid ratio and explicit direction | Pass | `direction = LH/LL`, `classification_ready = True` |
| 4 | `historical_weekly_structure_classification_common_window.csv` | `2018-08-10`, `XLC` | Common-window start should include XLC as classification-ready | Pass | `direction = LH/LL`, `classification_ready = True` |
| 5 | `historical_weekly_structure_classification_common_window.csv` | `2018-08-10`, `XLF` | Same weekly date may legitimately show a different direction than XLB/XLC | Pass | `direction = HH/HL`, `classification_ready = True` |
| 6 | `historical_ratio_panel_common_window.csv` | earliest common-window daily date in output set | Common-window daily panel should only include dates where all 11 sectors have non-null ratio coverage | Pass | Row count structure is consistent with full 11-sector overlap |
| 7 | `historical_weekly_structure_date_coverage.csv` | first common-window weekly date | Weekly common-window should begin only when all 11 sectors are classification-ready | Pass | Common-window weekly start aligns with `2018-08-10` |
| 8 | `weekly_structure_transition_matrix.csv` | full matrix | 3×3 matrix should contain only HH/HL, LH/LL, TRANSITION states | Pass | Matrix contains valid state set only |

---

## Checks still recommended locally

The following checks should still be performed directly against local raw CSV files because those raw files were not uploaded into this review context:

| Check ID | Local file | Exact row/date to verify | Expected result |
|---|---|---|---|
| 9 | `data/raw/XLB.csv` | first row (`2010-01-04`) | `Adj Close` non-null and date equals baseline start |
| 10 | `data/raw/XLC.csv` | first row (`2018-06-19`) | first available row matches later-inception start |
| 11 | `cases/market-structure-consistency/outputs/02_process/historical_ratio_panel.csv` | `ticker = XLC`, `date < 2018-06-19` | `adj_close` and `ratio_value` should be null before inception |
| 12 | `cases/market-structure-consistency/outputs/02_process/historical_weekly_structure_classification.csv` | one early XLB row before 8 valid weeks accumulate | `direction = INSUFFICIENT_HISTORY` |
| 13 | `cases/market-structure-consistency/outputs/02_process/historical_weekly_structure_classification.csv` | one pre-inception XLC weekly row | `direction = NO_RATIO` |

These are exact target checks for local completion.

---

## Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Uploaded processed outputs are representative of local outputs | Needed for this review context | Local files may differ from uploaded versions | Compare local timestamps and row counts |
| Common-window files are sufficient to validate core weekly classification structure | They contain classification-ready overlap dates | They do not cover NO_RATIO / INSUFFICIENT_HISTORY cases | Perform local checks 11–13 |
| Download summary reflects the local raw-file start dates accurately | Needed because raw CSVs were not uploaded here | Raw file contents could differ from log output | Open local raw CSV first rows |

---

## Limitations

- This note includes completed checks for uploaded processed outputs and exact target checks for local-only files.
- It does not replace the automated validation already performed.
- It is a targeted review, not a full manual audit.

---

## Integrity Declaration

- No transformations are performed in this note
- No conclusions beyond the reviewed rows are made
- Rows not directly available in this review context are marked as local verification items