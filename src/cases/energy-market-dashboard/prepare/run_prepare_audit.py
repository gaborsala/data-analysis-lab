#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "adj_close", "volume"]


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize incoming column names to lowercase snake_case.
    """
    rename_map = {}
    for col in df.columns:
        normalized = col.strip().lower().replace(" ", "_")
        if normalized == "adjclose":
            normalized = "adj_close"
        rename_map[col] = normalized
    return df.rename(columns=rename_map)


def infer_ticker_from_filename(path: Path) -> str:
    """
    Infer ticker label from file name convention like:
    wti_raw.csv, brent_raw.csv, xle_raw.csv, spy_raw.csv
    """
    stem = path.stem.lower()
    ticker_map = {
        "wti_raw": "CL=F",
        "brent_raw": "BZ=F",
        "natgas_raw": "NG=F",
        "xle_raw": "XLE",
        "spy_raw": "SPY",
    }
    return ticker_map.get(stem, stem.replace("_raw", "").upper())


def ensure_ticker_column(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    if "ticker" not in df.columns:
        df = df.copy()
        df["ticker"] = ticker
    return df


def read_raw_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = standardize_columns(df)
    inferred_ticker = infer_ticker_from_filename(path)
    df = ensure_ticker_column(df, inferred_ticker)
    return df


def count_duplicates(df: pd.DataFrame) -> int:
    if not {"date", "ticker"}.issubset(df.columns):
        return -1
    return int(df.duplicated(subset=["date", "ticker"]).sum())


def schema_ok(df: pd.DataFrame) -> bool:
    needed = set(REQUIRED_COLUMNS + ["ticker"])
    return needed.issubset(df.columns)


def build_audit_row(path: Path) -> dict:
    df = read_raw_csv(path)

    # Preserve original values for audit
    row_count = len(df)

    # Date coercion just for measurement, not persistent modification
    date_series = pd.to_datetime(df["date"], errors="coerce") if "date" in df.columns else pd.Series(dtype="datetime64[ns]")

    audit = {
        "source_file": path.name,
        "ticker": df["ticker"].iloc[0] if "ticker" in df.columns and not df.empty else "",
        "row_count": int(row_count),
        "min_date": date_series.min(),
        "max_date": date_series.max(),
        "null_date": int(date_series.isna().sum()) if len(date_series) else -1,
        "null_open": int(df["open"].isna().sum()) if "open" in df.columns else -1,
        "null_high": int(df["high"].isna().sum()) if "high" in df.columns else -1,
        "null_low": int(df["low"].isna().sum()) if "low" in df.columns else -1,
        "null_close": int(df["close"].isna().sum()) if "close" in df.columns else -1,
        "null_adj_close": int(df["adj_close"].isna().sum()) if "adj_close" in df.columns else -1,
        "null_volume": int(df["volume"].isna().sum()) if "volume" in df.columns else -1,
        "duplicate_date_ticker": count_duplicates(df),
        "schema_ok": "Yes" if schema_ok(df) else "No",
        "notes": "",
    }

    if audit["schema_ok"] == "No":
        audit["notes"] = "Missing one or more required columns after standardization."

    return audit


def discover_input_files(raw_dir: Path) -> list[Path]:
    files = sorted(raw_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")
    return files


def build_prepare_audit(raw_dir: Path) -> pd.DataFrame:
    files = discover_input_files(raw_dir)
    rows = [build_audit_row(path) for path in files]
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build prepare audit for energy market dashboard raw files.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing raw CSV files.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("cases\energy-market-dashboard/outputs/prepare_audit.csv"),
        help="Output CSV path for prepare audit.",
    )
    args = parser.parse_args()

    audit_df = build_prepare_audit(args.raw_dir)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    audit_df.to_csv(args.out, index=False)

    print(f"Prepare audit written to: {args.out}")
    print(audit_df.to_string(index=False))


if __name__ == "__main__":
    main()