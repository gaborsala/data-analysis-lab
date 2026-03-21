from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import pandas as pd


@dataclass
class RuleResult:
    name: str
    value: Any
    status: str
    notes: str = ""


def infer_schema(df: pd.DataFrame) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for col in df.columns:
        series = df[col]
        observed_type = str(series.dtype)
        non_null = int(series.notna().sum())
        null_count = int(series.isna().sum())
        null_pct = float((null_count / len(df) * 100.0) if len(df) else 0.0)

        expected_type = observed_type
        if col.lower() == "date":
            expected_type = "datetime64[ns]"
        elif pd.api.types.is_integer_dtype(series):
            expected_type = "integer"
        elif pd.api.types.is_float_dtype(series):
            expected_type = "float"
        elif pd.api.types.is_object_dtype(series):
            expected_type = "string/category"

        rows.append(
            {
                "column": col,
                "observed_type": observed_type,
                "expected_type": expected_type,
                "non_null": non_null,
                "null_count": null_count,
                "null_pct": round(null_pct, 4),
                "example": None if series.dropna().empty else str(series.dropna().iloc[0]),
            }
        )
    return rows



def run_integrity_checks(df: pd.DataFrame) -> List[RuleResult]:
    checks: List[RuleResult] = []
    row_count = len(df)

    checks.append(RuleResult("row_count", row_count, "info"))
    checks.append(RuleResult("column_count", len(df.columns), "info"))

    if {"ticker", "date"}.issubset(df.columns):
        dup_keys = int(df.duplicated(subset=["ticker", "date"]).sum())
        checks.append(
            RuleResult(
                "duplicate_ticker_date_rows",
                dup_keys,
                "pass" if dup_keys == 0 else "warn",
                "Composite key candidate: ticker + date",
            )
        )

    if "date" in df.columns:
        parsed = pd.to_datetime(df["date"], errors="coerce")
        parse_failures = int(parsed.isna().sum())
        weekend_rows = int((parsed.dt.dayofweek >= 5).sum()) if parse_failures < len(df) else None
        checks.append(
            RuleResult(
                "date_parse_failures",
                parse_failures,
                "pass" if parse_failures == 0 else "warn",
            )
        )
        if weekend_rows is not None:
            checks.append(
                RuleResult(
                    "weekend_dated_rows",
                    weekend_rows,
                    "pass" if weekend_rows == 0 else "warn",
                )
            )

    numeric_cols = [c for c in ["open", "high", "low", "close", "volume"] if c in df.columns]
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors="coerce")
        negatives = int((series < 0).sum())
        zeros = int((series == 0).sum())
        checks.append(
            RuleResult(
                f"negative_{col}",
                negatives,
                "pass" if negatives == 0 else "warn",
            )
        )
        checks.append(
            RuleResult(
                f"zero_{col}",
                zeros,
                "info" if col == "volume" else ("pass" if zeros == 0 else "warn"),
            )
        )

    if {"open", "high", "low", "close"}.issubset(df.columns):
        open_s = pd.to_numeric(df["open"], errors="coerce")
        high_s = pd.to_numeric(df["high"], errors="coerce")
        low_s = pd.to_numeric(df["low"], errors="coerce")
        close_s = pd.to_numeric(df["close"], errors="coerce")

        checks.extend(
            [
                RuleResult("high_lt_open", int((high_s < open_s).sum()), "pass" if int((high_s < open_s).sum()) == 0 else "warn"),
                RuleResult("high_lt_close", int((high_s < close_s).sum()), "pass" if int((high_s < close_s).sum()) == 0 else "warn"),
                RuleResult("low_gt_open", int((low_s > open_s).sum()), "pass" if int((low_s > open_s).sum()) == 0 else "warn"),
                RuleResult("low_gt_close", int((low_s > close_s).sum()), "pass" if int((low_s > close_s).sum()) == 0 else "warn"),
                RuleResult("high_lt_low", int((high_s < low_s).sum()), "pass" if int((high_s < low_s).sum()) == 0 else "warn"),
            ]
        )

    return checks
