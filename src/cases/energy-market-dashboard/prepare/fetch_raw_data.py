#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf


TICKERS = {
    "wti": "CL=F",
    "brent": "BZ=F",
    "natgas": "NG=F",
    "xle": "XLE",
    "spy": "SPY",
}


def _flatten_columns(columns) -> list[str]:
    flat = []
    for col in columns:
        if isinstance(col, tuple):
            flat.append(str(col[0]))
        else:
            flat.append(str(col))
    return flat


def fetch_single(ticker: str, period: str = "5y") -> pd.DataFrame:
    df = yf.download(
        ticker,
        period=period,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    df.columns = _flatten_columns(df.columns)

    df = df.reset_index()
    df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]

    if "adj_close" not in df.columns and "adjclose" in df.columns:
        df = df.rename(columns={"adjclose": "adj_close"})

    required_cols = {"date", "open", "high", "low", "close", "volume"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"{ticker}: missing expected columns: {sorted(missing)}")

    df["ticker"] = ticker

    return df


def save_raw(df: pd.DataFrame, name: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{name}_raw.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch raw market data")
    parser.add_argument("--out-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--period", type=str, default="5y")
    args = parser.parse_args()

    for name, ticker in TICKERS.items():
        print(f"Downloading {name} ({ticker})...")
        df = fetch_single(ticker, args.period)
        save_raw(df, name, args.out_dir)

    print("All raw data downloaded successfully.")


if __name__ == "__main__":
    main()