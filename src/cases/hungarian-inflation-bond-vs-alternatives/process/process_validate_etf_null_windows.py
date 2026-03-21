from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_process_utils import load_csv, parse_dates_by_name, write_csv, write_json


def classify_null_windows(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = df.copy().sort_values(["ticker", "Date"]).reset_index(drop=True)

    detailed_rows = []
    summary_rows = []

    for ticker, g in work.groupby("ticker", dropna=False):
        g = g.copy().reset_index(drop=True)
        non_null = g[g["close"].notna()].copy()

        if non_null.empty:
            first_valid = pd.NaT
            last_valid = pd.NaT
        else:
            first_valid = non_null["Date"].min()
            last_valid = non_null["Date"].max()

        nulls = g[g["close"].isna()].copy()

        pre_inception = 0
        post_coverage = 0
        internal_active = 0

        for _, row in nulls.iterrows():
            d = row["Date"]
            if pd.isna(first_valid) or pd.isna(last_valid):
                classification = "all_null_series"
            elif d < first_valid:
                classification = "pre_inception"
                pre_inception += 1
            elif d > last_valid:
                classification = "post_coverage"
                post_coverage += 1
            else:
                classification = "internal_active_window"
                internal_active += 1

            detailed_rows.append(
                {
                    "ticker": ticker,
                    "Date": d,
                    "classification": classification,
                    "first_valid_close_date": first_valid,
                    "last_valid_close_date": last_valid,
                }
            )

        summary_rows.append(
            {
                "ticker": ticker,
                "first_valid_close_date": first_valid,
                "last_valid_close_date": last_valid,
                "null_close_count": int(g["close"].isna().sum()),
                "pre_inception_null_count": pre_inception,
                "post_coverage_null_count": post_coverage,
                "internal_active_window_null_count": internal_active,
                "has_internal_active_nulls": bool(internal_active > 0),
            }
        )

    detailed = pd.DataFrame(detailed_rows).sort_values(["ticker", "Date"]).reset_index(drop=True)
    summary = pd.DataFrame(summary_rows).sort_values("ticker").reset_index(drop=True)
    return detailed, summary


def run(raw_dir: Path, out_dir: Path) -> None:
    df = load_csv(raw_dir / "etf_prices_daily.csv")
    df = parse_dates_by_name(df)

    detailed, summary = classify_null_windows(df)
    write_csv(out_dir / "etf_null_window_classification_detailed.csv", detailed)
    write_csv(out_dir / "etf_null_window_classification_summary.csv", summary)

    overall = {
        "tickers_with_internal_active_nulls": int(summary["has_internal_active_nulls"].sum()) if not summary.empty else 0,
        "total_pre_inception_nulls": int(summary["pre_inception_null_count"].sum()) if not summary.empty else 0,
        "total_post_coverage_nulls": int(summary["post_coverage_null_count"].sum()) if not summary.empty else 0,
        "total_internal_active_window_nulls": int(summary["internal_active_window_null_count"].sum()) if not summary.empty else 0,
    }
    write_json(out_dir / "etf_null_window_classification_overall.json", overall)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate whether ETF nulls occur outside or inside active windows.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    run(Path(args.raw_dir), Path(args.out_dir))