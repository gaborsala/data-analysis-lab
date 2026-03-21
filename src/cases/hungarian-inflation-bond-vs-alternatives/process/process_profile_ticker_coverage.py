from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_process_utils import load_csv, parse_dates_by_name, write_csv, write_json


def build_ticker_coverage(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work = work.sort_values(["ticker", "Date"]).reset_index(drop=True)

    rows = []
    for ticker, g in work.groupby("ticker", dropna=False):
        non_null = g[g["close"].notna()].copy()

        first_date_all = g["Date"].min()
        last_date_all = g["Date"].max()

        first_valid_date = non_null["Date"].min() if not non_null.empty else pd.NaT
        last_valid_date = non_null["Date"].max() if not non_null.empty else pd.NaT

        rows.append(
            {
                "ticker": ticker,
                "row_count": int(len(g)),
                "first_date_all": first_date_all,
                "last_date_all": last_date_all,
                "first_valid_close_date": first_valid_date,
                "last_valid_close_date": last_valid_date,
                "non_null_close_count": int(g["close"].notna().sum()),
                "null_close_count": int(g["close"].isna().sum()),
                "min_close": float(non_null["close"].min()) if not non_null.empty else None,
                "max_close": float(non_null["close"].max()) if not non_null.empty else None,
            }
        )

    out = pd.DataFrame(rows).sort_values("ticker").reset_index(drop=True)
    return out


def run(raw_dir: Path, out_dir: Path) -> None:
    df = load_csv(raw_dir / "etf_prices_daily.csv")
    df = parse_dates_by_name(df)

    coverage = build_ticker_coverage(df)
    write_csv(out_dir / "etf_ticker_coverage_profile.csv", coverage)

    summary = {
        "ticker_count": int(coverage["ticker"].nunique()),
        "total_rows": int(len(df)),
        "total_non_null_close": int(df["close"].notna().sum()),
        "total_null_close": int(df["close"].isna().sum()),
    }
    write_json(out_dir / "etf_ticker_coverage_profile_summary.json", summary)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Profile ETF ticker coverage before cleaning.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    run(Path(args.raw_dir), Path(args.out_dir))