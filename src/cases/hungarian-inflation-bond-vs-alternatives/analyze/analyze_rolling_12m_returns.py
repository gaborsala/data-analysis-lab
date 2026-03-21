"""
ANALYZE — Rolling 12-Month Annualized Returns
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Compute trailing 12-month compounded returns for ETF alternatives using
PROCESS monthly outputs, then generate summary tables for:

- full-history mode
- common-window mode

Primary outputs
---------------
- 03_ANALYZE/outputs/tables/rolling_12m_return_summary_full_history.csv
- 03_ANALYZE/outputs/tables/rolling_12m_return_summary_common_window.csv
- 03_ANALYZE/outputs/tables/rolling_12m_returns_detail_full_history.csv
- 03_ANALYZE/outputs/tables/rolling_12m_returns_detail_common_window.csv
- 03_ANALYZE/outputs/logs/analyze_rolling_12m_returns.log

Assumptions
-----------
1. PROCESS outputs contain a monthly ETF panel with either:
   - a monthly return column, or
   - a price-like column from which monthly returns can be computed.
2. The monthly panel includes a ticker identifier and a month/date field.
3. PROCESS already removed pre-inception null padding and active-window null issues.
4. Full-history and common-window are both required because XLC and XLRE start later.

Limitations
-----------
1. This script is descriptive and historical only.
2. Rolling 12-month return windows do not predict future annual returns.
3. Results remain sensitive to exact benchmark framing, which is checked separately.
4. If actual PROCESS filenames differ from expected candidates, candidate lists may need adjustment.

Validation checks performed/recommended
---------------------------------------
Performed:
- input file exists
- normalized columns loaded
- required ticker/date fields present
- monotonic month ordering checked
- rolling windows computed only after sorting
- summary tables checked for infinite values

Recommended:
- manual spot-check one ticker against Excel/pandas calculation
- reconcile output ticker counts with PROCESS coverage summary
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from common_analyze_utils import (
    COMMON_WINDOW,
    FULL_HISTORY,
    VALID_MODES,
    AnalyzePaths,
    apply_window_mode,
    assert_no_infinite_values,
    build_analyze_paths,
    build_run_metadata,
    compute_monthly_returns_from_price,
    compute_rolling_12m_returns,
    ensure_output_dirs,
    format_pct,
    infer_return_column,
    infer_ticker_column,
    load_monthly_panel_from_process,
    summarize_rolling_returns,
    validate_required_columns,
    write_table,
    write_text,
)


def prepare_monthly_returns(df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
    """
    Ensure monthly panel contains a return column.

    Returns
    -------
    (df_with_returns, ticker_col, return_col)
    """
    ticker_col = infer_ticker_column(df)

    try:
        return_col = infer_return_column(df)
        validate_required_columns(df, [ticker_col, "month_end", return_col], "monthly_panel")
        out = df.copy()
    except KeyError:
        out = compute_monthly_returns_from_price(
            df,
            ticker_col=ticker_col,
            date_col="month_end",
            price_col=None,
            out_col="monthly_return",
        )
        return_col = "monthly_return"

    return out, ticker_col, return_col


def run_for_mode(
    monthly_df: pd.DataFrame,
    mode: str,
    paths: AnalyzePaths,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run rolling 12m return analysis for one mode.

    Returns
    -------
    detail_df, summary_df
    """
    monthly_df, ticker_col, return_col = prepare_monthly_returns(monthly_df)

    filtered = apply_window_mode(
        monthly_df,
        mode=mode,
        ticker_col=ticker_col,
        date_col="month_end",
    ).copy()

    filtered = compute_rolling_12m_returns(
        filtered,
        ticker_col=ticker_col,
        date_col="month_end",
        return_col=return_col,
        out_col="rolling_12m_return",
        min_periods=12,
    )

    summary = summarize_rolling_returns(
        filtered,
        mode=mode,
        ticker_col=ticker_col,
        rolling_col="rolling_12m_return",
    )

    numeric_cols = [
        "mean_rolling_12m_return",
        "median_rolling_12m_return",
        "min_rolling_12m_return",
        "max_rolling_12m_return",
    ]
    assert_no_infinite_values(summary, numeric_cols, "rolling_return_summary")

    summary[numeric_cols] = summary[numeric_cols].apply(format_pct)

    detail_cols = [ticker_col, "month_end", return_col, "rolling_12m_return"]
    detail = filtered[detail_cols].copy()
    detail["mode"] = mode

    return detail, summary


def save_mode_outputs(
    detail_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    mode: str,
    paths: AnalyzePaths,
) -> None:
    """
    Save detail and summary tables for one mode.
    """
    suffix = "full_history" if mode == FULL_HISTORY else "common_window"

    detail_path = paths.outputs_tables_dir / f"rolling_12m_returns_detail_{suffix}.csv"
    summary_path = paths.outputs_tables_dir / f"rolling_12m_return_summary_{suffix}.csv"

    write_table(detail_df, detail_path, index=False)
    write_table(summary_df, summary_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute rolling 12-month return outputs for ANALYZE stage."
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="Case-study root directory containing 02_PROCESS/ and 03_ANALYZE/.",
    )
    parser.add_argument(
        "--process-dir",
        type=str,
        default="02_PROCESS/outputs",
        help="Relative path from project root to PROCESS outputs directory.",
    )
    parser.add_argument(
        "--analyze-dir",
        type=str,
        default="03_ANALYZE",
        help="Relative path from project root to ANALYZE directory.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="both",
        help="Mode to run: full-history, common-window, or both.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    paths = build_analyze_paths(
        project_root=args.project_root,
        process_dir=args.process_dir,
        analyze_dir=args.analyze_dir,
    )
    ensure_output_dirs(paths)

    monthly_df = load_monthly_panel_from_process(paths.process_dir)

    selected_modes: list[str]
    if args.mode == "both":
        selected_modes = [FULL_HISTORY, COMMON_WINDOW]
    else:
        if args.mode not in VALID_MODES:
            raise ValueError(
                f"Invalid --mode value '{args.mode}'. Use one of: full-history, common-window, both."
            )
        selected_modes = [args.mode]

    log_lines: list[str] = []
    for mode in selected_modes:
        detail_df, summary_df = run_for_mode(
            monthly_df=monthly_df,
            mode=mode,
            paths=paths,
        )
        save_mode_outputs(
            detail_df=detail_df,
            summary_df=summary_df,
            mode=mode,
            paths=paths,
        )

        log_lines.append(
            build_run_metadata(
                mode=mode,
                n_rows_input=len(monthly_df),
                n_rows_output=len(detail_df),
                notes=[
                    f"summary_rows={len(summary_df)}",
                    f"detail_non_null_rolling_windows={int(detail_df['rolling_12m_return'].notna().sum())}",
                    "rolling return formula = trailing 12-month compounded return",
                ],
            )
        )

    log_text = "\n\n".join(log_lines)
    write_text(log_text, paths.outputs_logs_dir / "analyze_rolling_12m_returns.log")


if __name__ == "__main__":
    main()