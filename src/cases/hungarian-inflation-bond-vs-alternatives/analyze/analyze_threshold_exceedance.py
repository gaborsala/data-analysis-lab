"""
ANALYZE — Threshold Exceedance Probability
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Compute the share of valid rolling 12-month return windows where each asset
exceeded the selected annual bond benchmark threshold.

This script supports:
- full-history mode
- common-window mode

Primary outputs
---------------
- 03_ANALYZE/outputs/tables/threshold_exceedance_full_history.csv
- 03_ANALYZE/outputs/tables/threshold_exceedance_common_window.csv
- 03_ANALYZE/outputs/tables/benchmark_definition_check.csv
- 03_ANALYZE/outputs/logs/analyze_threshold_exceedance.log

Assumptions
-----------
1. Rolling 12-month returns are computed from monthly PROCESS outputs.
2. A valid annual bond threshold exists either:
   - as a column in the PROCESS monthly merged panel, or
   - as a user-supplied constant threshold.
3. The threshold is expressed in decimal form:
   - 0.05 = 5%
4. PROCESS already normalized bond-related percentage-point fields.

Limitations
-----------
1. Historical threshold exceedance is descriptive, not predictive.
2. Exceedance rate depends on benchmark definition and time alignment.
3. A high exceedance rate does not imply moderate risk by itself.
4. If PROCESS column names differ from expected candidates, explicit override may be needed.

Validation checks performed/recommended
---------------------------------------
Performed:
- monthly panel load check
- mode validation
- required columns check
- benchmark candidate table generation
- finite exceedance-rate check

Recommended:
- verify benchmark field against PROCESS documentation
- spot-check a few exceedance flags manually
- compare ticker counts between rolling-return summary and exceedance outputs
"""

from __future__ import annotations

import argparse
from typing import Optional

import pandas as pd

from common_analyze_utils import (
    COMMON_WINDOW,
    FULL_HISTORY,
    VALID_MODES,
    AnalyzePaths,
    add_constant_threshold,
    apply_window_mode,
    assert_no_infinite_values,
    build_analyze_paths,
    build_benchmark_definition_check,
    build_run_metadata,
    compute_monthly_returns_from_price,
    compute_rolling_12m_returns,
    compute_threshold_exceedance,
    ensure_output_dirs,
    format_pct,
    infer_benchmark_column,
    infer_return_column,
    infer_ticker_column,
    load_monthly_panel_from_process,
    validate_required_columns,
    write_table,
    write_text,
)


def prepare_monthly_returns(df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
    """
    Ensure the monthly panel includes a monthly return column.
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


def prepare_threshold_column(
    df: pd.DataFrame,
    threshold_value: Optional[float] = None,
    threshold_col_override: Optional[str] = None,
) -> tuple[pd.DataFrame, str, str]:
    """
    Prepare the threshold column to use in exceedance logic.

    Returns
    -------
    df_with_threshold, threshold_col_name, threshold_source
    """
    out = df.copy()

    if threshold_value is not None:
        out = add_constant_threshold(
            out,
            threshold_value=float(threshold_value),
            out_col="benchmark_threshold",
        )
        return out, "benchmark_threshold", f"constant:{threshold_value:.6f}"

    if threshold_col_override:
        validate_required_columns(out, [threshold_col_override], "monthly_panel")
        return out, threshold_col_override, f"column_override:{threshold_col_override}"

    inferred = infer_benchmark_column(out)
    validate_required_columns(out, [inferred], "monthly_panel")
    return out, inferred, f"column_inferred:{inferred}"


def run_for_mode(
    monthly_df: pd.DataFrame,
    mode: str,
    threshold_value: Optional[float] = None,
    threshold_col_override: Optional[str] = None,
) -> tuple[pd.DataFrame, str]:
    """
    Run threshold exceedance analysis for one mode.

    Returns
    -------
    exceedance_df, threshold_source
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

    filtered, threshold_col, threshold_source = prepare_threshold_column(
        filtered,
        threshold_value=threshold_value,
        threshold_col_override=threshold_col_override,
    )

    exceedance = compute_threshold_exceedance(
        filtered,
        mode=mode,
        threshold_col=threshold_col,
        ticker_col=ticker_col,
        rolling_col="rolling_12m_return",
    )

    numeric_cols = ["threshold", "exceedance_rate"]
    assert_no_infinite_values(exceedance, numeric_cols, "threshold_exceedance")

    exceedance[numeric_cols] = exceedance[numeric_cols].apply(format_pct)

    return exceedance, threshold_source


def save_mode_outputs(
    exceedance_df: pd.DataFrame,
    mode: str,
    paths: AnalyzePaths,
) -> None:
    """
    Save threshold exceedance output for one mode.
    """
    suffix = "full_history" if mode == FULL_HISTORY else "common_window"
    out_path = paths.outputs_tables_dir / f"threshold_exceedance_{suffix}.csv"
    write_table(exceedance_df, out_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute threshold exceedance outputs for ANALYZE stage."
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
    parser.add_argument(
        "--threshold-value",
        type=float,
        default=None,
        help="Optional constant annual threshold in decimal form. Example: 0.05 for 5%%.",
    )
    parser.add_argument(
        "--threshold-col",
        type=str,
        default=None,
        help="Optional threshold column name to use instead of inference.",
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

    benchmark_check = build_benchmark_definition_check(monthly_df)
    write_table(
        benchmark_check,
        paths.outputs_tables_dir / "benchmark_definition_check.csv",
        index=False,
    )

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
        exceedance_df, threshold_source = run_for_mode(
            monthly_df=monthly_df,
            mode=mode,
            threshold_value=args.threshold_value,
            threshold_col_override=args.threshold_col,
        )
        save_mode_outputs(
            exceedance_df=exceedance_df,
            mode=mode,
            paths=paths,
        )

        log_lines.append(
            build_run_metadata(
                mode=mode,
                n_rows_input=len(monthly_df),
                n_rows_output=len(exceedance_df),
                notes=[
                    f"threshold_source={threshold_source}",
                    f"tickers_output={len(exceedance_df)}",
                    f"windows_total={int(exceedance_df['total_valid_windows'].sum())}",
                    f"windows_above_total={int(exceedance_df['windows_above_threshold'].sum())}",
                ],
            )
        )

    write_text(
        "\n\n".join(log_lines),
        paths.outputs_logs_dir / "analyze_threshold_exceedance.log",
    )


if __name__ == "__main__":
    main()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          