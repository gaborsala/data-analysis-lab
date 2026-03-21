from __future__ import annotations

import argparse
from pathlib import Path

from common_prepare_utils import ensure_dir, write_text
from prepare_generate_summary import run as generate_summary_run
from prepare_profile_datasets import run as profile_run
from prepare_validate_keys import run as key_validation_run


def build_readme(raw_dir: Path, out_dir: Path) -> str:
    return f"""# PREPARE Run Notes

## Inputs
- Raw directory: `{raw_dir}`

## Outputs
- `prepare_file_profile.csv`
- `prepare_dataset_summary.csv`
- `prepare_key_validation_summary.csv`
- `*_column_profile.csv`
- `*_overview.json`
- `*_key_validation.json`
- `prepare_output_summary.md`

## Purpose
This run profiles the raw dataset package for structural understanding only.
No cleaning or transformation is applied here.

## Validation scope
- file-level row/column checks
- schema profiling
- null profiling
- duplicate full-row checks
- candidate primary key validation

## Limitations
- no economic interpretation
- no return calculations
- no frequency harmonization
- no source-authority reconciliation
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full PREPARE profiling pipeline.")
    parser.add_argument("--raw-dir", required=True, help="Directory containing raw case CSV files")
    parser.add_argument("--out-dir", required=True, help="Directory to store prepare outputs")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = ensure_dir(Path(args.out_dir))

    profile_run(raw_dir, out_dir)
    key_validation_run(raw_dir, out_dir)
    generate_summary_run(out_dir)

    write_text(out_dir / "README_prepare_outputs.md", build_readme(raw_dir, out_dir))
    print(f"PREPARE profiling complete. Outputs written to: {out_dir}")


if __name__ == "__main__":
    main()