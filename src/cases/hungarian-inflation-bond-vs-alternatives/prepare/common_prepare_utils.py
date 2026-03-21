from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any

import pandas as pd


RAW_FILES = {
    "etf_prices_daily": "etf_prices_daily.csv",
    "hungary_cpi_yoy": "hungary_cpi_yoy.csv",
    "hungary_10y_yield": "hungary_10y_yield.csv",
    "bond_reference_template": "bond_reference_template.csv",
}

META_SUFFIX = ".meta.json"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def load_meta_if_exists(path: Path) -> dict[str, Any]:
    meta_path = path.with_suffix(path.suffix + META_SUFFIX)
    if meta_path.exists():
        with meta_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def parse_dates_by_name(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col.lower() in {"date", "datetime", "timestamp"}:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    return out


def infer_nullable(series: pd.Series) -> bool:
    return bool(series.isna().any())


def safe_min(series: pd.Series) -> Any:
    non_null = series.dropna()
    return None if non_null.empty else non_null.min()


def safe_max(series: pd.Series) -> Any:
    non_null = series.dropna()
    return None if non_null.empty else non_null.max()


def normalize_scalar(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            return str(value)
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    if isinstance(value, (int, float, str, bool)) or value is None:
        return value
    return str(value)


def schema_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for col in df.columns:
        series = df[col]
        records.append(
            {
                "column": col,
                "observed_dtype": str(series.dtype),
                "non_null_count": int(series.notna().sum()),
                "null_count": int(series.isna().sum()),
                "null_pct": round(float(series.isna().mean() * 100), 4),
                "n_unique": int(series.nunique(dropna=True)),
                "sample_min": normalize_scalar(safe_min(series)),
                "sample_max": normalize_scalar(safe_max(series)),
            }
        )
    return records


def dataset_overview(df: pd.DataFrame, file_path: Path) -> dict[str, Any]:
    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "sha256": sha256_file(file_path),
        "row_count": int(len(df)),
        "column_count": int(df.shape[1]),
        "columns": list(df.columns),
        "duplicate_full_rows": int(df.duplicated().sum()),
    }


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def write_csv(path: Path, df: pd.DataFrame) -> None:
    ensure_dir(path.parent)
    df.to_csv(path, index=False)


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")