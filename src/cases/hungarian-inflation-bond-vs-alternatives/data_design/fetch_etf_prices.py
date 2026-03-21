from __future__ import annotations

import argparse
import yfinance as yf
import pandas as pd
from common_io import save_csv_with_metadata


tickers = [
    "XLC", "XLY", "XLE", "XLF", "XLV",
    "XLI", "XLB", "XLRE", "XLK", "XLU", "SPY"
]


def parse_args():
    parser = argparse.ArgumentParser(description="Download ETF prices.")
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Single output directory for saved files."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Downloading ETF prices...")

    data = yf.download(tickers, start="2010-01-01")
    df = data["Close"]
    df = df.reset_index()
    df = df.melt(id_vars="Date", var_name="ticker", value_name="close")

    saved_path = save_csv_with_metadata(
        df=df,
        output_dir=args.output_dir,
        filename="etf_prices_daily.csv"
    )

    print(f"ETF dataset saved -> {saved_path}")


if __name__ == "__main__":
    main()