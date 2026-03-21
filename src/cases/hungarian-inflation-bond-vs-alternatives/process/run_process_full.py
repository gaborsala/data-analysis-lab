from __future__ import annotations

import argparse
from pathlib import Path

from common_process_utils import ensure_dir, write_text
from process_clean_datasets import run as clean_run
from process_generate_summary import run as summary_run
from process_profile_ticker_coverage import run as coverage_run
from process_validate_etf_null_windows import run as null_validation_run


def build_readme(raw_dir: Path, out_dir: Path) -> str:
    return f"""# PROCESS Run Notes

## Inputs
- Raw directory: `{raw_dir}`

## Outputs
- raw_snapshot hashes preserved through summary generation
- etf_ticker_coverage_profile.csv
- etf_null_window_classification_detailed.csv
- etf_null_window_classification_summary.csv
- cleaned CSV outputs
- month-end ETF resample
- monthly merged context
- process_output_summary.md

## Execution order
1. ticker coverage profiling
2. ETF null-window validation
3. dataset cleaning and normalization
4. monthly resampling and merged context generation
5. summary generation

## Guardrails
- no silent filtering
- no imputation of ETF close prices
- percent normalization adds columns instead of overwriting raw strings
- resampling rule is explicit and auditable
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full PROCESS pipeline.")
    parser.add_argument("--raw-dir", required=True, help="Directory containing raw case CSV files")
    parser.add_argument("--out-dir", required=True, help="Directory to store process outputs")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = ensure_dir(Path(args.out_dir))

    coverage_run(raw_dir, out_dir)
    null_validation_run(raw_dir, out_dir)
    clean_run(raw_dir, out_dir)
    summary_run(raw_dir, out_dir)

    write_text(out_dir / "README_process_outputs.md", build_readme(raw_dir, out_dir))
    print(f"PROCESS run complete. Outputs written to: {out_dir}")


if __name__ == "__main__":
    main()