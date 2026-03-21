from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from prepare_schema_checks import infer_schema, run_integrity_checks


DEFAULT_OUTPUT_JSON = "prepare_audit_summary.json"


def discover_csvs(root: Path) -> List[Path]:
    return sorted([p for p in root.rglob("*.csv") if p.is_file()])



def read_dataset(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)



def summarize_files(csv_paths: List[Path], root: Path) -> List[Dict[str, Any]]:
    rows = []
    for p in csv_paths:
        rel = p.relative_to(root)
        df = pd.read_csv(p, nrows=5)
        rows.append(
            {
                "relative_path": str(rel).replace("\\", "/"),
                "column_count": len(df.columns),
                "columns": list(df.columns),
            }
        )
    return rows



def build_summary(dataset_path: Path, extracted_root: Path | None = None) -> Dict[str, Any]:
    if dataset_path.suffix.lower() == ".zip":
        if extracted_root is None:
            extracted_root = dataset_path.with_suffix("")
        extracted_root.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(dataset_path) as zf:
            zf.extractall(extracted_root)
        root = extracted_root
        csv_paths = discover_csvs(root)
        combined = next((p for p in csv_paths if p.name == "all_sectors.csv"), None)
        if combined is None:
            raise FileNotFoundError("all_sectors.csv not found inside ZIP archive")
        df = read_dataset(combined)
        source_kind = "zip_archive"
        canonical_path = combined
    else:
        canonical_path = dataset_path
        df = read_dataset(canonical_path)
        source_kind = "csv_file"
        root = canonical_path.parent
        csv_paths = [canonical_path]

    parsed_dates = pd.to_datetime(df["date"], errors="coerce") if "date" in df.columns else pd.Series(dtype="datetime64[ns]")

    ticker_counts = (
        df.groupby("ticker").size().sort_values(ascending=False).to_dict()
        if "ticker" in df.columns
        else {}
    )
    sector_by_ticker = (
        df.groupby("ticker")["sector"].nunique().to_dict()
        if {"ticker", "sector"}.issubset(df.columns)
        else {}
    )

    summary: Dict[str, Any] = {
        "source_kind": source_kind,
        "source_path": str(dataset_path),
        "canonical_dataset": str(canonical_path),
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "columns": list(df.columns),
        "min_date": None if parsed_dates.empty else str(parsed_dates.min()),
        "max_date": None if parsed_dates.empty else str(parsed_dates.max()),
        "unique_tickers": int(df["ticker"].nunique()) if "ticker" in df.columns else None,
        "unique_sectors": int(df["sector"].nunique()) if "sector" in df.columns else None,
        "schema": infer_schema(df),
        "integrity_checks": [vars(x) for x in run_integrity_checks(df)],
        "file_inventory": summarize_files(csv_paths, root),
        "ticker_row_counts": ticker_counts,
        "ticker_to_sector_nunique": sector_by_ticker,
        "missing_by_column": {col: int(df[col].isna().sum()) for col in df.columns},
    }

    if "volume" in df.columns:
        summary["zero_volume_rows"] = int((pd.to_numeric(df["volume"], errors="coerce") == 0).sum())

    if {"ticker", "date"}.issubset(df.columns):
        per_ticker_dates = (
            df.assign(date_parsed=parsed_dates)
            .groupby("ticker")["date_parsed"]
            .agg(["min", "max", "count"]) 
            .reset_index()
        )
        summary["ticker_date_coverage"] = per_ticker_dates.to_dict(orient="records")

    return summary



def main() -> None:
    parser = argparse.ArgumentParser(description="Run PREPARE-phase structural audit on a dataset or ZIP archive.")
    parser.add_argument("input_path", help="Path to ZIP archive or canonical CSV file")
    parser.add_argument("--extract-dir", default=None, help="Where to extract ZIP contents if input is a ZIP")
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON, help="Path for JSON summary output")
    args = parser.parse_args()

    input_path = Path(args.input_path).expanduser().resolve()
    extract_dir = Path(args.extract_dir).expanduser().resolve() if args.extract_dir else None
    output_json = Path(args.output_json).expanduser().resolve()

    summary = build_summary(input_path, extract_dir)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"Saved audit summary: {output_json}")


if __name__ == "__main__":
    main()
