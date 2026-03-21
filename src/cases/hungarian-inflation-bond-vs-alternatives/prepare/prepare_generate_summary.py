from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_prepare_utils import write_text


def read_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def render_markdown(
    file_profile: pd.DataFrame,
    dataset_summary: pd.DataFrame,
    key_validation: pd.DataFrame,
) -> str:
    lines: list[str] = []

    lines.append("# PREPARE Output Summary")
    lines.append("")
    lines.append("This file is machine-generated from PREPARE profiling outputs.")
    lines.append("")
    lines.append("## 1. File-Level Profile")
    lines.append("")
    lines.append(file_profile.to_markdown(index=False))
    lines.append("")
    lines.append("## 2. Dataset Summary")
    lines.append("")
    lines.append(dataset_summary.to_markdown(index=False))
    lines.append("")
    lines.append("## 3. Key Validation Summary")
    lines.append("")
    lines.append(key_validation.to_markdown(index=False))
    lines.append("")
    lines.append("## 4. Validation Notes")
    lines.append("")
    lines.append("- Row and column counts captured for each file.")
    lines.append("- Full-row duplicates checked.")
    lines.append("- Candidate primary keys evaluated.")
    lines.append("- Column-level null counts profiled.")
    lines.append("- Date parsing should still be verified during PROCESS.")
    lines.append("")
    lines.append("## 5. Recommended Next Checks")
    lines.append("")
    lines.append("- Review any duplicate-key extracts.")
    lines.append("- Confirm ticker universe and date coverage by ticker.")
    lines.append("- Confirm monthly continuity for CPI and 10Y yield.")
    lines.append("- Normalize percentage strings in bond template during PROCESS.")
    lines.append("")

    return "\n".join(lines)


def run(out_dir: Path) -> None:
    file_profile = read_csv_if_exists(out_dir / "prepare_file_profile.csv")
    dataset_summary = read_csv_if_exists(out_dir / "prepare_dataset_summary.csv")
    key_validation = read_csv_if_exists(out_dir / "prepare_key_validation_summary.csv")

    text = render_markdown(file_profile, dataset_summary, key_validation)
    write_text(out_dir / "prepare_output_summary.md", text)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate markdown summary from PREPARE outputs.")
    parser.add_argument("--out-dir", required=True, help="Output directory containing prepare results")
    args = parser.parse_args()

    run(Path(args.out_dir))