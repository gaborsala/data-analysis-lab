"""
ANALYZE — Generate Charts
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Create the missing chart outputs for the ANALYZE stage from the already
generated CSV tables.

Why this script is needed
-------------------------
The full ANALYZE run completed successfully, but the current pipeline only
produced tables and logs. The logs confirm that:
- rolling-return tables were generated for both modes
- threshold exceedance tables were generated for both modes
- volatility/drawdown tables were generated for both modes
- combined summary tables were generated successfully

No current script writes PNG chart files, so the absence of charts is expected.

Outputs
-------
- 03_ANALYZE/outputs/charts/rolling_12m_return_full_history.png
- 03_ANALYZE/outputs/charts/rolling_12m_return_common_window.png
- 03_ANALYZE/outputs/charts/threshold_exceedance_comparison.png
- 03_ANALYZE/outputs/charts/annualized_volatility_comparison.png
- 03_ANALYZE/outputs/charts/max_drawdown_comparison.png
- 03_ANALYZE/outputs/charts/cumulative_growth_comparison.png
- 03_ANALYZE/outputs/logs/analyze_generate_charts.log

Assumptions
-----------
1. The upstream ANALYZE scripts have already run successfully.
2. Required CSV files exist in 03_ANALYZE/outputs/tables/.
3. Ticker labels are consistent across generated summary tables.
4. Full-history and common-window tables are both required for auditability.

Limitations
-----------
1. Charts are descriptive only.
2. The cumulative growth chart uses the full-history detail table.
3. The rolling 12m line charts plot all tickers together, so visual density may be high.
4. This script does not make any financial interpretation.

Validation checks performed/recommended
---------------------------------------
Performed:
- required input table existence checks
- required columns validated before plotting
- output chart directory created if missing

Recommended:
- visually inspect ticker labels for readability
- confirm chart titles match artifact terminology
- use tables, not charts, as the primary evidence source in the markdown artifact
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from common_analyze_utils import (
    build_analyze_paths,
    ensure_output_dirs,
    load_table,
    write_text,
)


def require_columns(df: pd.DataFrame, required: list[str], name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")


def save_line_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    group_col: str,
    title: str,
    out_path: Path,
) -> None:
    plt.figure(figsize=(12, 7))
    for key, grp in df.groupby(group_col):
        grp = grp.sort_values(x_col)
        plt.plot(grp[x_col], grp[y_col], label=str(key))
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def save_bar_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    out_path: Path,
    ascending: bool = False,
) -> None:
    plot_df = df.sort_values(y_col, ascending=ascending).copy()
    plt.figure(figsize=(12, 7))
    plt.bar(plot_df[x_col].astype(str), plot_df[y_col])
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ANALYZE charts from summary tables.")
    parser.add_argument("--project-root", type=str, default=".")
    parser.add_argument("--analyze-dir", type=str, default="03_analyze")
    args = parser.parse_args()

    paths = build_analyze_paths(
        project_root=args.project_root,
        process_dir="outputs/02_process",
        analyze_dir=args.analyze_dir,
    )
    ensure_output_dirs(paths)

    tables_dir = paths.outputs_tables_dir
    charts_dir = paths.outputs_charts_dir
    logs_dir = paths.outputs_logs_dir

    rolling_full = load_table(tables_dir / "rolling_12m_returns_detail_full_history.csv")
    rolling_common = load_table(tables_dir / "rolling_12m_returns_detail_common_window.csv")
    threshold_full = load_table(tables_dir / "threshold_exceedance_full_history.csv")
    vol_full = load_table(tables_dir / "volatility_drawdown_full_history.csv")
    drawdown_full = load_table(tables_dir / "cumulative_growth_detail_full_history.csv")

    require_columns(rolling_full, ["ticker", "month_end", "rolling_12m_return"], "rolling_full")
    require_columns(rolling_common, ["ticker", "month_end", "rolling_12m_return"], "rolling_common")
    require_columns(threshold_full, ["ticker", "exceedance_rate"], "threshold_full")
    require_columns(vol_full, ["ticker", "annualized_volatility", "max_drawdown"], "vol_full")
    require_columns(drawdown_full, ["ticker", "month_end", "growth_index"], "drawdown_full")

    rolling_full["month_end"] = pd.to_datetime(rolling_full["month_end"])
    rolling_common["month_end"] = pd.to_datetime(rolling_common["month_end"])
    drawdown_full["month_end"] = pd.to_datetime(drawdown_full["month_end"])

    save_line_chart(
        rolling_full.dropna(subset=["rolling_12m_return"]),
        x_col="month_end",
        y_col="rolling_12m_return",
        group_col="ticker",
        title="Rolling 12-Month Return — Full History",
        out_path=charts_dir / "rolling_12m_return_full_history.png",
    )

    save_line_chart(
        rolling_common.dropna(subset=["rolling_12m_return"]),
        x_col="month_end",
        y_col="rolling_12m_return",
        group_col="ticker",
        title="Rolling 12-Month Return — Common Window",
        out_path=charts_dir / "rolling_12m_return_common_window.png",
    )

    save_bar_chart(
        threshold_full,
        x_col="ticker",
        y_col="exceedance_rate",
        title="Threshold Exceedance Rate — Full History",
        out_path=charts_dir / "threshold_exceedance_comparison.png",
    )

    save_bar_chart(
        vol_full,
        x_col="ticker",
        y_col="annualized_volatility",
        title="Annualized Volatility — Full History",
        out_path=charts_dir / "annualized_volatility_comparison.png",
    )

    save_bar_chart(
        vol_full,
        x_col="ticker",
        y_col="max_drawdown",
        title="Maximum Drawdown — Full History",
        out_path=charts_dir / "max_drawdown_comparison.png",
        ascending=True,
    )

    save_line_chart(
        drawdown_full,
        x_col="month_end",
        y_col="growth_index",
        group_col="ticker",
        title="Cumulative Growth Comparison — Full History",
        out_path=charts_dir / "cumulative_growth_comparison.png",
    )

    log_text = "\n".join(
        [
            "analyze_generate_charts.py completed successfully",
            "charts_created=6",
            f"charts_dir={charts_dir}",
        ]
    )
    write_text(log_text, logs_dir / "analyze_generate_charts.log")


if __name__ == "__main__":
    main()