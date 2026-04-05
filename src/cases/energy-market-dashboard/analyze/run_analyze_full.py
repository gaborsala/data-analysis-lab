from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


TICKER_ORDER = ["BZ=F", "CL=F", "NG=F", "SPY", "XLE"]


def annualized_volatility(series: pd.Series, window: int = 20) -> pd.Series:
    returns = series.pct_change()
    return returns.rolling(window=window).std() * np.sqrt(252) * 100


def drawdown_series(series: pd.Series) -> pd.Series:
    running_max = series.cummax()
    return (series / running_max - 1.0) * 100


def normalized_index(series: pd.Series, base: float = 100.0) -> pd.Series:
    first_valid = series.dropna().iloc[0]
    return series / first_valid * base


def save_line_chart(df: pd.DataFrame, title: str, ylabel: str, out_path: Path) -> None:
    plt.figure(figsize=(12, 6))
    for col in df.columns:
        plt.plot(df.index, df[col], label=col)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Date")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main() -> None:
    root = Path(__file__).resolve().parents[4]
    case_dir = root / "cases" / "energy-market-dashboard"
    out_dir = case_dir / "outputs" / "analyze"
    charts_dir = out_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    process_dir = case_dir / "outputs" / "process"
    aligned_path = process_dir / "aligned_panel.csv"
    combined_path = process_dir / "combined_panel.csv"

    if not aligned_path.exists():
        raise FileNotFoundError(f"Missing aligned panel: {aligned_path}")

    if not combined_path.exists():
        raise FileNotFoundError(f"Missing combined panel: {combined_path}")

    aligned = pd.read_csv(aligned_path)
    combined = pd.read_csv(combined_path)

    required_cols = {"date", "ticker", "close", "adj_close"}
    missing_cols = required_cols - set(aligned.columns)
    if missing_cols:
        raise ValueError(f"aligned_panel.csv missing columns: {sorted(missing_cols)}")

    aligned["date"] = pd.to_datetime(aligned["date"], errors="raise")
    combined["date"] = pd.to_datetime(combined["date"], errors="raise")

    aligned = aligned.sort_values(["date", "ticker"]).reset_index(drop=True)

    # Use combined only for diagnostics, not direct comparison outputs
    combined_diagnostics = (
        combined.groupby("ticker", as_index=False)
        .agg(
            rows=("ticker", "size"),
            min_date=("date", "min"),
            max_date=("date", "max"),
        )
        .sort_values("ticker")
        .reset_index(drop=True)
    )
    combined_diagnostics["min_date"] = combined_diagnostics["min_date"].dt.date.astype(str)
    combined_diagnostics["max_date"] = combined_diagnostics["max_date"].dt.date.astype(str)
    combined_diagnostics.to_csv(out_dir / "combined_panel_diagnostics.csv", index=False)

    close_pivot = (
        aligned.pivot(index="date", columns="ticker", values="close")
        .reindex(columns=TICKER_ORDER)
        .sort_index()
    )

    adj_close_pivot = (
        aligned.pivot(index="date", columns="ticker", values="adj_close")
        .reindex(columns=TICKER_ORDER)
        .sort_index()
    )

    normalized_close = close_pivot.apply(normalized_index)
    rolling_vol_20d_close = close_pivot.apply(annualized_volatility, window=20)
    drawdown_close = close_pivot.apply(drawdown_series)

    relative_strength_xle_spy_close = pd.DataFrame(
        {"XLE/SPY": close_pivot["XLE"] / close_pivot["SPY"]}
    )

    analysis_rows = []
    for ticker in TICKER_ORDER:
        s = close_pivot[ticker].dropna()
        vol = rolling_vol_20d_close[ticker].dropna()
        dd = drawdown_close[ticker].dropna()

        total_return_pct = (s.iloc[-1] / s.iloc[0] - 1.0) * 100
        normalized_end_index = normalized_close[ticker].dropna().iloc[-1]
        last_20d_ann_vol_pct = vol.iloc[-1] if not vol.empty else np.nan
        max_drawdown_pct = dd.min() if not dd.empty else np.nan

        analysis_rows.append(
            {
                "ticker": ticker,
                "start_date": s.index.min().date().isoformat(),
                "end_date": s.index.max().date().isoformat(),
                "aligned_obs": len(s),
                "start_price": round(float(s.iloc[0]), 6),
                "end_price": round(float(s.iloc[-1]), 6),
                "normalized_end_index": round(float(normalized_end_index), 6),
                "total_return_pct": round(float(total_return_pct), 6),
                "last_20d_ann_vol_pct": round(float(last_20d_ann_vol_pct), 6),
                "max_drawdown_pct": round(float(max_drawdown_pct), 6),
            }
        )

    analysis_summary_close = pd.DataFrame(analysis_rows)
    analysis_summary_close.to_csv(out_dir / "analysis_summary_close.csv", index=False)

    comparison_rows = []
    for ticker in TICKER_ORDER:
        c = close_pivot[ticker].dropna()
        a = adj_close_pivot[ticker].dropna()

        close_total_return_pct = (c.iloc[-1] / c.iloc[0] - 1.0) * 100
        adj_close_total_return_pct = (a.iloc[-1] / a.iloc[0] - 1.0) * 100

        comparison_rows.append(
            {
                "ticker": ticker,
                "close_start": round(float(c.iloc[0]), 6),
                "close_end": round(float(c.iloc[-1]), 6),
                "close_total_return_pct": round(float(close_total_return_pct), 6),
                "adj_close_start": round(float(a.iloc[0]), 6),
                "adj_close_end": round(float(a.iloc[-1]), 6),
                "adj_close_total_return_pct": round(float(adj_close_total_return_pct), 6),
                "return_diff_pct_points": round(
                    float(adj_close_total_return_pct - close_total_return_pct), 6
                ),
            }
        )

    close_vs_adjclose_comparison = pd.DataFrame(comparison_rows)
    close_vs_adjclose_comparison.to_csv(
        out_dir / "close_vs_adjclose_comparison.csv", index=False
    )

    normalized_close.to_csv(out_dir / "normalized_performance_close.csv")
    rolling_vol_20d_close.to_csv(out_dir / "rolling_volatility_20d_close.csv")
    drawdown_close.to_csv(out_dir / "drawdown_close.csv")
    relative_strength_xle_spy_close.to_csv(out_dir / "relative_strength_xle_vs_spy_close.csv")

    save_line_chart(
        normalized_close,
        title="Normalized Performance (Close Basis)",
        ylabel="Index (Base = 100)",
        out_path=charts_dir / "normalized_performance_close.png",
    )

    save_line_chart(
        rolling_vol_20d_close,
        title="Rolling 20-Day Annualized Volatility (Close Basis)",
        ylabel="Annualized Volatility (%)",
        out_path=charts_dir / "rolling_volatility_20d_close.png",
    )

    save_line_chart(
        drawdown_close,
        title="Drawdown (Close Basis)",
        ylabel="Drawdown (%)",
        out_path=charts_dir / "drawdown_close.png",
    )

    save_line_chart(
        relative_strength_xle_spy_close,
        title="Relative Strength: XLE / SPY (Close Basis)",
        ylabel="Ratio",
        out_path=charts_dir / "relative_strength_xle_vs_spy_close.png",
    )

    print("Saved:")
    print(f"  {out_dir / 'analysis_summary_close.csv'}")
    print(f"  {out_dir / 'close_vs_adjclose_comparison.csv'}")
    print(f"  {out_dir / 'normalized_performance_close.csv'}")
    print(f"  {out_dir / 'rolling_volatility_20d_close.csv'}")
    print(f"  {out_dir / 'drawdown_close.csv'}")
    print(f"  {out_dir / 'relative_strength_xle_vs_spy_close.csv'}")
    print(f"  {out_dir / 'combined_panel_diagnostics.csv'}")
    print(f"  {charts_dir / 'normalized_performance_close.png'}")
    print(f"  {charts_dir / 'rolling_volatility_20d_close.png'}")
    print(f"  {charts_dir / 'drawdown_close.png'}")
    print(f"  {charts_dir / 'relative_strength_xle_vs_spy_close.png'}")


if __name__ == "__main__":
    main()