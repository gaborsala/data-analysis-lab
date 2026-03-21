"""
ANALYZE — Full Stage Runner
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Run the full ANALYZE stage in deterministic order:

1. rolling 12-month return analysis
2. threshold exceedance analysis
3. volatility and max drawdown analysis
4. summary table generation

This runner is designed to:
- fail fast on the first error
- preserve audit traceability
- write a single stage-level run log
- support explicit benchmark overrides when needed

Primary outputs
---------------
Indirectly generates all outputs from the called ANALYZE scripts, including:
- rolling return tables
- threshold exceedance tables
- volatility/drawdown tables
- combined summary tables
- benchmark review tables

Direct output:
- 03_ANALYZE/outputs/logs/run_analyze_full.log

Assumptions
-----------
1. The ANALYZE scripts exist in the same src/ directory:
   - analyze_rolling_12m_returns.py
   - analyze_threshold_exceedance.py
   - analyze_volatility_drawdown.py
   - analyze_generate_summary_tables.py
2. PROCESS outputs are already available and stable.
3. The current Python environment includes all required dependencies.
4. This script is run from a context where relative paths are valid, or explicit paths are provided.

Limitations
-----------
1. This script orchestrates execution but does not validate the economic meaning
   of the selected benchmark threshold.
2. If upstream file schemas change, downstream scripts may still fail.
3. This runner does not perform chart generation.
4. Final narrative interpretation still belongs in the ANALYZE markdown artifact.

Validation checks performed/recommended
---------------------------------------
Performed:
- required script file existence check
- subprocess return-code validation
- fail-fast behavior on first error
- single stage log with command trace and stderr/stdout capture

Recommended:
- inspect benchmark_definition_check.csv after run
- confirm ticker counts across summary outputs
- spot-check one ticker manually before writing conclusions
"""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_ORDER = [
    "analyze_rolling_12m_returns.py",
    "analyze_threshold_exceedance.py",
    "analyze_volatility_drawdown.py",
    "analyze_generate_summary_tables.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run full ANALYZE stage for Hungarian Inflation Bond vs Alternatives."
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="Case-study root directory containing 02_PROCESS/ and 03_ANALYZE/.",
    )
    parser.add_argument(
        "--process-dir",
        type=str,
        default="02_PROCESS/outputs",
        help="Relative path from project root to PROCESS outputs directory.",
    )
    parser.add_argument(
        "--analyze-dir",
        type=str,
        default="03_ANALYZE",
        help="Relative path from project root to ANALYZE directory.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="both",
        help="Mode to run: full-history, common-window, or both.",
    )
    parser.add_argument(
        "--threshold-value",
        type=float,
        default=None,
        help="Optional constant annual threshold in decimal form. Example: 0.05 for 5%%.",
    )
    parser.add_argument(
        "--threshold-col",
        type=str,
        default=None,
        help="Optional exact threshold column name for threshold exceedance analysis.",
    )
    return parser.parse_args()


def ensure_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")


def build_command(
    python_executable: str,
    script_path: Path,
    *,
    project_root: str,
    process_dir: str | None = None,
    analyze_dir: str | None = None,
    mode: str | None = None,
    threshold_value: float | None = None,
    threshold_col: str | None = None,
) -> list[str]:
    cmd = [python_executable, str(script_path)]

    if project_root is not None:
        cmd.extend(["--project-root", project_root])

    if process_dir is not None and script_path.name != "analyze_generate_summary_tables.py":
        cmd.extend(["--process-dir", process_dir])

    if analyze_dir is not None:
        cmd.extend(["--analyze-dir", analyze_dir])

    if mode is not None and script_path.name != "analyze_generate_summary_tables.py":
        cmd.extend(["--mode", mode])

    if script_path.name == "analyze_threshold_exceedance.py":
        if threshold_value is not None:
            cmd.extend(["--threshold-value", str(threshold_value)])
        if threshold_col is not None:
            cmd.extend(["--threshold-col", threshold_col])

    return cmd


def run_one_command(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def quote_cmd(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def main() -> None:
    args = parse_args()

    project_root = Path(args.project_root).resolve()
    analyze_dir = (project_root / args.analyze_dir).resolve()

    # Use the actual folder where this runner file lives
    src_dir = Path(__file__).resolve().parent

    logs_dir = analyze_dir / "outputs" / "logs"

    ensure_exists(project_root, "Project root")
    ensure_exists(analyze_dir, "ANALYZE directory")
    ensure_exists(src_dir, "ANALYZE src directory")

    for script_name in SCRIPT_ORDER:
        ensure_exists(src_dir / script_name, f"Required script '{script_name}'")

    stage_log_path = logs_dir / "run_analyze_full.log"
    started_at = datetime.now().isoformat(timespec="seconds")

    log_parts: list[str] = []
    log_parts.append("ANALYZE FULL RUN")
    log_parts.append(f"started_at: {started_at}")
    log_parts.append(f"project_root: {project_root}")
    log_parts.append(f"process_dir: {args.process_dir}")
    log_parts.append(f"analyze_dir: {args.analyze_dir}")
    log_parts.append(f"mode: {args.mode}")
    log_parts.append(f"threshold_value: {args.threshold_value}")
    log_parts.append(f"threshold_col: {args.threshold_col}")
    log_parts.append("")

    python_executable = sys.executable

    for step_number, script_name in enumerate(SCRIPT_ORDER, start=1):
        script_path = src_dir / script_name

        cmd = build_command(
            python_executable=python_executable,
            script_path=script_path,
            project_root=str(project_root),
            process_dir=args.process_dir,
            analyze_dir=args.analyze_dir,
            mode=args.mode,
            threshold_value=args.threshold_value,
            threshold_col=args.threshold_col,
        )

        log_parts.append(f"STEP {step_number}: {script_name}")
        log_parts.append(f"command: {quote_cmd(cmd)}")

        result = run_one_command(cmd, cwd=project_root)

        log_parts.append(f"return_code: {result.returncode}")
        log_parts.append("stdout:")
        log_parts.append(result.stdout.strip() if result.stdout.strip() else "<empty>")
        log_parts.append("stderr:")
        log_parts.append(result.stderr.strip() if result.stderr.strip() else "<empty>")
        log_parts.append("")

        if result.returncode != 0:
            finished_at = datetime.now().isoformat(timespec="seconds")
            log_parts.append("status: FAILED")
            log_parts.append(f"failed_step: {script_name}")
            log_parts.append(f"finished_at: {finished_at}")
            stage_log_path.write_text("\n".join(log_parts), encoding="utf-8")

            raise RuntimeError(
                f"ANALYZE stage failed at step {step_number} ({script_name}). "
                f"See log: {stage_log_path}"
            )

    finished_at = datetime.now().isoformat(timespec="seconds")
    log_parts.append("status: SUCCESS")
    log_parts.append(f"finished_at: {finished_at}")

    stage_log_path.write_text("\n".join(log_parts), encoding="utf-8")


if __name__ == "__main__":
    main()