"""
Common utilities for ANALYZE stage:
Hungarian Inflation Bond vs Alternatives

Purpose
-------
Provide deterministic, reusable functions for:
- loading PROCESS outputs
- validating required columns
- handling full-history vs common-window modes
- computing monthly returns
- computing rolling 12-month returns
- computing threshold exceedance rates
- computing annualized volatility and max drawdown
- writing outputs reproducibly

Assumptions
-----------
1. PROCESS outputs already removed pre-inception null padding.
2. Active-window internal ETF nulls are zero, as documented in PROCESS.
3. Monthly alignment is performed on a `year_month` field or derivable monthly date field.
4. Price-like fields are available for ETF series, or monthly returns are already present.
5. Bond threshold fields were normalized in PROCESS.

Limitations
-----------
1. This module does not decide the final benchmark interpretation; it only helps surface it.
2. Column name inference is best-effort and may require adjustment to actual PROCESS output names.
3. Full-history and common-window logic are descriptive, not predictive.
4. Historical threshold exceedance is not a future guarantee.

Validation checks implemented
-----------------------------
- input path existence
- required column presence
- month ordering before rolling calculations
- minimum observations for rolling windows
- common-window date derivation across tickers
- finite-result checks on summary outputs
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence

import math
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

FULL_HISTORY = "full-history"
COMMON_WINDOW = "common-window"
VALID_MODES = {FULL_HISTORY, COMMON_WINDOW}


# ---------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class AnalyzePaths:
    project_root: Path
    process_dir: Path
    analyze_dir: Path
    outputs_tables_dir: Path
    outputs_charts_dir: Path
    outputs_logs_dir: Path


def build_analyze_paths(
    project_root: str | Path,
    process_dir: str | Path = "02_PROCESS/outputs",
    analyze_dir: str | Path = "03_ANALYZE",
) -> AnalyzePaths:
    """
    Build standard ANALYZE directory paths.

    Parameters
    ----------
    project_root : str | Path
        Repo or case-study root.
    process_dir : str | Path
        Relative path to PROCESS outputs.
    analyze_dir : str | Path
        Relative path to ANALYZE stage root.

    Returns
    -------
    AnalyzePaths
    """
    project_root = Path(project_root)
    process_dir = project_root / Path(process_dir)
    analyze_dir = project_root / Path(analyze_dir)

    return AnalyzePaths(
        project_root=project_root,
        process_dir=process_dir,
        analyze_dir=analyze_dir,
        outputs_tables_dir=analyze_dir / "outputs" / "tables",
        outputs_charts_dir=analyze_dir / "outputs" / "charts",
        outputs_logs_dir=analyze_dir / "outputs" / "logs",
    )


def ensure_output_dirs(paths: AnalyzePaths) -> None:
    """Create ANALYZE output directories if missing."""
    for p in (
        paths.analyze_dir,
        paths.outputs_tables_dir,
        paths.outputs_charts_dir,
        paths.outputs_logs_dir,
    ):
        p.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Generic I/O
# ---------------------------------------------------------------------

def load_table(path: str | Path) -> pd.DataFrame:
    """
    Load a table from CSV or Parquet.

    Raises
    ------
    FileNotFoundError
        If file does not exist.
    ValueError
        If extension unsupported.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)

    raise ValueError(f"Unsupported file format: {path.suffix}")


def write_table(df: pd.DataFrame, path: str | Path, index: bool = False) -> None:
    """Write DataFrame to CSV, ensuring parent dirs exist."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)


def write_text(text: str, path: str | Path) -> None:
    """Write plain text to file, ensuring parent dirs exist."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------
# Column helpers
# ---------------------------------------------------------------------

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy with normalized snake_case-ish column names.
    """
    out = df.copy()
    out.columns = [
        str(c)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("%", "pct")
        for c in out.columns
    ]
    return out


def first_existing_column(df: pd.DataFrame, candidates: Sequence[str]) -> str:
    """
    Return the first column from candidates that exists in df.
    """
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f"None of the candidate columns exist: {list(candidates)}")


def validate_required_columns(df: pd.DataFrame, required: Sequence[str], df_name: str) -> None:
    """
    Validate required columns exist.
    """
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{df_name} missing required columns: {missing}")


def infer_date_column(df: pd.DataFrame) -> str:
    """
    Infer a monthly/date column from common candidates.
    """
    candidates = [
        "year_month",
        "date",
        "month",
        "month_end",
        "month_date",
        "period_end",
        "as_of_date",
    ]
    return first_existing_column(df, candidates)


def infer_ticker_column(df: pd.DataFrame) -> str:
    """
    Infer a ticker/asset column from common candidates.
    """
    candidates = ["ticker", "symbol", "asset", "series", "etf", "instrument"]
    return first_existing_column(df, candidates)


def infer_price_column(df: pd.DataFrame) -> str:
    """
    Infer a price-like column from common candidates.
    """
    candidates = [
        "adj_close",
        "adjusted_close",
        "close",
        "close_month_end",
        "monthly_close",
        "price",
        "last_close",
        "month_end_close",
        "etf_close",
    ]
    return first_existing_column(df, candidates)

def infer_return_column(df: pd.DataFrame) -> str:
    """
    Infer a return column from common candidates.
    """
    candidates = [
        "monthly_return",
        "return",
        "ret",
        "pct_return",
        "return_pct",
        "monthly_pct_return",
    ]
    return first_existing_column(df, candidates)


def infer_benchmark_column(df: pd.DataFrame) -> str:
    """
    Infer a benchmark threshold column from likely PROCESS outputs.

    Notes
    -----
    This is intentionally best-effort. If no candidate is found,
    downstream scripts should override explicitly.
    """
    candidates = [
        "bond_threshold_pct_point",
        "bond_threshold_pct",
        "annual_benchmark_pct",
        "benchmark_pct",
        "bond_hurdle_pct",
        "bond_net_threshold_pct",
        "normalized_bond_threshold_pct",
        "real_return_threshold_pct",
    ]
    return first_existing_column(df, candidates)


# ---------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------

def to_month_end_timestamp(series: pd.Series) -> pd.Series:
    """
    Convert a date-like or year_month series to month-end Timestamp.
    """
    parsed = pd.to_datetime(series, errors="coerce")
    if parsed.notna().all():
        return parsed.dt.to_period("M").dt.to_timestamp("M")

    # Try explicit YYYY-MM handling
    text = series.astype(str).str.strip()
    parsed = pd.to_datetime(text + "-01", errors="coerce")
    if parsed.notna().all():
        return parsed.dt.to_period("M").dt.to_timestamp("M")

    raise ValueError("Could not convert series to month-end timestamps.")


def add_month_end_column(
    df: pd.DataFrame,
    source_date_col: Optional[str] = None,
    out_col: str = "month_end",
) -> pd.DataFrame:
    """
    Add a month_end Timestamp column.
    """
    out = df.copy()
    if source_date_col is None:
        source_date_col = infer_date_column(out)

    out[out_col] = to_month_end_timestamp(out[source_date_col])
    return out


# ---------------------------------------------------------------------
# Window selection
# ---------------------------------------------------------------------

def get_ticker_coverage_summary(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
) -> pd.DataFrame:
    """
    Build start/end/observation coverage summary by ticker.
    """
    if ticker_col is None:
        ticker_col = infer_ticker_column(df)

    validate_required_columns(df, [ticker_col, date_col], "coverage_df")

    coverage = (
        df.groupby(ticker_col, dropna=False)[date_col]
        .agg(start_date="min", end_date="max", n_obs="count")
        .reset_index()
        .sort_values([ticker_col])
    )
    return coverage


def get_common_window_bounds(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
) -> tuple[pd.Timestamp, pd.Timestamp]:
    """
    Derive overlapping date window across all tickers.
    """
    coverage = get_ticker_coverage_summary(df, ticker_col=ticker_col, date_col=date_col)

    common_start = coverage["start_date"].max()
    common_end = coverage["end_date"].min()

    if common_start > common_end:
        raise ValueError(
            f"No overlapping common window found. common_start={common_start}, common_end={common_end}"
        )

    return common_start, common_end


def apply_window_mode(
    df: pd.DataFrame,
    mode: str,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
) -> pd.DataFrame:
    """
    Apply either full-history or common-window filter.

    Parameters
    ----------
    df : pd.DataFrame
        Input monthly panel.
    mode : str
        'full-history' or 'common-window'
    """
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode '{mode}'. Valid modes: {sorted(VALID_MODES)}")

    if mode == FULL_HISTORY:
        return df.copy()

    common_start, common_end = get_common_window_bounds(
        df, ticker_col=ticker_col, date_col=date_col
    )

    out = df[(df[date_col] >= common_start) & (df[date_col] <= common_end)].copy()
    return out


# ---------------------------------------------------------------------
# Return calculations
# ---------------------------------------------------------------------

def compute_monthly_returns_from_price(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
    price_col: Optional[str] = None,
    out_col: str = "monthly_return",
) -> pd.DataFrame:
    """
    Compute simple monthly returns from price by ticker.
    """
    out = df.copy()
    if ticker_col is None:
        ticker_col = infer_ticker_column(out)
    if price_col is None:
        price_col = infer_price_column(out)

    validate_required_columns(out, [ticker_col, date_col, price_col], "price_df")

    out = out.sort_values([ticker_col, date_col]).copy()
    out[out_col] = out.groupby(ticker_col, dropna=False)[price_col].pct_change()

    return out


def validate_monotonic_month_order(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
) -> None:
    """
    Validate date order per ticker is monotonic non-decreasing.
    """
    if ticker_col is None:
        ticker_col = infer_ticker_column(df)

    for ticker, grp in df.groupby(ticker_col, dropna=False):
        if not grp[date_col].is_monotonic_increasing:
            raise ValueError(f"Date order is not monotonic for ticker={ticker}")


def compute_rolling_12m_returns(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
    return_col: Optional[str] = None,
    out_col: str = "rolling_12m_return",
    min_periods: int = 12,
) -> pd.DataFrame:
    """
    Compute trailing 12-month compounded returns from monthly returns.

    Formula
    -------
    rolling_12m_return = prod(1 + r_t over trailing 12 months) - 1

    Notes
    -----
    - Requires monthly return series.
    - Uses full 12-month windows by default.
    """
    out = df.copy()
    if ticker_col is None:
        ticker_col = infer_ticker_column(out)
    if return_col is None:
        return_col = infer_return_column(out)

    validate_required_columns(out, [ticker_col, date_col, return_col], "returns_df")
    out = out.sort_values([ticker_col, date_col]).copy()
    validate_monotonic_month_order(out, ticker_col=ticker_col, date_col=date_col)

    def _rolling_compound(s: pd.Series) -> pd.Series:
        gross = (1.0 + s.astype(float))
        return gross.rolling(window=12, min_periods=min_periods).apply(np.prod, raw=True) - 1.0

    out[out_col] = (
        out.groupby(ticker_col, dropna=False)[return_col]
        .transform(_rolling_compound)
    )

    return out


def summarize_rolling_returns(
    df: pd.DataFrame,
    mode: str,
    ticker_col: Optional[str] = None,
    rolling_col: str = "rolling_12m_return",
) -> pd.DataFrame:
    """
    Summarize rolling 12-month return distribution by ticker.
    """
    if ticker_col is None:
        ticker_col = infer_ticker_column(df)

    validate_required_columns(df, [ticker_col, rolling_col], "rolling_returns_df")

    valid = df[df[rolling_col].notna()].copy()

    summary = (
        valid.groupby(ticker_col, dropna=False)[rolling_col]
        .agg(
            valid_windows="count",
            mean_rolling_12m_return="mean",
            median_rolling_12m_return="median",
            min_rolling_12m_return="min",
            max_rolling_12m_return="max",
        )
        .reset_index()
    )
    summary["mode"] = mode
    return summary[[ticker_col, "mode", "valid_windows",
                    "mean_rolling_12m_return", "median_rolling_12m_return",
                    "min_rolling_12m_return", "max_rolling_12m_return"]]


# ---------------------------------------------------------------------
# Threshold logic
# ---------------------------------------------------------------------

def add_constant_threshold(
    df: pd.DataFrame,
    threshold_value: float,
    out_col: str = "benchmark_threshold",
) -> pd.DataFrame:
    """
    Add constant annual threshold column.

    Parameters
    ----------
    threshold_value : float
        Decimal form, e.g. 0.05 for 5%.
    """
    out = df.copy()
    out[out_col] = float(threshold_value)
    return out


def compute_threshold_exceedance(
    df: pd.DataFrame,
    mode: str,
    threshold_col: str,
    ticker_col: Optional[str] = None,
    rolling_col: str = "rolling_12m_return",
) -> pd.DataFrame:
    """
    Compute threshold exceedance counts and rates by ticker.

    Returns
    -------
    pd.DataFrame
        Columns:
        - ticker
        - mode
        - threshold
        - windows_above_threshold
        - total_valid_windows
        - exceedance_rate
    """
    if ticker_col is None:
        ticker_col = infer_ticker_column(df)

    validate_required_columns(df, [ticker_col, rolling_col, threshold_col], "threshold_df")

    valid = df[df[rolling_col].notna() & df[threshold_col].notna()].copy()
    valid["above_threshold"] = valid[rolling_col] > valid[threshold_col]

    grouped = (
        valid.groupby(ticker_col, dropna=False)
        .agg(
            threshold=(threshold_col, "median"),
            windows_above_threshold=("above_threshold", "sum"),
            total_valid_windows=("above_threshold", "count"),
        )
        .reset_index()
    )
    grouped["exceedance_rate"] = (
        grouped["windows_above_threshold"] / grouped["total_valid_windows"]
    )
    grouped["mode"] = mode

    return grouped[[ticker_col, "mode", "threshold",
                    "windows_above_threshold", "total_valid_windows", "exceedance_rate"]]


def build_benchmark_definition_check(
    df: pd.DataFrame,
    benchmark_candidates: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    """
    Surface benchmark candidate columns with completeness and basic stats.

    Purpose
    -------
    Helps verify which normalized bond threshold field should be used
    before final interpretation.

    Returns
    -------
    pd.DataFrame
    """
    if benchmark_candidates is None:
        benchmark_candidates = [
            "bond_threshold_pct_point",
            "bond_threshold_pct",
            "annual_benchmark_pct",
            "benchmark_pct",
            "bond_hurdle_pct",
            "bond_net_threshold_pct",
            "normalized_bond_threshold_pct",
            "real_return_threshold_pct",
        ]

    rows = []
    for col in benchmark_candidates:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            rows.append(
                {
                    "benchmark_column": col,
                    "non_null_count": int(s.notna().sum()),
                    "null_count": int(s.isna().sum()),
                    "median_value": float(s.median()) if s.notna().any() else np.nan,
                    "min_value": float(s.min()) if s.notna().any() else np.nan,
                    "max_value": float(s.max()) if s.notna().any() else np.nan,
                }
            )

    if not rows:
        rows.append(
            {
                "benchmark_column": "NO_CANDIDATE_FOUND",
                "non_null_count": 0,
                "null_count": len(df),
                "median_value": np.nan,
                "min_value": np.nan,
                "max_value": np.nan,
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# Risk metrics
# ---------------------------------------------------------------------

def compute_cumulative_growth(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    date_col: str = "month_end",
    return_col: Optional[str] = None,
    out_col: str = "growth_index",
    start_value: float = 1.0,
) -> pd.DataFrame:
    """
    Convert monthly return series into cumulative growth index.
    """
    out = df.copy()
    if ticker_col is None:
        ticker_col = infer_ticker_column(out)
    if return_col is None:
        return_col = infer_return_column(out)

    validate_required_columns(out, [ticker_col, date_col, return_col], "risk_df")

    out = out.sort_values([ticker_col, date_col]).copy()

    out[out_col] = (
        out.groupby(ticker_col, dropna=False)[return_col]
        .transform(lambda s: (1.0 + s.fillna(0.0)).cumprod() * start_value)
    )
    return out


def compute_drawdown_from_growth(
    df: pd.DataFrame,
    ticker_col: Optional[str] = None,
    growth_col: str = "growth_index",
    out_col: str = "drawdown",
) -> pd.DataFrame:
    """
    Compute drawdown from a cumulative growth index.
    """
    out = df.copy()
    if ticker_col is None:
        ticker_col = infer_ticker_column(out)

    validate_required_columns(out, [ticker_col, growth_col], "growth_df")

    running_peak = out.groupby(ticker_col, dropna=False)[growth_col].cummax()
    out[out_col] = out[growth_col] / running_peak - 1.0
    return out


def summarize_volatility_drawdown(
    df: pd.DataFrame,
    mode: str,
    ticker_col: Optional[str] = None,
    return_col: Optional[str] = None,
    drawdown_col: str = "drawdown",
) -> pd.DataFrame:
    """
    Summarize annualized volatility and maximum drawdown by ticker.
    """
    out = df.copy()
    if ticker_col is None:
        ticker_col = infer_ticker_column(out)
    if return_col is None:
        return_col = infer_return_column(out)

    validate_required_columns(out, [ticker_col, return_col, drawdown_col], "vol_dd_df")

    summary = (
        out.groupby(ticker_col, dropna=False)
        .agg(
            annualized_volatility=(return_col, lambda s: float(pd.Series(s).std(ddof=1) * math.sqrt(12))),
            max_drawdown=(drawdown_col, "min"),
            n_return_obs=(return_col, lambda s: int(pd.Series(s).notna().sum())),
        )
        .reset_index()
    )
    summary["mode"] = mode
    return summary[[ticker_col, "mode", "annualized_volatility", "max_drawdown", "n_return_obs"]]


# ---------------------------------------------------------------------
# Process-output helpers
# ---------------------------------------------------------------------

def find_first_existing_file(
    base_dir: str | Path,
    candidates: Sequence[str],
) -> Path:
    """
    Return first existing candidate file beneath base_dir.
    """
    base_dir = Path(base_dir)
    for candidate in candidates:
        path = base_dir / candidate
        if path.exists():
            return path
    raise FileNotFoundError(
        f"None of the candidate files were found under {base_dir}: {list(candidates)}"
    )


def load_monthly_panel_from_process(process_dir: str | Path) -> pd.DataFrame:
    """
    Load the most likely monthly ETF/context panel from PROCESS outputs.

    Candidate search is intentionally flexible because exact filenames may vary.
    """
    candidates = [
        "monthly_merged_context.csv",
        "monthly_merged_context.parquet",
        "etf_monthly_merged_context.csv",
        "etf_monthly_merged_context.parquet",
        "monthly_panel.csv",
        "monthly_panel.parquet",
        "etf_monthly_resample.csv",
        "etf_monthly_resample.parquet",
    ]
    path = find_first_existing_file(process_dir, candidates)
    df = load_table(path)
    df = normalize_column_names(df)
    df = add_month_end_column(df)
    return df


def load_cleaned_etf_panel_from_process(process_dir: str | Path) -> pd.DataFrame:
    """
    Load the most likely cleaned ETF panel from PROCESS outputs.
    """
    candidates = [
        "etf_cleaned.csv",
        "etf_cleaned.parquet",
        "cleaned_etf_panel.csv",
        "cleaned_etf_panel.parquet",
        "etf_panel_clean.csv",
        "etf_panel_clean.parquet",
    ]
    path = find_first_existing_file(process_dir, candidates)
    df = load_table(path)
    df = normalize_column_names(df)
    df = add_month_end_column(df)
    return df


# ---------------------------------------------------------------------
# Audit helpers
# ---------------------------------------------------------------------

def assert_no_infinite_values(df: pd.DataFrame, cols: Sequence[str], df_name: str) -> None:
    """
    Raise if selected columns contain +/- inf values.
    """
    for col in cols:
        s = pd.to_numeric(df[col], errors="coerce")
        if np.isinf(s).any():
            raise ValueError(f"{df_name}.{col} contains infinite values.")


def build_run_metadata(
    mode: str,
    n_rows_input: int,
    n_rows_output: int,
    notes: Optional[Iterable[str]] = None,
) -> str:
    """
    Build simple text metadata for logs.
    """
    lines = [
        f"mode: {mode}",
        f"input_rows: {n_rows_input}",
        f"output_rows: {n_rows_output}",
    ]
    if notes:
        lines.append("notes:")
        for note in notes:
            lines.append(f"- {note}")
    return "\n".join(lines)


def format_pct(series: pd.Series, decimals: int = 4) -> pd.Series:
    """
    Helper for final CSV/report formatting if needed.
    Leaves raw values numeric if caller does not use it.
    """
    return series.round(decimals)


# ---------------------------------------------------------------------
# End of module
# ---------------------------------------------------------------------