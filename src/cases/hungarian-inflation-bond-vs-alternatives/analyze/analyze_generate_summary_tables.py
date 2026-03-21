"""
ANALYZE — Generate Summary Tables
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Combine core ANALYZE outputs into comparison-ready tables for the final
ANALYZE artifact and downstream audit checks.

This script reads:
- rolling 12m return summaries
- threshold exceedance summaries
- volatility / max drawdown summaries
- benchmark definition check

Then produces:
- mode-specific combined comparison tables
- cross-mode comparison table
- benchmark interpretation note table

Primary outputs
---------------
- 03_ANALYZE/outputs/tables/analyze_summary_full_history.csv
- 03_ANALYZE/outputs/tables/analyze_summary_common_window.csv
- 03_ANALYZE/outputs/tables/analyze_mode_comparison.csv
- 03_ANALYZE/outputs/tables/benchmark_interpretation_notes.csv
- 03_ANALYZE/outputs/logs/analyze_generate_summary_tables.log

Assumptions
-----------
1. Upstream ANALYZE scripts have already run successfully.
2. Ticker identifiers are consistent across output tables.
3. The summary tables use one row per ticker per mode.
4. Benchmark candidate columns surfaced in benchmark_definition_check.csv are sufficient
   for interpretation review.

Limitations
-----------
1. This script only combines existing outputs; it does not create new metrics.
2. If upstream filenames or schemas changed, this script must be updated.
3. Benchmark interpretation notes are descriptive and should still be reviewed manually.
4. Cross-mode differences may reflect sample window changes, not true asset behavior shifts.

Validation checks performed/recommended
---------------------------------------
Performed:
- required upstream files exist
- key join columns exist
- one-row-per-ticker shape expected for summaries
- finite checks on key numeric columns after merge

Recommended:
- inspect merged row counts against expected ticker counts
- compare common-window and full-history output manually for one ticker
- review benchmark interpretation notes before final conclusions
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from common_analyze_utils import (
    AnalyzePaths,
    assert_no_infinite_values,
    build_analyze_paths,
    build_run_metadata,
    ensure_output_dirs,
    format_pct,
    load_table,
    write_table,
    write_text,
)

FULL_HISTORY_SUFFIX = "full_history"
COMMON_WINDOW_SUFFIX = "common_window"


def _load_required_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    return load_table(path)


def _infer_ticker_col(df: pd.DataFrame) -> str:
    candidates = ["ticker", "symbol", "asset", "series", "etf", "instrument"]
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f"Could not infer ticker column from columns: {list(df.columns)}")


def _prepare_mode_summary(
    rolling_path: Path,
    exceedance_path: Path,
    risk_path: Path,
    mode_label: str,
) -> pd.DataFrame:
    """
    Merge per-mode summary outputs into one comparison table.
    """
    rolling = _load_required_csv(rolling_path)
    exceedance = _load_required_csv(exceedance_path)
    risk = _load_required_csv(risk_path)

    ticker_col = _infer_ticker_col(rolling)

    if ticker_col not in exceedance.columns or ticker_col not in risk.columns:
        raise KeyError("Ticker column mismatch across ANALYZE summary tables.")

    merge_keys = [ticker_col]
    if "mode" in rolling.columns and "mode" in exceedance.columns and "mode" in risk.columns:
        merge_keys.append("mode")

    merged = rolling.merge(exceedance, on=merge_keys, how="inner")
    merged = merged.merge(risk, on=merge_keys, how="inner")

    expected_mode = mode_label.replace("_", "-")
    if "mode" in merged.columns:
        merged = merged[merged["mode"] == expected_mode].copy()

    numeric_candidates = [
        "mean_rolling_12m_return",
        "median_rolling_12m_return",
        "min_rolling_12m_return",
        "max_rolling_12m_return",
        "threshold",
        "exceedance_rate",
        "annualized_volatility",
        "max_drawdown",
    ]
    numeric_cols = [c for c in numeric_candidates if c in merged.columns]
    if numeric_cols:
        assert_no_infinite_values(merged, numeric_cols, f"merged_summary_{mode_label}")
        merged[numeric_cols] = merged[numeric_cols].apply(format_pct)

    sort_cols = [c for c in ["exceedance_rate", "mean_rolling_12m_return"] if c in merged.columns]
    if sort_cols:
        merged = merged.sort_values(sort_cols, ascending=[False] * len(sort_cols)).reset_index(drop=True)

    return merged


def _build_mode_comparison(full_df: pd.DataFrame, common_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build cross-mode comparison table by ticker.
    """
    ticker_col = _infer_ticker_col(full_df)

    full = full_df.copy()
    common = common_df.copy()

    full = full.rename(
        columns={
            "valid_windows": "valid_windows_full_history",
            "mean_rolling_12m_return": "mean_rolling_12m_return_full_history",
            "median_rolling_12m_return": "median_rolling_12m_return_full_history",
            "min_rolling_12m_return": "min_rolling_12m_return_full_history",
            "max_rolling_12m_return": "max_rolling_12m_return_full_history",
            "threshold": "threshold_full_history",
            "windows_above_threshold": "windows_above_threshold_full_history",
            "total_valid_windows": "total_valid_windows_full_history",
            "exceedance_rate": "exceedance_rate_full_history",
            "annualized_volatility": "annualized_volatility_full_history",
            "max_drawdown": "max_drawdown_full_history",
            "n_return_obs": "n_return_obs_full_history",
        }
    )

    common = common.rename(
        columns={
            "valid_windows": "valid_windows_common_window",
            "mean_rolling_12m_return": "mean_rolling_12m_return_common_window",
            "median_rolling_12m_return": "median_rolling_12m_return_common_window",
            "min_rolling_12m_return": "min_rolling_12m_return_common_window",
            "max_rolling_12m_return": "max_rolling_12m_return_common_window",
            "threshold": "threshold_common_window",
            "windows_above_threshold": "windows_above_threshold_common_window",
            "total_valid_windows": "total_valid_windows_common_window",
            "exceedance_rate": "exceedance_rate_common_window",
            "annualized_volatility": "annualized_volatility_common_window",
            "max_drawdown": "max_drawdown_common_window",
            "n_return_obs": "n_return_obs_common_window",
        }
    )

    drop_cols_full = [c for c in ["mode"] if c in full.columns]
    drop_cols_common = [c for c in ["mode"] if c in common.columns]
    full = full.drop(columns=drop_cols_full)
    common = common.drop(columns=drop_cols_common)

    comparison = full.merge(common, on=[ticker_col], how="outer")

    if (
        "exceedance_rate_full_history" in comparison.columns
        and "exceedance_rate_common_window" in comparison.columns
    ):
        comparison["exceedance_rate_diff_common_minus_full"] = (
            comparison["exceedance_rate_common_window"] - comparison["exceedance_rate_full_history"]
        )

    if (
        "mean_rolling_12m_return_full_history" in comparison.columns
        and "mean_rolling_12m_return_common_window" in comparison.columns
    ):
        comparison["mean_rolling_12m_return_diff_common_minus_full"] = (
            comparison["mean_rolling_12m_return_common_window"]
            - comparison["mean_rolling_12m_return_full_history"]
        )

    if (
        "annualized_volatility_full_history" in comparison.columns
        and "annualized_volatility_common_window" in comparison.columns
    ):
        comparison["annualized_volatility_diff_common_minus_full"] = (
            comparison["annualized_volatility_common_window"]
            - comparison["annualized_volatility_full_history"]
        )

    if (
        "max_drawdown_full_history" in comparison.columns
        and "max_drawdown_common_window" in comparison.columns
    ):
        comparison["max_drawdown_diff_common_minus_full"] = (
            comparison["max_drawdown_common_window"]
            - comparison["max_drawdown_full_history"]
        )

    diff_cols = [c for c in comparison.columns if c.endswith("_diff_common_minus_full")]
    if diff_cols:
        assert_no_infinite_values(comparison.fillna(0), diff_cols, "mode_comparison")
        comparison[diff_cols] = comparison[diff_cols].apply(format_pct)

    return comparison.sort_values(ticker_col).reset_index(drop=True)


def _build_benchmark_interpretation_notes(benchmark_check: pd.DataFrame) -> pd.DataFrame:
    """
    Create a lightweight review table for benchmark interpretation.
    """
    out = benchmark_check.copy()

    if "benchmark_column" not in out.columns:
        raise KeyError("benchmark_definition_check.csv must contain 'benchmark_column'.")

    notes = []
    for _, row in out.iterrows():
        col = row["benchmark_column"]
        non_null_count = row.get("non_null_count", 0)
        median_value = row.get("median_value", None)

        if col == "NO_CANDIDATE_FOUND":
            review_note = "No benchmark candidate found automatically; manual threshold selection required."
            suitability = "low"
        elif non_null_count == 0:
            review_note = "Column exists but has no usable non-null values."
            suitability = "low"
        else:
            review_note = (
                "Candidate available; verify definition against PROCESS bond normalization rules "
                "before final exceedance interpretation."
            )
            suitability = "review"

        notes.append(
            {
                "benchmark_column": col,
                "non_null_count": non_null_count,
                "median_value": median_value,
                "review_note": review_note,
                "suitability_flag": suitability,
            }
        )

    return pd.DataFrame(notes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine ANALYZE outputs into summary comparison tables."
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="Case-study root directory containing 03_ANALYZE/.",
    )
    parser.add_argument(
        "--analyze-dir",
        type=str,
        default="03_ANALYZE",
        help="Relative path from project root to ANALYZE directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    paths = build_analyze_paths(
        project_root=args.project_root,
        process_dir="02_PROCESS/outputs",
        analyze_dir=args.analyze_dir,
    )
    ensure_output_dirs(paths)

    tables_dir = paths.outputs_tables_dir

    full_summary = _prepare_mode_summary(
        rolling_path=tables_dir / "rolling_12m_return_summary_full_history.csv",
        exceedance_path=tables_dir / "threshold_exceedance_full_history.csv",
        risk_path=tables_dir / "volatility_drawdown_full_history.csv",
        mode_label=FULL_HISTORY_SUFFIX,
    )
    common_summary = _prepare_mode_summary(
        rolling_path=tables_dir / "rolling_12m_return_summary_common_window.csv",
        exceedance_path=tables_dir / "threshold_exceedance_common_window.csv",
        risk_path=tables_dir / "volatility_drawdown_common_window.csv",
        mode_label=COMMON_WINDOW_SUFFIX,
    )

    mode_comparison = _build_mode_comparison(full_summary, common_summary)

    benchmark_check = _load_required_csv(tables_dir / "benchmark_definition_check.csv")
    benchmark_notes = _build_benchmark_interpretation_notes(benchmark_check)

    write_table(full_summary, tables_dir / "analyze_summary_full_history.csv", index=False)
    write_table(common_summary, tables_dir / "analyze_summary_common_window.csv", index=False)
    write_table(mode_comparison, tables_dir / "analyze_mode_comparison.csv", index=False)
    write_table(benchmark_notes, tables_dir / "benchmark_interpretation_notes.csv", index=False)

    log_text = "\n\n".join(
        [
            build_run_metadata(
                mode="full-history",
                n_rows_input=len(full_summary),
                n_rows_output=len(full_summary),
                notes=[
                    f"combined_summary_rows={len(full_summary)}",
                    "source_tables=rolling_12m_return_summary_full_history.csv + threshold_exceedance_full_history.csv + volatility_drawdown_full_history.csv",
                ],
            ),
            build_run_metadata(
                mode="common-window",
                n_rows_input=len(common_summary),
                n_rows_output=len(common_summary),
                notes=[
                    f"combined_summary_rows={len(common_summary)}",
                    "source_tables=rolling_12m_return_summary_common_window.csv + threshold_exceedance_common_window.csv + volatility_drawdown_common_window.csv",
                ],
            ),
            build_run_metadata(
                mode="cross-mode",
                n_rows_input=len(full_summary) + len(common_summary),
                n_rows_output=len(mode_comparison),
                notes=[
                    f"benchmark_note_rows={len(benchmark_notes)}",
                    "cross-mode differences are descriptive and may reflect sample-window changes",
                ],
            ),
        ]
    )

    write_text(log_text, tables_dir.parent / "logs" / "analyze_generate_summary_tables.log")


if __name__ == "__main__":
    main()