from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_repo_root
from classify_weekly_structure import (
    get_default_input_file,
    build_weekly_ratio_panel,
    classify_weekly_structure,
    build_classification_summary,
    build_latest_snapshot,
    load_ratio_panel,
)


BLOCK_VARIANTS = [3, 4, 6]
VALID_DIRECTIONS = ["HH/HL", "LH/LL", "TRANSITION"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run 3-, 4-, and 6-week sensitivity variants for weekly structure classification."
    )
    parser.add_argument(
        "--input-file",
        default=None,
        help="Optional override for historical_ratio_panel.csv",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help=(
            "Optional override for output directory. "
            "Defaults to cases/market-structure-consistency/outputs/03_analyze/sensitivity"
        ),
    )
    parser.add_argument(
        "--weekly-rule",
        default="W-FRI",
        help="Weekly resample rule. Default: W-FRI",
    )
    return parser.parse_args()


def get_default_out_dir() -> Path:
    return (
        get_repo_root()
        / "cases"
        / "market-structure-consistency"
        / "outputs"
        / "03_analyze"
        / "sensitivity"
    )


def build_direction_share_table(df: pd.DataFrame, block_weeks: int) -> pd.DataFrame:
    ready = df.loc[df["classification_ready"] & df["direction"].isin(VALID_DIRECTIONS)].copy()
    counts = (
        ready["direction"]
        .value_counts()
        .reindex(VALID_DIRECTIONS)
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    counts.columns = ["direction", "count"]
    total = int(counts["count"].sum())
    counts["share_pct"] = (counts["count"] / total * 100.0).round(2) if total > 0 else 0.0
    counts["block_weeks"] = block_weeks
    counts["ready_total"] = total
    return counts[["block_weeks", "direction", "count", "share_pct", "ready_total"]]


def main() -> None:
    args = parse_args()

    input_file = Path(args.input_file).resolve() if args.input_file else get_default_input_file().resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_default_out_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Input ratio panel: {input_file}")
    print(f"Output directory: {out_dir}")
    print(f"Weekly rule: {args.weekly_rule}")

    long_df = load_ratio_panel(input_file)
    weekly_df = build_weekly_ratio_panel(long_df=long_df, weekly_rule=args.weekly_rule)

    all_share_tables = []

    for block_weeks in BLOCK_VARIANTS:
        variant_dir = out_dir / f"block_{block_weeks}w"
        variant_dir.mkdir(parents=True, exist_ok=True)

        classified_df = classify_weekly_structure(weekly_df=weekly_df, block_weeks=block_weeks)
        summary_df = build_classification_summary(classified_df)
        latest_df = build_latest_snapshot(classified_df)
        share_df = build_direction_share_table(classified_df, block_weeks)

        classified_df.to_csv(variant_dir / "historical_weekly_structure_classification.csv", index=False)
        summary_df.to_csv(variant_dir / "historical_weekly_structure_summary.csv", index=False)
        latest_df.to_csv(variant_dir / "historical_weekly_structure_latest.csv", index=False)
        share_df.to_csv(variant_dir / "direction_share_summary.csv", index=False)

        all_share_tables.append(share_df)

        print(f"[done] block={block_weeks}w rows={len(classified_df)} ready={int(classified_df['classification_ready'].sum())}")

    combined = pd.concat(all_share_tables, ignore_index=True)
    combined.to_csv(out_dir / "direction_share_summary_all_variants.csv", index=False)

    pivot = (
        combined.pivot(index="direction", columns="block_weeks", values="share_pct")
        .reset_index()
        .rename(columns={3: "share_pct_3w", 4: "share_pct_4w", 6: "share_pct_6w"})
    )
    pivot.to_csv(out_dir / "direction_share_comparison_pivot.csv", index=False)

    print("\nSensitivity run complete")
    print(f"- Combined share summary: {out_dir / 'direction_share_summary_all_variants.csv'}")
    print(f"- Pivot comparison: {out_dir / 'direction_share_comparison_pivot.csv'}")


if __name__ == "__main__":
    main()