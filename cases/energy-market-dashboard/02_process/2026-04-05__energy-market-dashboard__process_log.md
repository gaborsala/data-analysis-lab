# PROCESS — Cleaning & Transformation Log

Date: 2026-04-05  
Topic/Dataset: energy-market-dashboard  
Input snapshot: local raw CSV batch (`wti_raw.csv`, `brent_raw.csv`, `natgas_raw.csv`, `xle_raw.csv`, `spy_raw.csv`)

## 1. Purpose

Document all transformations required to make the energy market raw files analytically usable for a portfolio-ready dashboard case.

This PROCESS stage converts five separate raw instrument files into:

- one combined panel dataset
- one aligned common-date panel dataset
- supporting audit tables for reproducibility and validation

All changes are explicit, justified, validated, and reproducible.

## 2. Dataset Snapshot Integrity

Before any transformation:

| File | Ticker | Row Count | Column Count | Min Date | Max Date | Duplicate (`date`,`ticker`) Rows | Missing Values |
|---|---|---:|---:|---|---|---:|---:|
| `wti_raw.csv` | `CL=F` | 1,258 | 8 | 2021-04-05 | 2026-04-02 | 0 | 0 |
| `brent_raw.csv` | `BZ=F` | 1,259 | 8 | 2021-04-05 | 2026-04-02 | 0 | 0 |
| `natgas_raw.csv` | `NG=F` | 1,259 | 8 | 2021-04-05 | 2026-04-02 | 0 | 0 |
| `xle_raw.csv` | `XLE` | 1,256 | 8 | 2021-04-05 | 2026-04-02 | 0 | 0 |
| `spy_raw.csv` | `SPY` | 1,256 | 8 | 2021-04-05 | 2026-04-02 | 0 | 0 |

**Row count (raw total):** 6,288  
**Column count (raw):** 8  
**File hash or version reference:** local raw snapshot generated from patched fetch pipeline  
**Load errors encountered:** No, at PROCESS stage

## 3. Transformation Summary Table (Mandatory)

| Metric | Before | After (Combined Panel) | After (Aligned Panel) | Change | Justification |
|---|---:|---:|---:|---|---|
| Row count | 6,288 | 6,288 | 6,280 | -8 rows | Remove dates without full 5-ticker coverage |
| Column count | 8 | 8 | 8 | No change | Preserve raw schema for downstream comparability |
| Missing value count | 0 | 0 | 0 | No change | No imputation or null-handling required |

## 4. Chronological Change Log

| Step | Change | Rationale | Method (rule/code) | Validation Result |
|---|---|---|---|---|
| 1 | Load five raw CSV files | Establish deterministic raw input set | `pd.read_csv()` for each expected file | All files loaded successfully |
| 2 | Validate schema against expected columns | Prevent silent schema drift | Exact column whitelist check | All files passed |
| 3 | Validate ticker identity per file | Prevent file-to-ticker mismatch | Compare observed ticker set to expected ticker | All files passed |
| 4 | Parse `date` to datetime | Enable time-based sorting and alignment | `pd.to_datetime(..., errors="raise")` | No parse failures |
| 5 | Validate uniqueness on `date + ticker` | Protect panel integrity | Duplicate check on composite key | 0 duplicates found |
| 6 | Validate raw numeric integrity | Prevent downstream metric distortion | Check for nulls, negative values, `high < low` | All checks passed |
| 7 | Concatenate all files | Create full cross-instrument panel | `pd.concat()` | Combined row count = 6,288 |
| 8 | Sort by `date`, `ticker` | Enforce deterministic ordering | `.sort_values(["date", "ticker"])` | Order applied successfully |
| 9 | Build date coverage table | Measure cross-instrument overlap | `groupby(date).nunique()` | 1,259 distinct dates observed |
| 10 | Keep only dates with all 5 tickers present | Create comparable aligned panel | Filter where `ticker_count == 5` | 1,256 common dates retained |
| 11 | Save outputs and audits | Preserve reproducibility | `.to_csv()` | Output files generated successfully |

## 5. Missing Value Handling

No missing values were present in the raw snapshot.

| Column Group | Missing % Before | Strategy Applied | Rationale | Sensitivity Risk | Missing % After |
|---|---:|---|---|---|---:|
| All columns | 0.0% | None | No missing values detected | Low | 0.0% |

No imputation was performed.

## 6. Type Corrections

| Column | Original Observed Type | Corrected Type | Why Required | Risk if Misclassified | Validation Performed |
|---|---|---|---|---|---|
| `date` | string-formatted date | datetime | Required for alignment, sorting, and time-window logic | Incorrect time ordering and bad overlap logic | Parse completed without errors |
| `adj_close`, `close`, `high`, `low`, `open`, `volume` | numeric | no change | Already analytically usable | Low | Range and null checks passed |
| `ticker` | string | no change | Already analytically usable | Low | File-level ticker validation passed |

Type changes are traceable to PREPARE expectations.

## 7. Deduplication Rules

**Duplicate detection logic:**  
Check duplicate rows using composite key `date + ticker`.

**Criteria for removal:**  
Remove only if duplicate composite keys exist.

**Rows removed (count and %):**  
0 rows removed (0.00%)

**Validation of uniqueness after removal:**  
No duplicate composite keys were present before or after processing.

No deduplication was required.

## 8. Outlier / Extreme Value Treatment

**Detection method:**  
Not applicable in PROCESS for removal purposes

**Threshold definition:**  
None

**Treatment applied:**  
None

**Justification:**  
This case is a market-data dashboard. Extreme values may represent genuine market conditions and must be preserved for descriptive analysis.

**Sensitivity analysis performed:**  
No

No outlier capping, removal, or transformation was applied.

## 9. Statistical Sanity Checks

**Distribution before vs after:**  
No distributional manipulation was introduced. The aligned panel differs only by excluding dates without full five-instrument coverage.

**Unexpected variance reduction:**  
No unexplained variance reduction observed. Any reduction in downstream variation should be attributable only to date alignment.

**Mean / median shifts due to cleaning:**  
No cleaning-related value edits were performed. Only row exclusion from partial-coverage dates occurred.

**Integrity check on key metrics:**  
- Combined panel row count matches sum of input files: 6,288
- Aligned panel row count equals 1,256 common dates × 5 tickers = 6,280
- Aligned date window: 2021-04-05 to 2026-04-02
- No schema changes introduced

## 10. Validation Checks

**Row counts verified after each major step:** Yes  
**Range checks performed:** Yes  
**Constraint validation performed:** Yes  
**Referential integrity checks performed:** Yes  
**Random manual spot-check performed:** Recommended, not formally logged

### Explicit validation results

- all five expected raw files were present
- all files shared the same 8-column schema
- all files contained exactly one expected ticker
- no missing values were detected
- no negative values were detected in numeric fields
- no `high < low` anomalies were detected
- no duplicate `date + ticker` rows were detected
- 1,259 total dates existed in the combined panel
- 1,256 dates had full 5-ticker coverage
- aligned panel retained only full-coverage dates

## 11. Reproducibility

**Script location:**  
`src/cases/energy-market-dashboard/process/run_process_full.py`

**Version reference:**  
Deterministic pipeline version generated after replacing the earlier TODO scaffold

**Deterministic steps confirmed:**  
Yes

**Manual steps performed:**  
None in the processing logic itself

If transformation cannot be reproduced, PROCESS is invalid. Current PROCESS is reproducible.

## 12. Remaining Data Quality Issues

| Issue Description | Impact on Analysis | Risk Level | Mitigation Plan in ANALYZE |
|---|---|---|---|
| Futures and ETFs are not methodologically identical instruments | Mixed-asset comparisons require careful metric choice | Moderate | Compare `close` vs `adj_close` and justify selected field |
| Some dates exist for fewer than 5 tickers in full panel | Full-history comparison can become inconsistent | Low | Use aligned panel for cross-instrument comparisons |
| Volume is not directly comparable across futures and ETFs | Cross-asset volume interpretation may be misleading | Moderate | Exclude direct cross-asset volume conclusions |
| Slight raw row-count differences by ticker | Reflects calendar/coverage mismatch rather than corruption | Low | Document date alignment explicitly in ANALYZE |

No hidden data debt is left undocumented.

## 13. PROCESS Gate Checklist

- [x] Raw snapshot documented
- [x] All transformations logged
- [x] Row changes justified
- [x] Validation performed and recorded
- [x] No silent filtering
- [x] No undocumented assumptions
- [x] Remaining issues acknowledged
- [x] Reproducibility confirmed
- [x] Next stage allowed (ANALYZE)

## 14. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|---|---|---|---|
| Full-coverage dates are the correct basis for cross-instrument comparison | Dashboard comparison requires same-date observations | Metric comparisons may be biased if partial dates are retained | Compare combined vs aligned panel behavior |
| Preserving raw numeric values is preferable to early transformation | PROCESS should minimize analytical distortion | Some downstream metrics may need additional derived fields later | Validate derived metrics in ANALYZE |
| Schema stability will continue in future fetch runs | Current snapshot passed all checks | Future `yfinance` changes may break the pipeline | Re-run schema validation on each batch |

## 15. Limitations

- PROCESS does not resolve instrument methodology differences between futures and ETFs.
- PROCESS does not determine whether `close` or `adj_close` is the correct analytical basis; that belongs in ANALYZE.
- PROCESS does not perform statistical modeling or inferential testing.
- Random manual spot-checking was recommended but not formally logged in the current batch.

## 16. Integrity Declaration

- Cleaning choices do not artificially strengthen results
- No selective filtering was performed beyond explicit full-coverage date alignment
- No undocumented transformations were applied
- All changes are reproducible
- Data integrity was preserved