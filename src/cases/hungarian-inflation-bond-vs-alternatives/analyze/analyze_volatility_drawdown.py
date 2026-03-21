"""
ANALYZE — Volatility and Maximum Drawdown
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Compute historical risk summaries for each asset in:
- full-history mode
- common-window mode

Metrics produced
----------------
- annualized volatility from monthly returns
- maximum drawdown from cumulative growth path
- observation counts used in risk calculations

Primary outputs
---------------
- 03_ANALYZE/outputs/tables/volatility_drawdown_full_history.csv
- 03_ANALYZE/outputs/tables/volatility_drawdown_common_window.csv
- 03_ANALYZE/outputs/tables/cumulative_growth_detail_full_history.csv
- 03_ANALYZE/outputs/tables/cumulative_growth_detail_common_window.csv
- 03_ANALYZE/outputs/logs/analyze_volatility_drawdown.log

Assumptions
-----------
1. PROCESS outputs contain a monthly ETF panel with either:
   - a monthly return column, or
   - a price-like column from which monthly returns can be computed.
2. Monthly observations are ordered correctly after month_end normalization.
3. PROCESS already removed pre-inception padding and documented active-window null handling.
4. Full-history and common-window both matter because some tickers start later.

Limitations
-----------
1. Historical volatility and drawdown do not predict future risk.
2. Maximum drawdown is sample-period dependent.
3. Monthly-frequency drawdown is less granular than daily drawdown.
4. This script does not compare risk to the bond directly; it prepares evidence for ANALYZE.

Validation checks performed/recommended
---------------------------------------
Performed:
- monthly panel load check
- required field validation
- monotonic month ordering check
- finite-value check on summary metrics

Recommended:
- manually inspect one ticker cumulative growth path
- compare return observation counts across modes
- verify common-window boundaries match prior outputs
"""

from __future__ import annotations

import argparse

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
    compute_cumulative_growth,
    compute_drawdown_from_growth,
    compute_monthly_returns_from_price,
    ensure_output_dirs,
    format_pct,
    infer_return_column,
    infer_ticker_column,
    load_monthly_panel_from_process,
    summarize_volatility_drawdown,
    validate_required_columns,
    write_table,
    write_text,
)


def prepare_monthly_returns(df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
    """
    Ensure the monthly panel contains a monthly return column.

    Returns
    -------
    df_with_returns, ticker_col, return_col
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
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run volatility and drawdown analysis for one mode.

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

    filtered = compute_cumulative_growth(
        filtered,
        ticker_col=ticker_col,
        date_col="month_end",
        return_col=return_col,
        out_col="growth_index",
        start_value=1.0,
    )

    filtered = compute_drawdown_from_growth(
        filtered,
        ticker_col=ticker_col,
        growth_col="growth_index",
        out_col="drawdown",
    )

    summary = summarize_volatility_drawdown(
        filtered,
        mode=mode,
        ticker_col=ticker_col,
        return_col=return_col,
        drawdown_col="drawdown",
    )

    numeric_cols = ["annualized_volatility", "max_drawdown"]
    assert_no_infinite_values(summary, numeric_cols, "volatility_drawdown_summary")
    summary[numeric_cols] = summary[numeric_cols].apply(format_pct)

    detail_cols = [ticker_col, "month_end", return_col, "growth_index", "drawdown"]
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
    Save detail and summary outputs for one mode.
    """
    suffix = "full_history" if mode == FULL_HISTORY else "common_window"

    detail_path = paths.outputs_tables_dir / f"cumulative_growth_detail_{suffix}.csv"
    summary_path = paths.outputs_tables_dir / f"volatility_drawdown_{suffix}.csv"

    write_table(detail_df, detail_path, index=False)
    write_table(summary_df, summary_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute volatility and max drawdown outputs for ANALYZE stage."
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
                    f"detail_non_null_growth={int(detail_df['growth_index'].notna().sum())}",
                    f"detail_non_null_drawdown={int(detail_df['drawdown'].notna().sum())}",
                    "annualized volatility = std(monthly_return) * sqrt(12)",
                    "max drawdown = minimum drawdown from cumulative growth path",
                ],
            )
        )

    write_text(
        "\n\n".join(log_lines),
        paths.outputs_logs_dir / "analyze_volatility_drawdown.log",
    )


if __name__ == "__main__":
    main()