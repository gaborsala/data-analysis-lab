from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_process_utils import (
    add_year_month_period,
    load_csv,
    parse_dates_by_name,
    pct_string_to_points,
    validate_no_parse_failures,
    write_csv,
    write_json,
)


def clean_etf_prices(raw_dir: Path, out_dir: Path) -> dict:
    df_raw = load_csv(raw_dir / "etf_prices_daily.csv")
    df = parse_dates_by_name(df_raw)

    parse_issues = validate_no_parse_failures(df_raw, df)

    coverage = pd.read_csv(out_dir / "etf_ticker_coverage_profile.csv", parse_dates=["first_date_all", "last_date_all", "first_valid_close_date", "last_valid_close_date"])
    null_summary = pd.read_csv(out_dir / "etf_null_window_classification_summary.csv", parse_dates=["first_valid_close_date", "last_valid_close_date"])

    coverage_map = coverage.set_index("ticker")[["first_valid_close_date", "last_valid_close_date"]].to_dict(orient="index")

    def keep_row(row: pd.Series) -> bool:
        if pd.notna(row["close"]):
            return True

        ticker = row["ticker"]
        d = row["Date"]
        first_valid = coverage_map[ticker]["first_valid_close_date"]
        last_valid = coverage_map[ticker]["last_valid_close_date"]

        if pd.isna(first_valid) or pd.isna(last_valid):
            return False

        return bool(first_valid <= d <= last_valid)

    before_rows = int(len(df))
    before_missing = int(df["close"].isna().sum())

    df["keep_row"] = df.apply(keep_row, axis=1)
    cleaned = df[df["keep_row"]].copy().drop(columns=["keep_row"])

    cleaned = cleaned.sort_values(["ticker", "Date"]).reset_index(drop=True)
    cleaned = add_year_month_period(cleaned, "Date", "year_month")

    after_rows = int(len(cleaned))
    after_missing = int(cleaned["close"].isna().sum())
    non_positive_close_count = int((cleaned["close"] <= 0).fillna(False).sum())

    write_csv(out_dir / "etf_prices_daily_clean.csv", cleaned)

    result = {
        "dataset": "etf_prices_daily",
        "before_rows": before_rows,
        "after_rows": after_rows,
        "rows_removed": before_rows - after_rows,
        "before_missing_close": before_missing,
        "after_missing_close": after_missing,
        "non_positive_close_count_after": non_positive_close_count,
        "date_parse_issues": parse_issues,
        "tickers_with_internal_active_nulls": int(null_summary["has_internal_active_nulls"].sum()) if not null_summary.empty else 0,
    }
    write_json(out_dir / "etf_prices_daily_cleaning_summary.json", result)
    return result


def clean_cpi(raw_dir: Path, out_dir: Path) -> dict:
    df_raw = load_csv(raw_dir / "hungary_cpi_yoy.csv")
    df = parse_dates_by_name(df_raw)
    parse_issues = validate_no_parse_failures(df_raw, df)

    df = df.sort_values("date").reset_index(drop=True)
    df = add_year_month_period(df, "date", "year_month")
    write_csv(out_dir / "hungary_cpi_yoy_clean.csv", df)

    result = {
        "dataset": "hungary_cpi_yoy",
        "before_rows": int(len(df_raw)),
        "after_rows": int(len(df)),
        "duplicate_date_count": int(df["date"].duplicated().sum()),
        "missing_value_count_after": int(df.isna().sum().sum()),
        "date_parse_issues": parse_issues,
    }
    write_json(out_dir / "hungary_cpi_yoy_cleaning_summary.json", result)
    return result


def clean_yield(raw_dir: Path, out_dir: Path) -> dict:
    df_raw = load_csv(raw_dir / "hungary_10y_yield.csv")
    df = parse_dates_by_name(df_raw)
    parse_issues = validate_no_parse_failures(df_raw, df)

    df = df.sort_values("date").reset_index(drop=True)
    df = add_year_month_period(df, "date", "year_month")
    write_csv(out_dir / "hungary_10y_yield_clean.csv", df)

    result = {
        "dataset": "hungary_10y_yield",
        "before_rows": int(len(df_raw)),
        "after_rows": int(len(df)),
        "duplicate_date_count": int(df["date"].duplicated().sum()),
        "missing_value_count_after": int(df.isna().sum().sum()),
        "date_parse_issues": parse_issues,
    }
    write_json(out_dir / "hungary_10y_yield_cleaning_summary.json", result)
    return result


def clean_bond_reference(raw_dir: Path, out_dir: Path) -> dict:
    df_raw = load_csv(raw_dir / "bond_reference_template.csv")
    df = df_raw.copy()

    df["premium_pct_points"] = df["premium"].apply(pct_string_to_points)
    df["redemption_fee_pct_points"] = df["redemption_fee"].apply(pct_string_to_points)

    write_csv(out_dir / "bond_reference_template_clean.csv", df)

    result = {
        "dataset": "bond_reference_template",
        "before_rows": int(len(df_raw)),
        "after_rows": int(len(df)),
        "premium_parse_success_count": int(df["premium_pct_points"].notna().sum()),
        "redemption_fee_parse_success_count": int(df["redemption_fee_pct_points"].notna().sum()),
        "premium_parse_failure_count": int(df["premium_pct_points"].isna().sum()),
        "redemption_fee_parse_failure_count": int(df["redemption_fee_pct_points"].isna().sum()),
    }
    write_json(out_dir / "bond_reference_template_cleaning_summary.json", result)
    return result


def create_monthly_etf_resample(out_dir: Path) -> dict:
    df = pd.read_csv(out_dir / "etf_prices_daily_clean.csv", parse_dates=["Date"])
    df = df.sort_values(["ticker", "Date"]).reset_index(drop=True)

    monthly = (
    df.groupby(["ticker", pd.Grouper(key="Date", freq="ME")], as_index=False)
      .agg(close_month_end=("close", "last"))
    )

    monthly["year_month"] = monthly["Date"].dt.to_period("M").astype(str)

    write_csv(out_dir / "etf_prices_month_end.csv", monthly)

    result = {
        "dataset": "etf_prices_month_end",
        "row_count": int(len(monthly)),
        "ticker_count": int(monthly["ticker"].nunique()),
        "missing_close_month_end_count": int(monthly["close_month_end"].isna().sum()),
        "rule": "last valid ETF close within calendar month by ticker",
    }
    write_json(out_dir / "etf_prices_month_end_summary.json", result)
    return result


def create_monthly_merged_context(out_dir: Path) -> dict:
    etf = pd.read_csv(out_dir / "etf_prices_month_end.csv", parse_dates=["Date"])
    cpi = pd.read_csv(out_dir / "hungary_cpi_yoy_clean.csv", parse_dates=["date"])
    yld = pd.read_csv(out_dir / "hungary_10y_yield_clean.csv", parse_dates=["date"])

    merged = etf.merge(
        cpi[["year_month", "cpi_yoy"]],
        on="year_month",
        how="left",
    ).merge(
        yld[["year_month", "yield_10y"]],
        on="year_month",
        how="left",
    )

    write_csv(out_dir / "monthly_merged_context.csv", merged)

    result = {
        "dataset": "monthly_merged_context",
        "row_count": int(len(merged)),
        "missing_cpi_yoy_count": int(merged["cpi_yoy"].isna().sum()),
        "missing_yield_10y_count": int(merged["yield_10y"].isna().sum()),
        "join_rule": "ETF month-end series left joined to monthly CPI and 10Y yield on year_month",
    }
    write_json(out_dir / "monthly_merged_context_summary.json", result)
    return result


def run(raw_dir: Path, out_dir: Path) -> None:
    summaries = [
        clean_etf_prices(raw_dir, out_dir),
        clean_cpi(raw_dir, out_dir),
        clean_yield(raw_dir, out_dir),
        clean_bond_reference(raw_dir, out_dir),
    ]
    summaries.append(create_monthly_etf_resample(out_dir))
    summaries.append(create_monthly_merged_context(out_dir))

    write_json(out_dir / "process_cleaning_overall_summary.json", summaries)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run PROCESS cleaning for all datasets.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    run(Path(args.raw_dir), Path(args.out_dir))