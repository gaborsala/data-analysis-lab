from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run full dataset pipeline and save everything into one single folder."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Single output directory where all pipeline outputs will be saved."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the output directory before running."
    )
    return parser.parse_args()


def prepare_output_dir(output_dir: str, clean: bool) -> Path:
    out_dir = Path(output_dir).resolve()

    if clean and out_dir.exists():
        shutil.rmtree(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def run_script(script_path: Path, output_dir: Path) -> None:
    print(f"\n[RUN] {script_path.name}")

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--output-dir",
            str(output_dir),
        ],
        cwd=script_path.parent,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip())
        raise RuntimeError(f"Script failed: {script_path.name}")

    print(f"[OK] {script_path.name}")


def main() -> None:
    args = parse_args()

    base_dir = Path(__file__).resolve().parent
    output_dir = prepare_output_dir(args.output_dir, args.clean)

    scripts = [
        "fetch_etf_prices.py",
        "fetch_hungary_cpi.py",
        "fetch_hungary_rates.py",
        "fetch_bond_reference.py",
    ]

    print("Starting full dataset pipeline...")
    print(f"Working directory: {base_dir}")
    print(f"Single output directory: {output_dir}")

    for script_name in scripts:
        script_path = base_dir / script_name

        if not script_path.exists():
            raise FileNotFoundError(f"Missing required script: {script_path}")

        run_script(script_path, output_dir)

    print("\nFull dataset pipeline completed successfully.")


if __name__ == "__main__":
    main()