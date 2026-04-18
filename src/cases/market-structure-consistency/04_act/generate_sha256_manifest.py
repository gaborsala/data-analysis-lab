from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd

from config import get_repo_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a SHA256 manifest for market-structure-consistency key inputs and outputs."
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "Optional override for output directory. "
            "Defaults to cases/market-structure-consistency/outputs/02_process"
        ),
    )
    return parser.parse_args()


def get_default_out_dir() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "02_process"
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> list[Path]:
    repo_root = get_repo_root()
    candidates = [
        repo_root / "data" / "raw" / "raw_download_manifest.csv",
        repo_root / "data" / "raw" / "raw_data_audit.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_adjusted_close_wide.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_ratio_panel.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_ratio_panel_coverage.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_weekly_ratio_panel.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_weekly_structure_classification.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_weekly_structure_summary.csv",
        repo_root / "cases" / "market-structure-consistency" / "outputs" / "02_process" / "historical_weekly_structure_latest.csv",
    ]
    return [p for p in candidates if p.exists()]


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_default_out_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    files = collect_files()
    if not files:
        raise FileNotFoundError("No expected files found for SHA256 manifest generation.")

    rows = []
    for path in files:
        stat = path.stat()
        rows.append(
            {
                "relative_path": str(path.relative_to(get_repo_root())),
                "file_size_bytes": int(stat.st_size),
                "sha256": sha256_file(path),
            }
        )

    manifest = pd.DataFrame(rows).sort_values("relative_path").reset_index(drop=True)
    out_path = out_dir / "sha256_manifest.csv"
    manifest.to_csv(out_path, index=False)

    print("SHA256 manifest generated")
    print(f"- Output: {out_path}")
    print(f"- File count: {len(manifest)}")


if __name__ == "__main__":
    main()