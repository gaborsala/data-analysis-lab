from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_repo_root


VALID_DIRECTIONS = {"HH/HL", "LH/LL", "TRANSITION"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build duration summaries from historical weekly structure classifications."
    )
    parser.add_argument(
        "--input-file",
        default=None,
        help=(
            "Optional override for classified weekly input file. "
            "Defaults to cases/market-structure-consistency/outputs/02_process/"
            "historical_weekly_structure_classification.csv"
        ),
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "Optional override for output directory. "
            "Defaults to cases/market-structure-consistency/outputs/03_analyze"
        ),
    )
    return parser.parse_args()


def get_default_input_file() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "02_process"
        / "historical_weekly_structure_classification.csv"
    )


def get_default_out_dir() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "03_analyze"
    )


def load_classified_weekly(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Classified weekly input not found: {path}")

    df = pd.read_csv(path)
    required = {"date", "ticker", "direction", "classification_ready"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    bad_dates = int(df["date"].isna().sum())
    if bad_dates > 0:
        raise ValueError(f"Input contains {bad_dates} invalid dates.")

    df["classification_ready"] = df["classification_ready"].astype(bool)

    return df.sort_values(["ticker", "date"]).reset_index(drop=True)


def build_run_table(df: pd.DataFrame) -> pd.DataFrame:
    ready = df.loc[df["classification_ready"] & df["direction"].isin(VALID_DIRECTIONS)].copy()
    ready = ready.sort_values(["ticker", "date"]).reset_index(drop=True)

    if ready.empty:
        return pd.DataFrame(
            columns=[
                "ticker",
                "direction",
                "run_id",
                "start_date",
                "end_date",
                "duration_weeks",
            ]
        )

    ready["prev_direction"] = ready.groupby("ticker")["direction"].shift(1)
    ready["new_run_flag"] = (
        ready["prev_direction"].isna() | (ready["direction"] != ready["prev_direction"])
    )
    ready["run_id"] = ready.groupby("ticker")["new_run_flag"].cumsum()

    runs = (
        ready.groupby(["ticker", "direction", "run_id"], as_index=False)
        .agg(
            start_date=("date", "min"),
            end_date=("date", "max"),
            duration_weeks=("date", "size"),
        )
        .sort_values(["ticker", "start_date", "run_id"])
        .reset_index(drop=True)
    )

    runs["start_date"] = runs["start_date"].dt.strftime("%Y-%m-%d")
    runs["end_date"] = runs["end_date"].dt.strftime("%Y-%m-%d")
    return runs


def build_duration_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    if run_df.empty:
        return pd.DataFrame(
            columns=[
                "ticker",
                "direction",
                "run_count",
                "avg_duration_weeks",
                "median_duration_weeks",
                "min_duration_weeks",
                "max_duration_weeks",
            ]
        )

    summary = (
        run_df.groupby(["ticker", "direction"], as_index=False)
        .agg(
            run_count=("run_id", "nunique"),
            avg_duration_weeks=("duration_weeks", "mean"),
            median_duration_weeks=("duration_weeks", "median"),
            min_duration_weeks=("duration_weeks", "min"),
            max_duration_weeks=("duration_weeks", "max"),
        )
        .sort_values(["ticker", "direction"])
        .reset_index(drop=True)
    )

    summary["avg_duration_weeks"] = summary["avg_duration_weeks"].round(2)
    summary["median_duration_weeks"] = summary["median_duration_weeks"].round(2)
    return summary


def build_recent_vs_historical(run_df: pd.DataFrame) -> pd.DataFrame:
    if run_df.empty:
        return pd.DataFrame(
            columns=[
                "ticker",
                "latest_direction",
                "latest_duration_weeks",
                "historical_avg_duration_weeks_same_direction",
                "difference_vs_historical_avg_weeks",
            ]
        )

    latest_runs = (
        run_df.sort_values(["ticker", "end_date"])
        .groupby("ticker", as_index=False)
        .tail(1)
        .rename(
            columns={
                "direction": "latest_direction",
                "duration_weeks": "latest_duration_weeks",
            }
        )
    )

    hist_avg = (
        run_df.groupby(["ticker", "direction"], as_index=False)
        .agg(historical_avg_duration_weeks_same_direction=("duration_weeks", "mean"))
        .rename(columns={"direction": "latest_direction"})
    )

    out = latest_runs.merge(
        hist_avg,
        on=["ticker", "latest_direction"],
        how="left",
        validate="many_to_one",
    )

    out["historical_avg_duration_weeks_same_direction"] = (
        out["historical_avg_duration_weeks_same_direction"].round(2)
    )
    out["difference_vs_historical_avg_weeks"] = (
        out["latest_duration_weeks"] - out["historical_avg_duration_weeks_same_direction"]
    ).round(2)

    return out[
        [
            "ticker",
            "latest_direction",
            "start_date",
            "end_date",
            "latest_duration_weeks",
            "historical_avg_duration_weeks_same_direction",
            "difference_vs_historical_avg_weeks",
        ]
    ].sort_values("ticker").reset_index(drop=True)


def main() -> None:
    args = parse_args()

    input_file = (
        Path(args.input_file).resolve() if args.input_file else get_default_input_file().resolve()
    )
    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_default_out_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input classified weekly file: {input_file}")
    print(f"Output directory: {out_dir}")

    df = load_classified_weekly(input_file)
    run_df = build_run_table(df)
    summary_df = build_duration_summary(run_df)
    recent_df = build_recent_vs_historical(run_df)

    run_path = out_dir / "weekly_structure_duration_runs.csv"
    summary_path = out_dir / "weekly_structure_duration_summary.csv"
    recent_path = out_dir / "weekly_structure_recent_vs_historical_duration.csv"

    run_df.to_csv(run_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    recent_df.to_csv(recent_path, index=False)

    print("\nDuration build complete")
    print(f"- Run table: {run_path}")
    print(f"- Duration summary: {summary_path}")
    print(f"- Recent vs historical: {recent_path}")
    print(f"- Total runs: {len(run_df)}")
    print(f"- Summary rows: {len(summary_df)}")
    print(f"- Recent comparison rows: {len(recent_df)}")


if __name__ == "__main__":
    main()