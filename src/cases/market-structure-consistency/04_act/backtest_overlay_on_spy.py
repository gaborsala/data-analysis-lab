from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_repo_root


VALID_DIRECTIONS = {"HH/HL", "LH/LL", "TRANSITION"}
DEFAULT_STARTING_CAPITAL = 1.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Backtest a simple market-structure overlay on SPY. "
            "Baseline = always long SPY. "
            "Overlay = long SPY only when weekly direction == HH/HL; otherwise flat."
        )
    )
    parser.add_argument(
        "--spy-file",
        default=None,
        help="Optional override for SPY raw daily CSV. Defaults to data/raw/SPY.csv",
    )
    parser.add_argument(
        "--classification-file",
        default=None,
        help=(
            "Optional override for weekly classification CSV. "
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
    parser.add_argument(
        "--starting-capital",
        type=float,
        default=DEFAULT_STARTING_CAPITAL,
        help="Initial equity value for both curves. Default: 1.0",
    )
    return parser.parse_args()


def get_default_spy_file() -> Path:
    return get_repo_root() / "data" / "raw" / "SPY.csv"


def get_default_classification_file() -> Path:
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


def load_spy_daily(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"SPY raw file not found: {path}")

    df = pd.read_csv(path)
    required = {"Date", "Adj Close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"SPY file missing required columns: {sorted(missing)}")

    df = df[["Date", "Adj Close"]].copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Adj Close"] = pd.to_numeric(df["Adj Close"], errors="coerce")

    bad_dates = int(df["Date"].isna().sum())
    bad_prices = int(df["Adj Close"].isna().sum())
    duplicate_dates = int(df["Date"].duplicated().sum())

    if bad_dates > 0:
        raise ValueError(f"SPY file contains {bad_dates} invalid dates.")
    if bad_prices > 0:
        raise ValueError(f"SPY file contains {bad_prices} invalid adjusted close values.")
    if duplicate_dates > 0:
        raise ValueError(f"SPY file contains {duplicate_dates} duplicate dates.")

    non_positive = int((df["Adj Close"] <= 0).sum())
    if non_positive > 0:
        raise ValueError(f"SPY file contains {non_positive} non-positive adjusted close values.")

    df = df.sort_values("Date").reset_index(drop=True)
    df = df.rename(columns={"Date": "date", "Adj Close": "spy_adj_close"})
    return df


def load_weekly_classification(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Classification file not found: {path}")

    df = pd.read_csv(path)
    required = {"date", "ticker", "direction", "classification_ready"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Classification file missing required columns: {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    bad_dates = int(df["date"].isna().sum())
    if bad_dates > 0:
        raise ValueError(f"Classification file contains {bad_dates} invalid dates.")

    df["classification_ready"] = df["classification_ready"].astype(bool)

    spy_like = df.loc[df["ticker"] == "SPY"]
    if not spy_like.empty:
        raise ValueError("Classification file should contain sector rows only, not SPY rows.")

    return df.sort_values(["ticker", "date"]).reset_index(drop=True)


def build_market_regime_from_sectors(classified_df: pd.DataFrame) -> pd.DataFrame:
    ready = classified_df.loc[
        classified_df["classification_ready"] & classified_df["direction"].isin(VALID_DIRECTIONS)
    ].copy()

    if ready.empty:
        raise ValueError("No classification-ready sector rows found.")

    regime = (
        ready.groupby("date")
        .agg(
            hh_hl_count=("direction", lambda s: int((s == "HH/HL").sum())),
            lh_ll_count=("direction", lambda s: int((s == "LH/LL").sum())),
            transition_count=("direction", lambda s: int((s == "TRANSITION").sum())),
            sector_count=("ticker", "nunique"),
        )
        .reset_index()
        .sort_values("date")
        .reset_index(drop=True)
    )

    def decide_direction(row: pd.Series) -> str:
        if row["hh_hl_count"] > row["lh_ll_count"]:
            return "HH/HL"
        if row["lh_ll_count"] > row["hh_hl_count"]:
            return "LH/LL"
        return "TRANSITION"

    regime["overlay_direction"] = regime.apply(decide_direction, axis=1)
    regime["is_long_allowed"] = regime["overlay_direction"].eq("HH/HL")
    return regime


def merge_daily_with_weekly_signal(
    spy_daily: pd.DataFrame,
    weekly_regime: pd.DataFrame,
) -> pd.DataFrame:
    daily = spy_daily.copy().sort_values("date").reset_index(drop=True)
    weekly = weekly_regime[
        [
            "date",
            "overlay_direction",
            "is_long_allowed",
            "hh_hl_count",
            "lh_ll_count",
            "transition_count",
            "sector_count",
        ]
    ].copy().sort_values("date")

    merged = pd.merge_asof(
        daily,
        weekly,
        on="date",
        direction="backward",
    )

    merged["daily_return"] = merged["spy_adj_close"].pct_change().fillna(0.0)

    # Position is applied starting the day after a weekly signal becomes known.
    merged["overlay_position"] = merged["is_long_allowed"].fillna(False).astype(int).shift(1).fillna(0).astype(int)
    merged["baseline_position"] = 1

    merged["baseline_strategy_return"] = merged["daily_return"] * merged["baseline_position"]
    merged["overlay_strategy_return"] = merged["daily_return"] * merged["overlay_position"]

    return merged


def compute_equity_curves(
    df: pd.DataFrame,
    starting_capital: float,
) -> pd.DataFrame:
    out = df.copy()
    out["baseline_equity"] = (1.0 + out["baseline_strategy_return"]).cumprod() * starting_capital
    out["overlay_equity"] = (1.0 + out["overlay_strategy_return"]).cumprod() * starting_capital
    return out


def max_drawdown(equity: pd.Series) -> float:
    running_max = equity.cummax()
    dd = equity / running_max - 1.0
    return float(dd.min())


def annualized_return(equity: pd.Series, periods: int) -> float:
    if periods <= 1:
        return 0.0
    total_return = float(equity.iloc[-1] / equity.iloc[0])
    years = periods / 252.0
    if years <= 0:
        return 0.0
    return total_return ** (1.0 / years) - 1.0


def annualized_volatility(returns: pd.Series) -> float:
    if len(returns) <= 1:
        return 0.0
    return float(returns.std(ddof=1) * (252.0 ** 0.5))


def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for label, ret_col, eq_col, pos_col in [
        ("baseline_always_long_spy", "baseline_strategy_return", "baseline_equity", "baseline_position"),
        ("overlay_long_only_when_market_hh_hl", "overlay_strategy_return", "overlay_equity", "overlay_position"),
    ]:
        invested_days = int(df[pos_col].sum())
        total_days = int(len(df))
        pct_invested = invested_days / total_days * 100.0 if total_days > 0 else 0.0

        rows.append(
            {
                "strategy": label,
                "start_date": df["date"].min().strftime("%Y-%m-%d"),
                "end_date": df["date"].max().strftime("%Y-%m-%d"),
                "trading_days": total_days,
                "invested_days": invested_days,
                "invested_share_pct": round(pct_invested, 2),
                "final_equity": round(float(df[eq_col].iloc[-1]), 6),
                "total_return_pct": round((float(df[eq_col].iloc[-1]) / float(df[eq_col].iloc[0]) - 1.0) * 100.0, 2),
                "annualized_return_pct": round(annualized_return(df[eq_col], total_days) * 100.0, 2),
                "annualized_volatility_pct": round(annualized_volatility(df[ret_col]) * 100.0, 2),
                "max_drawdown_pct": round(max_drawdown(df[eq_col]) * 100.0, 2),
            }
        )

    return pd.DataFrame(rows)


def build_overlay_regime_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby("overlay_direction", dropna=False)
        .agg(
            day_count=("date", "size"),
            avg_hh_hl_count=("hh_hl_count", "mean"),
            avg_lh_ll_count=("lh_ll_count", "mean"),
            avg_transition_count=("transition_count", "mean"),
        )
        .reset_index()
        .sort_values("overlay_direction", na_position="last")
        .reset_index(drop=True)
    )
    return summary


def main() -> None:
    args = parse_args()

    spy_file = Path(args.spy_file).resolve() if args.spy_file else get_default_spy_file().resolve()
    classification_file = (
        Path(args.classification_file).resolve()
        if args.classification_file
        else get_default_classification_file().resolve()
    )
    out_dir = Path(args.out_dir).resolve() if args.out_dir else get_default_out_dir().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"SPY file: {spy_file}")
    print(f"Classification file: {classification_file}")
    print(f"Output directory: {out_dir}")

    spy_daily = load_spy_daily(spy_file)
    classified = load_weekly_classification(classification_file)
    weekly_regime = build_market_regime_from_sectors(classified)

    merged = merge_daily_with_weekly_signal(spy_daily, weekly_regime)
    equity_df = compute_equity_curves(merged, starting_capital=args.starting_capital)

    detail_path = out_dir / "spy_overlay_backtest_daily.csv"
    regime_path = out_dir / "spy_overlay_weekly_market_regime.csv"
    summary_path = out_dir / "spy_overlay_backtest_summary.csv"
    overlay_regime_summary_path = out_dir / "spy_overlay_regime_summary.csv"

    equity_df.to_csv(detail_path, index=False)
    weekly_regime.to_csv(regime_path, index=False)

    summary_df = build_summary_table(equity_df)
    summary_df.to_csv(summary_path, index=False)

    regime_summary_df = build_overlay_regime_summary(equity_df.dropna(subset=["overlay_direction"]))
    regime_summary_df.to_csv(overlay_regime_summary_path, index=False)

    print("\nBacktest complete")
    print(f"- Daily backtest detail: {detail_path}")
    print(f"- Weekly market regime: {regime_path}")
    print(f"- Summary: {summary_path}")
    print(f"- Overlay regime summary: {overlay_regime_summary_path}")
    print("\nSummary table:")
    print(summary_df.to_string(index=False))

    print("\nAssumptions:")
    print("- Baseline is always-long SPY")
    print("- Overlay is long SPY only when sector-majority weekly regime is HH/HL")
    print("- Weekly signal is applied with a 1-day lag to avoid same-day lookahead")
    print("- No transaction costs or slippage are included")


if __name__ == "__main__":
    main()