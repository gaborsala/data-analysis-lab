from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_repo_root


VALID_DIRECTIONS = ["HH/HL", "LH/LL", "TRANSITION"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build transition matrices from historical weekly structure classifications."
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

    ready = df.loc[df["classification_ready"] & df["direction"].isin(VALID_DIRECTIONS)].copy()
    return ready.sort_values(["ticker", "date"]).reset_index(drop=True)


def build_transition_events(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["from_direction"] = work.groupby("ticker")["direction"].shift(1)
    work["from_date"] = work.groupby("ticker")["date"].shift(1)
    work = work.dropna(subset=["from_direction", "from_date"]).copy()

    work = work.rename(columns={"direction": "to_direction", "date": "to_date"})
    work["transition_changed"] = work["from_direction"] != work["to_direction"]

    work["from_date"] = pd.to_datetime(work["from_date"]).dt.strftime("%Y-%m-%d")
    work["to_date"] = pd.to_datetime(work["to_date"]).dt.strftime("%Y-%m-%d")

    return work[
        [
            "ticker",
            "from_date",
            "to_date",
            "from_direction",
            "to_direction",
            "transition_changed",
        ]
    ].reset_index(drop=True)


def build_transition_summary(events_df: pd.DataFrame) -> pd.DataFrame:
    if events_df.empty:
        return pd.DataFrame(
            columns=[
                "from_direction",
                "to_direction",
                "transition_count",
                "transition_share_from_state",
            ]
        )

    summary = (
        events_df.groupby(["from_direction", "to_direction"], as_index=False)
        .agg(transition_count=("ticker", "size"))
    )

    from_totals = (
        summary.groupby("from_direction", as_index=False)
        .agg(total_from_count=("transition_count", "sum"))
    )

    summary = summary.merge(from_totals, on="from_direction", how="left", validate="many_to_one")
    summary["transition_share_from_state"] = (
        summary["transition_count"] / summary["total_from_count"] * 100.0
    ).round(2)

    return summary[
        ["from_direction", "to_direction", "transition_count", "transition_share_from_state"]
    ].sort_values(["from_direction", "to_direction"]).reset_index(drop=True)


def build_transition_matrix(summary_df: pd.DataFrame) -> pd.DataFrame:
    if summary_df.empty:
        return pd.DataFrame(index=VALID_DIRECTIONS, columns=VALID_DIRECTIONS)

    matrix = (
        summary_df.pivot(index="from_direction", columns="to_direction", values="transition_count")
        .reindex(index=VALID_DIRECTIONS, columns=VALID_DIRECTIONS)
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    return matrix


def build_changed_transition_summary(events_df: pd.DataFrame) -> pd.DataFrame:
    changed = events_df.loc[events_df["transition_changed"]].copy()
    if changed.empty:
        return pd.DataFrame(
            columns=["from_direction", "to_direction", "transition_count"]
        )

    out = (
        changed.groupby(["from_direction", "to_direction"], as_index=False)
        .agg(transition_count=("ticker", "size"))
        .sort_values(["from_direction", "to_direction"])
        .reset_index(drop=True)
    )
    return out


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
    events_df = build_transition_events(df)
    summary_df = build_transition_summary(events_df)
    matrix_df = build_transition_matrix(summary_df)
    changed_df = build_changed_transition_summary(events_df)

    events_path = out_dir / "weekly_structure_transition_events.csv"
    summary_path = out_dir / "weekly_structure_transition_summary.csv"
    matrix_path = out_dir / "weekly_structure_transition_matrix.csv"
    changed_path = out_dir / "weekly_structure_changed_transitions_only.csv"

    events_df.to_csv(events_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    matrix_df.to_csv(matrix_path, index=False)
    changed_df.to_csv(changed_path, index=False)

    print("\nTransition build complete")
    print(f"- Transition events: {events_path}")
    print(f"- Transition summary: {summary_path}")
    print(f"- Transition matrix: {matrix_path}")
    print(f"- Changed transitions only: {changed_path}")
    print(f"- Event rows: {len(events_df)}")
    print(f"- Summary rows: {len(summary_df)}")
    print(f"- Changed-transition rows: {len(changed_df)}")


if __name__ == "__main__":
    main()