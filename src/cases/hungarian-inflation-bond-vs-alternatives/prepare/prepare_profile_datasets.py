from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_prepare_utils import (
    RAW_FILES,
    dataset_overview,
    load_csv,
    load_meta_if_exists,
    parse_dates_by_name,
    schema_records,
    write_csv,
    write_json,
)


def column_level_profile(df: pd.DataFrame) -> pd.DataFrame:
    parsed = parse_dates_by_name(df)
    records = schema_records(parsed)
    return pd.DataFrame(records)


def file_level_profile(raw_dir: Path) -> pd.DataFrame:
    rows = []
    for dataset_name, filename in RAW_FILES.items():
        path = raw_dir / filename
        df = load_csv(path)
        overview = dataset_overview(df, path)
        overview["dataset_name"] = dataset_name
        overview["meta_found"] = bool(load_meta_if_exists(path))
        rows.append(overview)
    return pd.DataFrame(rows)


def run(raw_dir: Path, out_dir: Path) -> None:
    summary_rows = []

    file_profile = file_level_profile(raw_dir)
    write_csv(out_dir / "prepare_file_profile.csv", file_profile)

    for dataset_name, filename in RAW_FILES.items():
        path = raw_dir / filename
        df = load_csv(path)
        meta = load_meta_if_exists(path)

        col_profile = column_level_profile(df)
        write_csv(out_dir / f"{dataset_name}__column_profile.csv", col_profile)

        parsed = parse_dates_by_name(df)
        summary_rows.append(
            {
                "dataset_name": dataset_name,
                "file_name": filename,
                "rows": int(len(df)),
                "cols": int(df.shape[1]),
                "date_columns_detected": ",".join(
                    [c for c in parsed.columns if str(parsed[c].dtype).startswith("datetime64")]
                ),
                "total_missing_values": int(df.isna().sum().sum()),
                "duplicate_full_rows": int(df.duplicated().sum()),
                "meta_found": bool(meta),
            }
        )

        write_json(
            out_dir / f"{dataset_name}__overview.json",
            {
                "dataset_name": dataset_name,
                "file_name": filename,
                "file_profile": dataset_overview(df, path),
                "meta": meta,
                "column_profile": col_profile.to_dict(orient="records"),
            },
        )

    write_csv(out_dir / "prepare_dataset_summary.csv", pd.DataFrame(summary_rows))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate PREPARE dataset profiles.")
    parser.add_argument("--raw-dir", required=True, help="Directory containing raw CSV files")
    parser.add_argument("--out-dir", required=True, help="Output directory for prepare profiles")
    args = parser.parse_args()

    run(Path(args.raw_dir), Path(args.out_dir))