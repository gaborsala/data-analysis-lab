from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st


APP_TITLE = "Energy Market Dashboard — V1"
APP_CAPTION = (
    "Descriptive, non-forecasting dashboard built from the aligned daily panel. "
    "Metric basis is fixed to close for mixed-asset consistency."
)

TICKER_ORDER = ["BZ=F", "CL=F", "NG=F", "SPY", "XLE"]
TICKER_LABELS = {
    "BZ=F": "Brent",
    "CL=F": "WTI",
    "NG=F": "Natural Gas",
    "SPY": "SPY",
    "XLE": "XLE",
}


def resolve_case_root() -> Path:
    """
    Resolve the case root from:
    cases/energy-market-dashboard/app/app.py
    """
    return Path(__file__).resolve().parents[1]


def resolve_paths(case_root: Path) -> dict[str, Path]:
    outputs_root = case_root / "outputs"
    process_dir = outputs_root / "process"
    analyze_dir = outputs_root / "analyze"

    return {
        "aligned_panel": process_dir / "aligned_panel.csv",
        "analysis_summary": analyze_dir / "analysis_summary_close.csv",
        "close_vs_adjclose": analyze_dir / "close_vs_adjclose_comparison.csv",
        "normalized": analyze_dir / "normalized_performance_close.csv",
        "rolling_vol": analyze_dir / "rolling_volatility_20d_close.csv",
        "drawdown": analyze_dir / "drawdown_close.csv",
        "relative_strength": analyze_dir / "relative_strength_xle_vs_spy_close.csv",
    }


def validate_required_files(paths: dict[str, Path]) -> list[str]:
    missing = []
    for name, path in paths.items():
        if not path.exists():
            missing.append(f"{name}: {path}")
    return missing


@st.cache_data(show_spinner=False)
def load_csv(path: Path, parse_dates: list[str] | None = None) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=parse_dates)


def validate_aligned_panel(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []

    required_cols = {"date", "ticker", "close", "adj_close"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        errors.append(f"aligned_panel.csv missing columns: {sorted(missing_cols)}")

    if "date" in df.columns and "ticker" in df.columns:
        dup_count = int(df.duplicated(subset=["date", "ticker"]).sum())
        if dup_count > 0:
            errors.append(f"aligned_panel.csv has {dup_count} duplicate (date, ticker) rows")

    if "ticker" in df.columns:
        observed = sorted(df["ticker"].dropna().unique().tolist())
        expected = sorted(TICKER_ORDER)
        if observed != expected:
            errors.append(f"Ticker set mismatch. Expected {expected}, found {observed}")

    return errors


def prepare_line_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce")
        out = out.sort_values("date")
        out = out.set_index("date")

    ordered_cols = [c for c in TICKER_ORDER if c in out.columns]
    out = out[ordered_cols]
    out = out.rename(columns=TICKER_LABELS)

    return out


def prepare_relative_strength_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce")
        out = out.sort_values("date")
        out = out.set_index("date")

    return out.rename(columns={"XLE/SPY": "XLE / SPY"})


def build_sidebar(paths: dict[str, Path], aligned_panel: pd.DataFrame) -> None:
    st.sidebar.header("Scope")
    st.sidebar.write("Dataset: aligned panel only")
    st.sidebar.write("Metric basis: close")
    st.sidebar.write("Panels: 4")
    st.sidebar.write("Forecasting: excluded")
    st.sidebar.write("Causal claims: excluded")

    st.sidebar.header("Source files")
    st.sidebar.code(
        "\n".join(
            [
                str(paths["aligned_panel"]),
                str(paths["normalized"]),
                str(paths["rolling_vol"]),
                str(paths["drawdown"]),
                str(paths["relative_strength"]),
            ]
        ),
        language="text",
    )

    if not aligned_panel.empty:
        st.sidebar.header("Aligned panel facts")
        st.sidebar.write(f"Rows: {len(aligned_panel):,}")
        st.sidebar.write(f"Tickers: {aligned_panel['ticker'].nunique()}")
        st.sidebar.write(f"Start: {aligned_panel['date'].min().date()}")
        st.sidebar.write(f"End: {aligned_panel['date'].max().date()}")


def render_header(
    summary_df: pd.DataFrame,
    aligned_panel: pd.DataFrame,
    close_vs_adjclose_df: pd.DataFrame,
) -> None:
    st.title(APP_TITLE)
    st.caption(APP_CAPTION)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aligned dates", f"{aligned_panel['date'].nunique():,}")
    col2.metric("Tickers", f"{aligned_panel['ticker'].nunique()}")
    col3.metric("Metric basis", "close")
    col4.metric("V1 panels", "4")

    st.markdown(
        """
        **Method note:** This dashboard uses the aligned panel only.  
        `combined_panel.csv` is intentionally excluded from direct cross-instrument comparison and should be used only for diagnostics.
        """
    )

    if not close_vs_adjclose_df.empty:
        etf_rows = close_vs_adjclose_df[
            close_vs_adjclose_df["ticker"].isin(["SPY", "XLE"])
        ].copy()
        if not etf_rows.empty:
            st.info(
                "Metric basis is fixed to `close` because this is a mixed-asset dashboard "
                "(futures + ETFs). `adj_close` differs materially for ETFs and can be added later as an ETF-only mode."
            )

    if not summary_df.empty:
        st.subheader("Summary table")
        summary_view = summary_df.copy()
        summary_view["ticker"] = summary_view["ticker"].map(TICKER_LABELS).fillna(summary_view["ticker"])
        st.dataframe(summary_view, width="stretch", hide_index=True)


def render_panel(title: str, description: str, df: pd.DataFrame, y_label_hint: str) -> None:
    st.subheader(title)
    st.write(description)

    if df.empty or df.shape[1] == 0:
        st.warning("No data available for this panel.")
        return

    st.line_chart(df, width="stretch")
    st.caption(f"Display basis: {y_label_hint}")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")

    case_root = resolve_case_root()
    paths = resolve_paths(case_root)

    missing_files = validate_required_files(paths)
    if missing_files:
        st.error("Required dashboard inputs are missing.")
        st.code("\n".join(missing_files), language="text")
        st.stop()

    aligned_panel = load_csv(paths["aligned_panel"], parse_dates=["date"])
    summary_df = load_csv(paths["analysis_summary"])
    close_vs_adjclose_df = load_csv(paths["close_vs_adjclose"])
    normalized_df = load_csv(paths["normalized"], parse_dates=["date"])
    rolling_vol_df = load_csv(paths["rolling_vol"], parse_dates=["date"])
    drawdown_df = load_csv(paths["drawdown"], parse_dates=["date"])
    relative_strength_df = load_csv(paths["relative_strength"], parse_dates=["date"])

    validation_errors = validate_aligned_panel(aligned_panel)
    if validation_errors:
        st.error("Aligned panel validation failed.")
        st.code("\n".join(validation_errors), language="text")
        st.stop()

    build_sidebar(paths, aligned_panel)
    render_header(summary_df, aligned_panel, close_vs_adjclose_df)

    normalized_plot = prepare_line_df(normalized_df)
    rolling_vol_plot = prepare_line_df(rolling_vol_df)
    drawdown_plot = prepare_line_df(drawdown_df)
    relative_strength_plot = prepare_relative_strength_df(relative_strength_df)

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Normalized Performance",
            "Rolling Volatility",
            "Drawdown",
            "XLE / SPY Relative Strength",
        ]
    )

    with tab1:
        render_panel(
            title="Normalized Performance (Close Basis)",
            description=(
                "Compares path-level market behavior from a common base. "
                "This is the primary comparative performance view for V1."
            ),
            df=normalized_plot,
            y_label_hint="Index, base = 100",
        )

    with tab2:
        render_panel(
            title="Rolling 20-Day Annualized Volatility (Close Basis)",
            description=(
                "Shows short-horizon risk-state differences across instruments using the 20-day rolling annualized volatility series."
            ),
            df=rolling_vol_plot,
            y_label_hint="Annualized volatility (%)",
        )

    with tab3:
        render_panel(
            title="Drawdown (Close Basis)",
            description=(
                "Shows downside depth and recovery structure relative to each instrument's running peak."
            ),
            df=drawdown_plot,
            y_label_hint="Drawdown (%)",
        )

    with tab4:
        render_panel(
            title="Relative Strength: XLE / SPY (Close Basis)",
            description=(
                "Benchmark-relative energy sector view. Higher values indicate stronger XLE performance relative to SPY."
            ),
            df=relative_strength_plot,
            y_label_hint="Price ratio",
        )

    with st.expander("Validation and governance notes"):
        st.markdown(
            """
            - Primary analytical dataset: `cases/energy-market-dashboard/outputs/process/aligned_panel.csv`
            - Combined panel is excluded from direct comparison views
            - Metric basis is fixed to `close`
            - This dashboard is descriptive only
            - Forecasting, macro overlays, sentiment layers, and cross-asset volume panels are intentionally excluded from V1
            """
        )

    with st.expander("Assumptions and limitations"):
        st.markdown(
            """
            **Assumptions**
            - The aligned panel remains the correct base dataset for cross-instrument comparison.
            - `close` remains the correct V1 metric basis for mixed-asset comparison.
            - The four selected panels are sufficient for the first production version.

            **Limitations**
            - The dataset mixes futures and ETFs, so interpretation must remain descriptive.
            - This dashboard does not support causal claims or forecasting.
            - Volatility and drawdown are window- and path-dependent metrics.
            """
        )


if __name__ == "__main__":
    main()