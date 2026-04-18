from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
import yfinance as yf

from config import (
    CANONICAL_TICKERS,
    DEFAULT_START_DATE,
    REQUIRED_COLUMNS,
    get_raw_data_dir,
)

@dataclass
class DownloadResult:
    ticker: str
    status: str
    row_count: int
    min_date: str
    max_date: str
    duplicate_date_count: int
    missing_required_columns: str
    output_file: str
    error_message: str
    downloaded_at_utc: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download raw daily OHLCV data for SPDR sector ETFs and SPY."
    )
    parser.add_argument(
        "--start-date",
        default=DEFAULT_START_DATE,
        help="Download start date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help="Optional exclusive end date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Optional override for raw output directory.",
    )
    return parser.parse_args()


def validate_price_frame(df: pd.DataFrame) -> List[str]:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing


def normalize_download_frame(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize yfinance output into a flat dataframe with expected columns.

    Handles both normal and occasional multi-index outputs.
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    df = df.reset_index()

    if "Datetime" in df.columns and "Date" not in df.columns:
        df = df.rename(columns={"Datetime": "Date"})

    if "Adj Close" not in df.columns and "Close" in df.columns:
        # Preserve schema compatibility even if provider returns a reduced shape.
        df["Adj Close"] = df["Close"]

    return df


def download_ticker(
    ticker: str,
    start_date: str,
    end_date: str | None,
    out_dir: Path,
) -> DownloadResult:
    from datetime import datetime, UTC
    now_utc = datetime.now(UTC).replace(microsecond=0).isoformat()

    try:
        df = yf.download(
            tickers=ticker,
            start=start_date,
            end=end_date,
            auto_adjust=False,
            progress=False,
            threads=False,
        )

        if df is None or df.empty:
            return DownloadResult(
                ticker=ticker,
                status="failed_empty",
                row_count=0,
                min_date="",
                max_date="",
                duplicate_date_count=0,
                missing_required_columns="",
                output_file="",
                error_message="No data returned by provider.",
                downloaded_at_utc=now_utc,
            )

        df = normalize_download_frame(df)

        missing_required = validate_price_frame(df)

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")

        duplicate_date_count = 0
        min_date = ""
        max_date = ""

        if "Date" in df.columns:
            duplicate_date_count = int(df["Date"].duplicated().sum())
            non_null_dates = df["Date"].dropna()
            if not non_null_dates.empty:
                min_date = str(non_null_dates.min())
                max_date = str(non_null_dates.max())

        output_path = out_dir / f"{ticker}.csv"
        df.to_csv(output_path, index=False)

        status = "success" if not missing_required else "success_with_schema_warning"

        return DownloadResult(
            ticker=ticker,
            status=status,
            row_count=int(len(df)),
            min_date=min_date,
            max_date=max_date,
            duplicate_date_count=duplicate_date_count,
            missing_required_columns="|".join(missing_required),
            output_file=str(output_path),
            error_message="",
            downloaded_at_utc=now_utc,
        )

    except Exception as exc:
        return DownloadResult(
            ticker=ticker,
            status="failed_exception",
            row_count=0,
            min_date="",
            max_date="",
            duplicate_date_count=0,
            missing_required_columns="",
            output_file="",
            error_message=str(exc),
            downloaded_at_utc=now_utc,
        )


def build_manifest(results: list[DownloadResult], out_dir: Path) -> Path:
    manifest_df = pd.DataFrame([asdict(result) for result in results])
    manifest_path = out_dir / "raw_download_manifest.csv"
    manifest_df.to_csv(manifest_path, index=False)
    return manifest_path


def main() -> None:
    args = parse_args()

    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_raw_data_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    results: list[DownloadResult] = []

    for ticker in CANONICAL_TICKERS:
        result = download_ticker(
            ticker=ticker,
            start_date=args.start_date,
            end_date=args.end_date,
            out_dir=out_dir,
        )
        results.append(result)
        print(
            f"[{result.status}] {result.ticker} "
            f"rows={result.row_count} "
            f"range={result.min_date}..{result.max_date}"
        )

    manifest_path = build_manifest(results, out_dir)

    success_count = sum(result.status.startswith("success") for result in results)
    fail_count = len(results) - success_count

    print("\nDownload summary")
    print(f"- Output directory: {out_dir}")
    print(f"- Manifest: {manifest_path}")
    print(f"- Successful tickers: {success_count}")
    print(f"- Failed tickers: {fail_count}")

    if fail_count > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()