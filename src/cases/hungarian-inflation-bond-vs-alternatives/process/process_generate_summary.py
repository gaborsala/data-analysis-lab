from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_process_utils import raw_snapshot_summary, write_text


def read_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def df_to_text(df: pd.DataFrame, title: str) -> list[str]:
    lines = [f"## {title}", ""]
    if df.empty:
        lines.append("_No data available._")
        lines.append("")
        return lines
    lines.append(df.to_string(index=False))
    lines.append("")
    return lines


def run(raw_dir: Path, out_dir: Path) -> None:
    snapshot = raw_snapshot_summary(raw_dir)
    coverage = read_csv_if_exists(out_dir / "etf_ticker_coverage_profile.csv")
    null_summary = read_csv_if_exists(out_dir / "etf_null_window_classification_summary.csv")
    merged_summary = read_csv_if_exists(out_dir / "monthly_merged_context.csv").head(20)

    lines: list[str] = []
    lines.append("# PROCESS Output Summary")
    lines.append("")
    lines.append("Machine-generated summary of PROCESS outputs.")
    lines.append("")

    lines.extend(df_to_text(snapshot, "1. Raw Snapshot"))
    lines.extend(df_to_text(coverage, "2. ETF Ticker Coverage"))
    lines.extend(df_to_text(null_summary, "3. ETF Null Window Classification"))
    lines.extend(df_to_text(merged_summary, "4. Monthly Merged Context Sample"))

    lines.append("## 5. Cleaning Rules Applied")
    lines.append("")
    lines.append("- ETF rows with null close outside active valid window are removed.")
    lines.append("- Internal active-window nulls are preserved for audit visibility and counted in summaries.")
    lines.append("- Bond percent strings are normalized into numeric percentage-point columns.")
    lines.append("- ETF daily prices are resampled to month-end last valid close by ticker.")
    lines.append("- CPI and 10Y yield are aligned by `year_month`.")
    lines.append("")

    write_text(out_dir / "process_output_summary.md", "\n".join(lines))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate PROCESS summary file.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    run(Path(args.raw_dir), Path(args.out_dir))