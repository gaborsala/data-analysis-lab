from __future__ import annotations

from pathlib import Path
import pandas as pd


EXPECTED_FILES = {
    "wti_raw.csv": "CL=F",
    "brent_raw.csv": "BZ=F",
    "natgas_raw.csv": "NG=F",
    "xle_raw.csv": "XLE",
    "spy_raw.csv": "SPY",
}

EXPECTED_COLUMNS = [
    "date",
    "adj_close",
    "close",
    "high",
    "low",
    "open",
    "volume",
    "ticker",
]


def load_raw_file(path: Path, expected_ticker: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"{path.name}: missing columns {sorted(missing_cols)}")

    extra_cols = set(df.columns) - set(EXPECTED_COLUMNS)
    if extra_cols:
        raise ValueError(f"{path.name}: unexpected columns {sorted(extra_cols)}")

    df = df[EXPECTED_COLUMNS].copy()

    if df.empty:
        raise ValueError(f"{path.name}: file is empty")

    observed_tickers = set(df["ticker"].dropna().astype(str).unique())
    if observed_tickers != {expected_ticker}:
        raise ValueError(
            f"{path.name}: expected ticker {expected_ticker}, found {sorted(observed_tickers)}"
        )

    df["date"] = pd.to_datetime(df["date"], errors="raise")

    dup_count = int(df.duplicated(subset=["date", "ticker"]).sum())
    if dup_count > 0:
        raise ValueError(f"{path.name}: found {dup_count} duplicate (date, ticker) rows")

    numeric_cols = ["adj_close", "close", "high", "low", "open", "volume"]
    for col in numeric_cols:
        if df[col].isna().any():
            raise ValueError(f"{path.name}: nulls detected in {col}")

    for col in ["adj_close", "close", "high", "low", "open", "volume"]:
        if (df[col] < 0).any():
            raise ValueError(f"{path.name}: negative values detected in {col}")

    bad_high_low = (df["high"] < df["low"]).sum()
    if bad_high_low > 0:
        raise ValueError(f"{path.name}: found {bad_high_low} rows where high < low")

    return df.sort_values(["date", "ticker"]).reset_index(drop=True)


def build_date_coverage(df: pd.DataFrame) -> pd.DataFrame:
    coverage = (
        df.groupby("date", as_index=False)
        .agg(ticker_count=("ticker", "nunique"))
        .sort_values("date")
        .reset_index(drop=True)
    )
    return coverage


def main() -> None:
    root = Path(__file__).resolve().parents[4]
    raw_dir = root / "data" / "raw"
    out_dir = root / "cases" / "energy-market-dashboard" / "outputs" / "process"
    out_dir.mkdir(parents=True, exist_ok=True)

    loaded = []
    audit_rows = []

    for filename, expected_ticker in EXPECTED_FILES.items():
        path = raw_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing raw file: {path}")

        df = load_raw_file(path, expected_ticker)
        loaded.append(df)

        audit_rows.append(
            {
                "file_name": filename,
                "ticker": expected_ticker,
                "rows": len(df),
                "cols": len(df.columns),
                "min_date": df["date"].min().date().isoformat(),
                "max_date": df["date"].max().date().isoformat(),
                "duplicate_date_ticker_rows": int(df.duplicated(subset=["date", "ticker"]).sum()),
                "missing_values_total": int(df.isna().sum().sum()),
            }
        )

    combined = (
        pd.concat(loaded, ignore_index=True)
        .sort_values(["date", "ticker"])
        .reset_index(drop=True)
    )

    combined_dups = int(combined.duplicated(subset=["date", "ticker"]).sum())
    if combined_dups > 0:
        raise ValueError(f"Combined dataset has {combined_dups} duplicate (date, ticker) rows")

    date_coverage = build_date_coverage(combined)
    expected_ticker_count = len(EXPECTED_FILES)
    common_dates = set(date_coverage.loc[date_coverage["ticker_count"] == expected_ticker_count, "date"])

    aligned = (
        combined[combined["date"].isin(common_dates)]
        .sort_values(["date", "ticker"])
        .reset_index(drop=True)
    )

    aligned_check = (
        aligned.groupby("date")["ticker"].nunique().reset_index(name="ticker_count")
    )
    if not (aligned_check["ticker_count"] == expected_ticker_count).all():
        raise ValueError("Aligned dataset contains dates without full ticker coverage")

    ticker_coverage_summary = (
        combined.groupby("ticker", as_index=False)
        .agg(
            rows=("ticker", "size"),
            min_date=("date", "min"),
            max_date=("date", "max"),
        )
        .sort_values("ticker")
        .reset_index(drop=True)
    )
    ticker_coverage_summary["min_date"] = ticker_coverage_summary["min_date"].dt.date.astype(str)
    ticker_coverage_summary["max_date"] = ticker_coverage_summary["max_date"].dt.date.astype(str)

    process_audit_summary = pd.DataFrame(
        [
            {
                "metric": "raw_row_count_total",
                "value": len(combined),
            },
            {
                "metric": "aligned_row_count_total",
                "value": len(aligned),
            },
            {
                "metric": "raw_column_count",
                "value": len(combined.columns),
            },
            {
                "metric": "aligned_column_count",
                "value": len(aligned.columns),
            },
            {
                "metric": "common_date_count",
                "value": len(common_dates),
            },
            {
                "metric": "expected_ticker_count",
                "value": expected_ticker_count,
            },
            {
                "metric": "aligned_start_date",
                "value": aligned["date"].min().date().isoformat(),
            },
            {
                "metric": "aligned_end_date",
                "value": aligned["date"].max().date().isoformat(),
            },
        ]
    )

    combined_to_save = combined.copy()
    aligned_to_save = aligned.copy()
    combined_to_save["date"] = combined_to_save["date"].dt.date.astype(str)
    aligned_to_save["date"] = aligned_to_save["date"].dt.date.astype(str)
    date_coverage_to_save = date_coverage.copy()
    date_coverage_to_save["date"] = date_coverage_to_save["date"].dt.date.astype(str)

    combined_to_save.to_csv(out_dir / "combined_panel.csv", index=False)
    aligned_to_save.to_csv(out_dir / "aligned_panel.csv", index=False)
    pd.DataFrame(audit_rows).to_csv(out_dir / "raw_file_audit.csv", index=False)
    date_coverage_to_save.to_csv(out_dir / "date_coverage.csv", index=False)
    ticker_coverage_summary.to_csv(out_dir / "ticker_coverage_summary.csv", index=False)
    process_audit_summary.to_csv(out_dir / "process_audit_summary.csv", index=False)

    print("Saved:")
    print(f"  {out_dir / 'combined_panel.csv'}")
    print(f"  {out_dir / 'aligned_panel.csv'}")
    print(f"  {out_dir / 'raw_file_audit.csv'}")
    print(f"  {out_dir / 'date_coverage.csv'}")
    print(f"  {out_dir / 'ticker_coverage_summary.csv'}")
    print(f"  {out_dir / 'process_audit_summary.csv'}")


if __name__ == "__main__":
    main()