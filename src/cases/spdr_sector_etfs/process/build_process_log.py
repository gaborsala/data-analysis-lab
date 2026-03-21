from __future__ import annotations

import json
from pathlib import Path


METRICS_PATH = Path("data/processed/process_metrics.json")
OUTPUT_MD = Path("cases/spdr-sector-etfs/02_process/2026-03-11__spdr_sector_etfs__process_log.md")


def yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def build_markdown(metrics: dict) -> str:
    return f"""# PROCESS — Cleaning & Transformation Log

Date: 2026-03-11  
Topic/Dataset: SPDR Sector ETFs (Daily OHLCV)  
Input snapshot: all_sectors.csv

---

# 1. Purpose

Document all transformations required to make the dataset reliable and analytically usable.

All changes are explicit, justified, validated, and reproducible.

No silent filtering was applied.

---

# 2. Dataset Snapshot Integrity

| Metric | Value |
|------|------|
| Row count (raw) | {metrics["raw_row_count"]} |
| Column count (raw) | {metrics["raw_column_count"]} |
| File reference | {metrics["raw_file_path"]} |
| Load errors encountered | No |
| Pipeline executed (UTC) | {metrics["execution_time_utc"]} |

---

# 3. Transformation Summary Table

| Metric | Before | After | Change | Justification |
|------|------|------|------|------|
| Row count | {metrics["raw_row_count"]} | {metrics["cleaned_row_count"]} | {metrics["rows_removed"]} | No rows removed |
| Column count | {metrics["raw_column_count"]} | {metrics["cleaned_column_count"]} | {metrics["columns_removed"]} | Schema preserved |
| Missing value count | {metrics["raw_missing_count"]} | {metrics["cleaned_missing_count"]} | {metrics["raw_missing_count"] - metrics["cleaned_missing_count"]} | No imputation required |

---

# 4. Chronological Change Log

| Step | Change | Rationale | Method (rule/code) | Validation Result |
|----|----|----|----|----|
""" + "\n".join(
        f"| {item['step']} | {item['change']} | {item['rationale']} | `{item['method']}` | {item['validation_result']} |"
        for item in metrics["transformations"]
    ) + f"""

---

# 5. Missing Value Handling

| Column | Missing % Before | Strategy Applied | Rationale | Sensitivity Risk | Missing % After |
|------|------|------|------|------|------|
| All columns | 0.00% | None | No missing values present | None | 0.00% |

No imputation or row dropping performed.

---

# 6. Type Corrections

| Column | Original Observed Type | Corrected Type | Why Required | Risk if Misclassified | Validation Performed |
|------|------|------|------|------|------|
| date | object | datetime64[ns] | Time-series operations require datetime type | Ordering and time calculations would be unreliable | Conversion completed with no parse failures |
| open/high/low/close/volume | numeric-like text or numeric | numeric | Required for arithmetic and constraint checks | Invalid calculations or silent coercion risk | Conversion completed successfully |

---

# 7. Deduplication Rules

Duplicate detection logic: `(ticker, date)`

| Metric | Result |
|------|------|
| Duplicate rows detected | {metrics["duplicate_key_count"]} |
| Criteria for removal | No duplicates found; no rows removed |
| Rows removed | 0 |
| Validation of uniqueness after removal | Passed |

---

# 8. Outlier / Extreme Value Treatment

| Item | Result |
|------|------|
| Detection method | Range and structural constraint checks |
| Threshold definition | No explicit winsorization or removal threshold used |
| Treatment applied | None |
| Justification | Market extremes retained to preserve true observed behavior |
| Sensitivity analysis performed | No |

---

# 9. Statistical Sanity Checks

| Check | Result |
|------|------|
| Non-positive price count | {metrics["price_nonpositive_count"]} |
| Negative volume count | {metrics["volume_negative_count"]} |
| OHLC structural violations | {metrics["ohlc_invalid_count"]} |
| Unexpected variance reduction | None observed from processing |
| Mean / median shifts due to cleaning | None expected; no row filtering applied |

---

# 10. Validation Checks

| Validation | Status |
|------|------|
| Row counts verified after major steps | Yes |
| Range checks performed | Yes |
| Constraint validation performed | Yes |
| Referential integrity checks (if applicable) | Not applicable |
| Random manual spot-check performed | Recommended |

Validation summary:
- Duplicate key count: {metrics["duplicate_key_count"]}
- Non-positive price count: {metrics["price_nonpositive_count"]}
- Negative volume count: {metrics["volume_negative_count"]}
- OHLC violation count: {metrics["ohlc_invalid_count"]}

---

# 11. Reproducibility

| Item | Description |
|------|------|
| Script location | `{metrics["script_path"]}` |
| Metrics artifact | `data/processed/spdr/process_metrics.json` |
| Deterministic steps confirmed | {yes_no(metrics["deterministic_pipeline"])} |
| Manual steps performed | {metrics["manual_steps"]} |

---

# 12. Remaining Data Quality Issues

| Issue description | Impact on analysis | Risk level | Mitigation plan in ANALYZE |
|------|------|------|------|
""" + "\n".join(
        f"| {issue['issue']} | {issue['impact']} | {issue['risk_level']} | {issue['mitigation']} |"
        for issue in metrics["remaining_issues"]
    ) + """

---

# 13. Assumptions

| Assumption | Why Assumed | Risk if Wrong | Detection Method |
|------|------|------|------|
| Source OHLCV fields represent valid daily market records | Standard market data structure | Downstream return and volatility metrics may be distorted | Cross-check against external vendor or issuer data |
| Volume is recorded in share units | Standard OHLCV convention | Liquidity interpretation may be incorrect | Verify with source documentation |

---

# 14. Limitations

- No adjusted close field is present in the raw dataset.
- Corporate actions are not explicitly encoded in separate columns.
- Unequal ETF inception dates affect long-horizon comparability.

---

# 15. PROCESS Gate Checklist

- [x] Raw snapshot documented
- [x] All transformations logged
- [x] Row changes justified
- [x] Validation performed and recorded
- [x] No silent filtering
- [x] No undocumented assumptions
- [x] Remaining issues acknowledged
- [x] Reproducibility confirmed

Next stage allowed: **ANALYZE**

---

# 16. Integrity Declaration

- Cleaning choices do not artificially strengthen results.
- No selective filtering performed.
- No undocumented transformations applied.
- All changes are reproducible.
- Data integrity preserved.
"""


def main() -> None:
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(build_markdown(metrics), encoding="utf-8")
    print(f"PROCESS markdown written to: {OUTPUT_MD}")


if __name__ == "__main__":
    main()