from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import CANONICAL_TICKERS, get_repo_root


BENCHMARK_TICKER = "SPY"
DATE_COLUMN = "Date"
PRICE_COLUMN = "Adj Close"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a historical long-format ratio panel for sector ETFs relative to SPY."
    )
    parser.add_argument(
        "--raw-dir",
        default=None,
        help="Optional override for raw input directory. Defaults to repo_root/data/raw",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Optional override for processed output directory. "
             "Defaults to cases/market-structure-consistency/outputs/02_process",
    )
    parser.add_argument(
        "--output-file",
        default="historical_ratio_panel.csv",
        help="Output CSV filename.",
    )
    return parser.parse_args()


def get_default_raw_dir() -> Path:
    return get_repo_root() / "data" / "raw"


def get_default_out_dir() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "02_process"
    )


def validate_input_file(path: Path, ticker: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing raw file for {ticker}: {path}")


def load_one_ticker(path: Path, ticker: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    required = {DATE_COLUMN, PRICE_COLUMN}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"{ticker} is missing required columns: {sorted(missing)}"
        )

    out = df[[DATE_COLUMN, PRICE_COLUMN]].copy()
    out[DATE_COLUMN] = pd.to_datetime(out[DATE_COLUMN], errors="coerce")

    invalid_dates = int(out[DATE_COLUMN].isna().sum())
    if invalid_dates > 0:
        raise ValueError(f"{ticker} contains {invalid_dates} invalid dates.")

    duplicate_dates = int(out[DATE_COLUMN].duplicated().sum())
    if duplicate_dates > 0:
        raise ValueError(f"{ticker} contains {duplicate_dates} duplicate dates.")

    out[PRICE_COLUMN] = pd.to_numeric(out[PRICE_COLUMN], errors="coerce")
    invalid_prices = int(out[PRICE_COLUMN].isna().sum())
    if invalid_prices > 0:
        raise ValueError(f"{ticker} contains {invalid_prices} invalid adjusted close values.")

    non_positive_prices = int((out[PRICE_COLUMN] <= 0).sum())
    if non_positive_prices > 0:
        raise ValueError(f"{ticker} contains {non_positive_prices} non-positive adjusted close values.")

    out = out.rename(columns={PRICE_COLUMN: ticker})
    out = out.sort_values(DATE_COLUMN).reset_index(drop=True)
    return out


def build_wide_price_panel(raw_dir: Path) -> pd.DataFrame:
    wide_df: pd.DataFrame | None = None

    for ticker in CANONICAL_TICKERS:
        path = raw_dir / f"{ticker}.csv"
        validate_input_file(path, ticker)
        ticker_df = load_one_ticker(path, ticker)

        if wide_df is None:
            wide_df = ticker_df
        else:
            wide_df = wide_df.merge(
                ticker_df,
                on=DATE_COLUMN,
                how="outer",
                validate="one_to_one",
            )

    if wide_df is None:
        raise RuntimeError("No ticker files were loaded.")

    wide_df = wide_df.sort_values(DATE_COLUMN).reset_index(drop=True)
    return wide_df


def build_long_ratio_panel(wide_df: pd.DataFrame) -> pd.DataFrame:
    if BENCHMARK_TICKER not in wide_df.columns:
        raise ValueError(f"Benchmark ticker {BENCHMARK_TICKER} not found in wide panel.")

    ticker_columns = [ticker for ticker in CANONICAL_TICKERS if ticker != BENCHMARK_TICKER]

    long_df = wide_df.melt(
        id_vars=[DATE_COLUMN, BENCHMARK_TICKER],
        value_vars=ticker_columns,
        var_name="ticker",
        value_name="adj_close",
    )

    long_df = long_df.rename(
        columns={
            DATE_COLUMN: "date",
            BENCHMARK_TICKER: "spy_adj_close",
        }
    )

    long_df["ratio_value"] = long_df["adj_close"] / long_df["spy_adj_close"]

    long_df["date"] = pd.to_datetime(long_df["date"], errors="coerce")
    long_df = long_df.sort_values(["ticker", "date"]).reset_index(drop=True)

    return long_df[
        [
            "date",
            "ticker",
            "adj_close",
            "spy_adj_close",
            "ratio_value",
        ]
    ]

def build_coverage_summary(long_df: pd.DataFrame) -> pd.DataFrame:
    coverage_rows: list[dict] = []

    for ticker, grp in long_df.groupby("ticker", dropna=False):
        grp = grp.copy()

        non_null_adj = grp.loc[grp["adj_close"].notna()].copy()
        non_null_ratio = grp.loc[grp["ratio_value"].notna()].copy()

        min_date = ""
        max_date = ""

        if not non_null_adj.empty:
            min_date = pd.to_datetime(non_null_adj["date"].min(), errors="coerce").strftime("%Y-%m-%d")
            max_date = pd.to_datetime(non_null_adj["date"].max(), errors="coerce").strftime("%Y-%m-%d")

        coverage_rows.append(
            {
                "ticker": ticker,
                "row_count": int(len(grp)),
                "non_null_adj_close": int(grp["adj_close"].notna().sum()),
                "non_null_spy_adj_close": int(grp["spy_adj_close"].notna().sum()),
                "non_null_ratio_value": int(grp["ratio_value"].notna().sum()),
                "min_date": min_date,
                "max_date": max_date,
            }
        )

    summary = pd.DataFrame(coverage_rows).sort_values("ticker").reset_index(drop=True)
    return summary

def main() -> None:
    args = parse_args()

    raw_dir = Path(args.raw_dir).resolve() if args.raw_dir else get_default_raw_dir().resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_default_out_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Raw input directory: {raw_dir}")
    print(f"Processed output directory: {out_dir}")

    wide_df = build_wide_price_panel(raw_dir=raw_dir)

    wide_out_path = out_dir / "historical_adjusted_close_wide.csv"
    wide_df.to_csv(wide_out_path, index=False)

    long_df = build_long_ratio_panel(wide_df=wide_df)

    output_path = out_dir / args.output_file
    long_df.to_csv(output_path, index=False)

    coverage_df = build_coverage_summary(long_df=long_df)
    coverage_out_path = out_dir / "historical_ratio_panel_coverage.csv"
    coverage_df.to_csv(coverage_out_path, index=False)

    print("\nBuild complete")
    print(f"- Wide adjusted-close panel: {wide_out_path}")
    print(f"- Long ratio panel: {output_path}")
    print(f"- Coverage summary: {coverage_out_path}")
    print(f"- Wide panel rows: {len(wide_df)}")
    print(f"- Long panel rows: {len(long_df)}")
    print(f"- Tickers in long panel: {long_df['ticker'].nunique()}")

    null_ratio_count = int(long_df["ratio_value"].isna().sum())
    print(f"- Null ratio_value count: {null_ratio_count}")

    if null_ratio_count > 0:
        print(
            "Note: null ratio values are expected where a sector did not yet exist on a given date "
            "or if benchmark alignment is unavailable."
        )


if __name__ == "__main__":
    main()