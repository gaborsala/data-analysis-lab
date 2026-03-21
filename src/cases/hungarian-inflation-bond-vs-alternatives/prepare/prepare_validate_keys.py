from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_prepare_utils import RAW_FILES, load_csv, parse_dates_by_name, write_csv, write_json


KEY_RULES = {
    "etf_prices_daily": ["Date", "ticker"],
    "hungary_cpi_yoy": ["date"],
    "hungary_10y_yield": ["date"],
    "bond_reference_template": ["bond_id"],
}


def validate_key(df: pd.DataFrame, key_cols: list[str]) -> dict:
    missing_cols = [c for c in key_cols if c not in df.columns]
    if missing_cols:
        return {
            "key_columns": key_cols,
            "missing_key_columns": missing_cols,
            "key_duplicate_count": None,
            "null_in_key_count": None,
            "unique_key_count": None,
            "valid": False,
        }

    key_df = df[key_cols]
    null_in_key_count = int(key_df.isna().any(axis=1).sum())
    key_duplicate_count = int(key_df.duplicated().sum())
    unique_key_count = int(len(key_df.drop_duplicates()))

    valid = (null_in_key_count == 0) and (key_duplicate_count == 0)

    return {
        "key_columns": key_cols,
        "missing_key_columns": [],
        "key_duplicate_count": key_duplicate_count,
        "null_in_key_count": null_in_key_count,
        "unique_key_count": unique_key_count,
        "valid": valid,
    }


def duplicate_extract(df: pd.DataFrame, key_cols: list[str]) -> pd.DataFrame:
    if any(c not in df.columns for c in key_cols):
        return pd.DataFrame()
    dup_mask = df.duplicated(subset=key_cols, keep=False)
    out = df.loc[dup_mask].copy()
    if not out.empty:
        out = out.sort_values(key_cols).reset_index(drop=True)
    return out


def run(raw_dir: Path, out_dir: Path) -> None:
    validation_rows = []

    for dataset_name, filename in RAW_FILES.items():
        path = raw_dir / filename
        df = parse_dates_by_name(load_csv(path))
        key_cols = KEY_RULES[dataset_name]

        result = validate_key(df, key_cols)
        result["dataset_name"] = dataset_name
        result["file_name"] = filename
        validation_rows.append(result)

        dup_df = duplicate_extract(df, key_cols)
        if not dup_df.empty:
            write_csv(out_dir / f"{dataset_name}__duplicate_keys.csv", dup_df)

        write_json(out_dir / f"{dataset_name}__key_validation.json", result)

    write_csv(out_dir / "prepare_key_validation_summary.csv", pd.DataFrame(validation_rows))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate candidate primary keys for PREPARE.")
    parser.add_argument("--raw-dir", required=True, help="Directory containing raw CSV files")
    parser.add_argument("--out-dir", required=True, help="Output directory for key validation")
    args = parser.parse_args()

    run(Path(args.raw_dir), Path(args.out_dir))