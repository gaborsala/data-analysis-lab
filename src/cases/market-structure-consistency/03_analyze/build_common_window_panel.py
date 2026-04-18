from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_repo_root


EXPECTED_SECTOR_COUNT = 11


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build common-window companion datasets for stricter cross-sector comparison."
    )
    parser.add_argument(
        "--ratio-file",
        default=None,
        help=(
            "Optional override for daily long ratio panel. "
            "Defaults to cases/market-structure-consistency/outputs/02_process/"
            "historical_ratio_panel.csv"
        ),
    )
    parser.add_argument(
        "--classified-file",
        default=None,
        help=(
            "Optional override for classified weekly panel. "
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


def get_default_ratio_file() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "02_process"
        / "historical_ratio_panel.csv"
    )


def get_default_classified_file() -> Path:
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


def load_ratio_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Daily ratio panel not found: {path}")

    df = pd.read_csv(path)
    required = {"date", "ticker", "adj_close", "spy_adj_close", "ratio_value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Daily ratio panel missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.sort_values(["date", "ticker"]).reset_index(drop=True)


def load_classified_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Weekly classified panel not found: {path}")

    df = pd.read_csv(path)
    required = {"date", "ticker", "ratio_value", "direction", "classification_ready"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Weekly classified panel missing required columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["classification_ready"] = df["classification_ready"].astype(bool)
    return df.sort_values(["date", "ticker"]).reset_index(drop=True)


def build_common_daily(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    coverage = (
        df.groupby("date", as_index=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            non_null_ratio_count=("ratio_value", lambda s: int(s.notna().sum())),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    common_dates = coverage.loc[
        coverage["non_null_ratio_count"] == EXPECTED_SECTOR_COUNT, "date"
    ]

    common_df = df.loc[df["date"].isin(common_dates)].copy()
    return common_df, coverage


def build_common_weekly(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    coverage = (
        df.groupby("date", as_index=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            non_null_ratio_count=("ratio_value", lambda s: int(s.notna().sum())),
            classification_ready_count=("classification_ready", lambda s: int(s.sum())),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    common_dates = coverage.loc[
        (coverage["non_null_ratio_count"] == EXPECTED_SECTOR_COUNT)
        & (coverage["classification_ready_count"] == EXPECTED_SECTOR_COUNT),
        "date"
    ]

    common_df = df.loc[df["date"].isin(common_dates)].copy()
    return common_df, coverage


def main() -> None:
    args = parse_args()

    ratio_file = Path(args.ratio_file).resolve() if args.ratio_file else get_default_ratio_file().resolve()
    classified_file = (
        Path(args.classified_file).resolve()
        if args.classified_file
        else get_default_classified_file().resolve()
    )
    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_default_out_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Daily ratio file: {ratio_file}")
    print(f"Weekly classified file: {classified_file}")
    print(f"Output directory: {out_dir}")

    daily_df = load_ratio_panel(ratio_file)
    weekly_df = load_classified_panel(classified_file)

    common_daily_df, daily_coverage_df = build_common_daily(daily_df)
    common_weekly_df, weekly_coverage_df = build_common_weekly(weekly_df)

    common_daily_path = out_dir / "historical_ratio_panel_common_window.csv"
    common_weekly_path = out_dir / "historical_weekly_structure_classification_common_window.csv"
    daily_coverage_path = out_dir / "historical_ratio_panel_daily_date_coverage.csv"
    weekly_coverage_path = out_dir / "historical_weekly_structure_date_coverage.csv"

    common_daily_df.to_csv(common_daily_path, index=False)
    common_weekly_df.to_csv(common_weekly_path, index=False)
    daily_coverage_df.to_csv(daily_coverage_path, index=False)
    weekly_coverage_df.to_csv(weekly_coverage_path, index=False)

    print("\nCommon-window build complete")
    print(f"- Daily common-window panel: {common_daily_path}")
    print(f"- Weekly common-window panel: {common_weekly_path}")
    print(f"- Daily date coverage: {daily_coverage_path}")
    print(f"- Weekly date coverage: {weekly_coverage_path}")
    print(f"- Daily common-window rows: {len(common_daily_df)}")
    print(f"- Weekly common-window rows: {len(common_weekly_df)}")


if __name__ == "__main__":
    main()