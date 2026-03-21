from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw/all_sectors.csv")
CLEAN_PATH = Path("data/processed/all_sectors_clean.csv")
METRICS_PATH = Path("data/processed/process_metrics.json")

SCRIPT_PATH = "src/cases/spdr_sector_etfs/process/process_spdr_dataset.py"


def count_missing(df: pd.DataFrame) -> int:
    return int(df.isna().sum().sum())


def validate_expected_columns(df: pd.DataFrame, expected_columns: list[str]) -> list[str]:
    missing = [col for col in expected_columns if col not in df.columns]
    return missing


def run_pipeline() -> dict:
    execution_time = datetime.now(UTC).isoformat()

    expected_columns = [
        "ticker",
        "sector",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    df_raw = pd.read_csv(RAW_PATH)

    raw_row_count = int(len(df_raw))
    raw_column_count = int(len(df_raw.columns))
    raw_missing_count = count_missing(df_raw)

    missing_columns = validate_expected_columns(df_raw, expected_columns)
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    # Keep a working copy
    df = df_raw.copy()

    # Type corrections
    df["date"] = pd.to_datetime(df["date"], errors="raise")

    numeric_columns = ["open", "high", "low", "close", "volume"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="raise")

    # Structural ordering
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)

    # Validation checks
    duplicate_key_count = int(df.duplicated(subset=["ticker", "date"]).sum())
    price_nonpositive_count = int((df[["open", "high", "low", "close"]] <= 0).sum().sum())
    volume_negative_count = int((df["volume"] < 0).sum())

    # OHLC integrity: low <= open/close <= high
    ohlc_invalid_count = int(
        (
            (df["low"] > df["open"]) |
            (df["low"] > df["close"]) |
            (df["high"] < df["open"]) |
            (df["high"] < df["close"]) |
            (df["low"] > df["high"])
        ).sum()
    )

    cleaned_row_count = int(len(df))
    cleaned_column_count = int(len(df.columns))
    cleaned_missing_count = count_missing(df)

    # Save outputs
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    metrics = {
        "topic": "spdr_sector_etfs",
        "execution_time_utc": execution_time,
        "script_path": SCRIPT_PATH,
        "raw_file_path": str(RAW_PATH),
        "clean_file_path": str(CLEAN_PATH),
        "raw_row_count": raw_row_count,
        "raw_column_count": raw_column_count,
        "raw_missing_count": raw_missing_count,
        "cleaned_row_count": cleaned_row_count,
        "cleaned_column_count": cleaned_column_count,
        "cleaned_missing_count": cleaned_missing_count,
        "rows_removed": raw_row_count - cleaned_row_count,
        "columns_removed": raw_column_count - cleaned_column_count,
        "duplicate_key_count": duplicate_key_count,
        "price_nonpositive_count": price_nonpositive_count,
        "volume_negative_count": volume_negative_count,
        "ohlc_invalid_count": ohlc_invalid_count,
        "date_parse_failures": 0,
        "deterministic_pipeline": True,
        "manual_steps": "None",
        "transformations": [
            {
                "step": 1,
                "change": "Convert date column from object to datetime",
                "rationale": "Required for chronological and time-series operations",
                "method": "pd.to_datetime(df['date'], errors='raise')",
                "validation_result": "No parse failures"
            },
            {
                "step": 2,
                "change": "Convert open/high/low/close/volume to numeric",
                "rationale": "Required for statistical and structural validation",
                "method": "pd.to_numeric(..., errors='raise')",
                "validation_result": "Successful conversion"
            },
            {
                "step": 3,
                "change": "Sort by ticker and date",
                "rationale": "Ensures deterministic ordering for downstream analysis",
                "method": "sort_values(['ticker', 'date'])",
                "validation_result": "Ordering applied successfully"
            }
        ],
        "remaining_issues": [
            {
                "issue": "Unequal ETF inception dates",
                "impact": "Unequal historical coverage across sectors",
                "risk_level": "Moderate",
                "mitigation": "Use common-window robustness checks in ANALYZE"
            },
            {
                "issue": "Non-trading days absent",
                "impact": "Expected gaps in calendar dates",
                "risk_level": "Low",
                "mitigation": "Treat as normal market-data structure"
            }
        ]
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    return metrics


if __name__ == "__main__":
    result = run_pipeline()
    print("PROCESS pipeline completed.")
    print(json.dumps(result, indent=2))