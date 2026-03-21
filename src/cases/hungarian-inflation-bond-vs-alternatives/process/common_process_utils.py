from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd


RAW_FILES = {
    "etf_prices_daily": "etf_prices_daily.csv",
    "hungary_cpi_yoy": "hungary_cpi_yoy.csv",
    "hungary_10y_yield": "hungary_10y_yield.csv",
    "bond_reference_template": "bond_reference_template.csv",
}


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_csv(path: Path, df: pd.DataFrame) -> None:
    ensure_dir(path.parent)
    df.to_csv(path, index=False)


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def parse_dates_by_name(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col.lower() in {"date", "datetime", "timestamp"}:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    return out


def validate_no_parse_failures(df_raw: pd.DataFrame, df_parsed: pd.DataFrame) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for col in df_raw.columns:
        if col.lower() in {"date", "datetime", "timestamp"}:
            raw_non_null = int(df_raw[col].notna().sum())
            parsed_non_null = int(df_parsed[col].notna().sum())
            parse_failures = raw_non_null - parsed_non_null
            issues.append(
                {
                    "column": col,
                    "raw_non_null": raw_non_null,
                    "parsed_non_null": parsed_non_null,
                    "parse_failures": parse_failures,
                }
            )
    return issues


def raw_snapshot_summary(raw_dir: Path) -> pd.DataFrame:
    rows = []
    for dataset_name, filename in RAW_FILES.items():
        path = raw_dir / filename
        df = load_csv(path)
        rows.append(
            {
                "dataset_name": dataset_name,
                "file_name": filename,
                "row_count_raw": int(len(df)),
                "column_count_raw": int(df.shape[1]),
                "sha256": sha256_file(path),
            }
        )
    return pd.DataFrame(rows)


def add_year_month_period(df: pd.DataFrame, date_col: str, new_col: str = "year_month") -> pd.DataFrame:
    out = df.copy()
    out[new_col] = pd.to_datetime(out[date_col]).dt.to_period("M").astype(str)
    return out


def pct_string_to_points(value: Any) -> float | None:
    if pd.isna(value):
        return None
    s = str(value).strip().replace("%", "")
    if s == "":
        return None
    return float(s)