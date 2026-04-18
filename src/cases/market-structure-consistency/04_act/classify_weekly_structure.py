from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_repo_root


BENCHMARK_TICKER = "SPY"
DEFAULT_BLOCK_WEEKS = 4
MIN_REQUIRED_WEEKS = DEFAULT_BLOCK_WEEKS * 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Resample the historical daily ratio panel to weekly frequency and "
            "classify structural state using block-based HH/HL vs LH/LL logic."
        )
    )
    parser.add_argument(
        "--input-file",
        default=None,
        help=(
            "Optional override for the long-format input ratio panel. "
            "Defaults to cases/market-structure-consistency/outputs/02_process/"
            "historical_ratio_panel.csv"
        ),
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "Optional override for output directory. "
            "Defaults to cases/market-structure-consistency/outputs/02_process"
        ),
    )
    parser.add_argument(
        "--block-weeks",
        type=int,
        default=DEFAULT_BLOCK_WEEKS,
        help=(
            "Number of weekly observations per comparison block. "
            "Classification compares current block vs prior block."
        ),
    )
    parser.add_argument(
        "--weekly-rule",
        default="W-FRI",
        help="Pandas weekly resample rule. Default: W-FRI",
    )
    return parser.parse_args()


def get_default_input_file() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "02_process"
        / "historical_ratio_panel.csv"
    )


def get_default_out_dir() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "02_process"
    )


def validate_long_panel(df: pd.DataFrame) -> None:
    required_cols = {"date", "ticker", "adj_close", "spy_adj_close", "ratio_value"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Input ratio panel is missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Input ratio panel is empty.")

    invalid_dates = pd.to_datetime(df["date"], errors="coerce").isna().sum()
    if invalid_dates > 0:
        raise ValueError(f"Input ratio panel contains {int(invalid_dates)} invalid dates.")

    duplicate_key_count = (
        df.assign(date=pd.to_datetime(df["date"], errors="coerce"))
        .duplicated(subset=["ticker", "date"])
        .sum()
    )
    if duplicate_key_count > 0:
        raise ValueError(
            f"Input ratio panel contains {int(duplicate_key_count)} duplicate ticker-date rows."
        )


def load_ratio_panel(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input ratio panel not found: {path}")

    df = pd.read_csv(path)
    validate_long_panel(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["ratio_value"] = pd.to_numeric(df["ratio_value"], errors="coerce")
    df["adj_close"] = pd.to_numeric(df["adj_close"], errors="coerce")
    df["spy_adj_close"] = pd.to_numeric(df["spy_adj_close"], errors="coerce")

    return df.sort_values(["ticker", "date"]).reset_index(drop=True)


def build_weekly_ratio_panel(
    long_df: pd.DataFrame,
    weekly_rule: str,
) -> pd.DataFrame:
    weekly_frames: list[pd.DataFrame] = []

    for ticker, grp in long_df.groupby("ticker", sort=True):
        grp = grp.sort_values("date").copy()
        grp = grp.set_index("date")

        weekly = (
            grp[["adj_close", "spy_adj_close", "ratio_value"]]
            .resample(weekly_rule)
            .last()
            .reset_index()
        )

        weekly["ticker"] = ticker
        weekly["has_ratio"] = weekly["ratio_value"].notna()
        weekly["has_adj_close"] = weekly["adj_close"].notna()

        weekly_frames.append(weekly)

    if not weekly_frames:
        raise RuntimeError("No weekly frames were created from the input panel.")

    weekly_df = pd.concat(weekly_frames, ignore_index=True)
    weekly_df = weekly_df.sort_values(["ticker", "date"]).reset_index(drop=True)

    return weekly_df[
        [
            "date",
            "ticker",
            "adj_close",
            "spy_adj_close",
            "ratio_value",
            "has_adj_close",
            "has_ratio",
        ]
    ]


def classify_one_ticker(
    grp: pd.DataFrame,
    block_weeks: int,
) -> pd.DataFrame:
    grp = grp.sort_values("date").copy()
    grp["observation_index"] = range(1, len(grp) + 1)

    # Only weeks with a valid ratio can be classified.
    valid = grp.loc[grp["ratio_value"].notna(), ["date", "ticker", "ratio_value"]].copy()
    valid = valid.sort_values("date").reset_index(drop=True)
    valid["valid_ratio_index"] = range(1, len(valid) + 1)

    result_rows: list[dict] = []

    for idx in range(len(valid)):
        current_row = valid.iloc[idx]
        valid_ratio_index = int(current_row["valid_ratio_index"])

        if valid_ratio_index < block_weeks * 2:
            result_rows.append(
                {
                    "date": current_row["date"],
                    "ticker": current_row["ticker"],
                    "weekly_ratio": float(current_row["ratio_value"]),
                    "valid_ratio_index": valid_ratio_index,
                    "current_block_high": pd.NA,
                    "current_block_low": pd.NA,
                    "prior_block_high": pd.NA,
                    "prior_block_low": pd.NA,
                    "high_delta": pd.NA,
                    "low_delta": pd.NA,
                    "direction": "INSUFFICIENT_HISTORY",
                    "classification_ready": False,
                }
            )
            continue

        current_block = valid.iloc[idx - block_weeks + 1 : idx + 1]
        prior_block = valid.iloc[idx - (block_weeks * 2) + 1 : idx - block_weeks + 1]

        current_block_high = float(current_block["ratio_value"].max())
        current_block_low = float(current_block["ratio_value"].min())
        prior_block_high = float(prior_block["ratio_value"].max())
        prior_block_low = float(prior_block["ratio_value"].min())

        high_delta = current_block_high - prior_block_high
        low_delta = current_block_low - prior_block_low

        if current_block_high > prior_block_high and current_block_low > prior_block_low:
            direction = "HH/HL"
        elif current_block_high < prior_block_high and current_block_low < prior_block_low:
            direction = "LH/LL"
        else:
            direction = "TRANSITION"

        result_rows.append(
            {
                "date": current_row["date"],
                "ticker": current_row["ticker"],
                "weekly_ratio": float(current_row["ratio_value"]),
                "valid_ratio_index": valid_ratio_index,
                "current_block_high": current_block_high,
                "current_block_low": current_block_low,
                "prior_block_high": prior_block_high,
                "prior_block_low": prior_block_low,
                "high_delta": high_delta,
                "low_delta": low_delta,
                "direction": direction,
                "classification_ready": True,
            }
        )

    result_df = pd.DataFrame(result_rows)

    merged = grp.merge(
        result_df,
        on=["date", "ticker"],
        how="left",
        validate="one_to_one",
    )

    merged["weekly_ratio"] = merged["weekly_ratio"].fillna(merged["ratio_value"])

    merged["direction"] = merged["direction"].fillna("NO_RATIO")
    merged["classification_ready"] = merged["classification_ready"].fillna(False)

    return merged


def classify_weekly_structure(
    weekly_df: pd.DataFrame,
    block_weeks: int,
) -> pd.DataFrame:
    classified_frames: list[pd.DataFrame] = []

    for ticker, grp in weekly_df.groupby("ticker", sort=True):
        classified = classify_one_ticker(grp=grp, block_weeks=block_weeks)
        classified_frames.append(classified)

    if not classified_frames:
        raise RuntimeError("No classified frames were produced.")

    out = pd.concat(classified_frames, ignore_index=True)
    out = out.sort_values(["ticker", "date"]).reset_index(drop=True)

    return out[
        [
            "date",
            "ticker",
            "adj_close",
            "spy_adj_close",
            "ratio_value",
            "weekly_ratio",
            "has_adj_close",
            "has_ratio",
            "observation_index",
            "valid_ratio_index",
            "current_block_high",
            "current_block_low",
            "prior_block_high",
            "prior_block_low",
            "high_delta",
            "low_delta",
            "direction",
            "classification_ready",
        ]
    ]


def build_classification_summary(classified_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        classified_df.groupby(["ticker", "direction"], dropna=False)
        .agg(row_count=("date", "size"))
        .reset_index()
        .sort_values(["ticker", "direction"])
        .reset_index(drop=True)
    )
    return summary


def build_latest_snapshot(classified_df: pd.DataFrame) -> pd.DataFrame:
    ready_df = classified_df.loc[classified_df["classification_ready"]].copy()
    if ready_df.empty:
        return pd.DataFrame(
            columns=[
                "ticker",
                "date",
                "weekly_ratio",
                "current_block_high",
                "current_block_low",
                "prior_block_high",
                "prior_block_low",
                "high_delta",
                "low_delta",
                "direction",
            ]
        )

    latest = (
        ready_df.sort_values(["ticker", "date"])
        .groupby("ticker", as_index=False)
        .tail(1)
        .sort_values("ticker")
        .reset_index(drop=True)
    )

    return latest[
        [
            "ticker",
            "date",
            "weekly_ratio",
            "current_block_high",
            "current_block_low",
            "prior_block_high",
            "prior_block_low",
            "high_delta",
            "low_delta",
            "direction",
        ]
    ]


def main() -> None:
    args = parse_args()

    if args.block_weeks < 2:
        raise ValueError("block-weeks must be at least 2.")

    input_file = (
        Path(args.input_file).resolve()
        if args.input_file
        else get_default_input_file().resolve()
    )
    out_dir = (
        Path(args.out_dir).resolve()
        if args.out_dir
        else get_default_out_dir().resolve()
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input ratio panel: {input_file}")
    print(f"Output directory: {out_dir}")
    print(f"Weekly rule: {args.weekly_rule}")
    print(f"Block weeks: {args.block_weeks}")

    long_df = load_ratio_panel(input_file)

    weekly_df = build_weekly_ratio_panel(
        long_df=long_df,
        weekly_rule=args.weekly_rule,
    )
    weekly_out_path = out_dir / "historical_weekly_ratio_panel.csv"
    weekly_df.to_csv(weekly_out_path, index=False)

    classified_df = classify_weekly_structure(
        weekly_df=weekly_df,
        block_weeks=args.block_weeks,
    )
    classified_out_path = out_dir / "historical_weekly_structure_classification.csv"
    classified_df.to_csv(classified_out_path, index=False)

    summary_df = build_classification_summary(classified_df)
    summary_out_path = out_dir / "historical_weekly_structure_summary.csv"
    summary_df.to_csv(summary_out_path, index=False)

    latest_df = build_latest_snapshot(classified_df)
    latest_out_path = out_dir / "historical_weekly_structure_latest.csv"
    latest_df.to_csv(latest_out_path, index=False)

    print("\nClassification complete")
    print(f"- Weekly ratio panel: {weekly_out_path}")
    print(f"- Weekly classified panel: {classified_out_path}")
    print(f"- Classification summary: {summary_out_path}")
    print(f"- Latest classified snapshot: {latest_out_path}")
    print(f"- Weekly rows: {len(weekly_df)}")
    print(f"- Classified rows: {len(classified_df)}")

    direction_counts = (
        classified_df["direction"].value_counts(dropna=False).to_dict()
    )
    print(f"- Direction counts: {direction_counts}")

    ready_count = int(classified_df["classification_ready"].sum())
    print(f"- Classification-ready rows: {ready_count}")

    insufficient_count = int((classified_df["direction"] == "INSUFFICIENT_HISTORY").sum())
    no_ratio_count = int((classified_df["direction"] == "NO_RATIO").sum())

    print(f"- Insufficient-history rows: {insufficient_count}")
    print(f"- No-ratio rows: {no_ratio_count}")
    print(
        "Assumption: structural state is defined by comparing the most recent "
        f"{args.block_weeks}-week block to the prior {args.block_weeks}-week block."
    )


if __name__ == "__main__":
    main()