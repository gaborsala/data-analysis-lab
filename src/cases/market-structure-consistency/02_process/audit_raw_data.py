from __future__ import annotations

from pathlib import Path
import pandas as pd

from config import CANONICAL_TICKERS, REQUIRED_COLUMNS, get_raw_data_dir


def audit_one_file(path: Path) -> dict:
    result = {
        "ticker": path.stem,
        "file_exists": path.exists(),
        "row_count": 0,
        "column_count": 0,
        "min_date": "",
        "max_date": "",
        "duplicate_date_count": 0,
        "missing_required_columns": "",
        "null_count_date": 0,
        "null_count_open": 0,
        "null_count_high": 0,
        "null_count_low": 0,
        "null_count_close": 0,
        "null_count_adj_close": 0,
        "null_count_volume": 0,
        "status": "unknown",
        "error_message": "",
    }

    if not path.exists():
        result["status"] = "missing_file"
        return result

    try:
        df = pd.read_csv(path)
        result["row_count"] = int(len(df))
        result["column_count"] = int(len(df.columns))

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        result["missing_required_columns"] = "|".join(missing_cols)

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            result["null_count_date"] = int(df["Date"].isna().sum())
            result["duplicate_date_count"] = int(df["Date"].duplicated().sum())

            non_null_dates = df["Date"].dropna()
            if not non_null_dates.empty:
                result["min_date"] = non_null_dates.min().strftime("%Y-%m-%d")
                result["max_date"] = non_null_dates.max().strftime("%Y-%m-%d")

        for source_col, out_key in [
            ("Open", "null_count_open"),
            ("High", "null_count_high"),
            ("Low", "null_count_low"),
            ("Close", "null_count_close"),
            ("Adj Close", "null_count_adj_close"),
            ("Volume", "null_count_volume"),
        ]:
            if source_col in df.columns:
                result[out_key] = int(df[source_col].isna().sum())

        if result["row_count"] == 0:
            result["status"] = "empty_file"
        elif missing_cols:
            result["status"] = "schema_warning"
        else:
            result["status"] = "ok"

        return result

    except Exception as exc:
        result["status"] = "read_error"
        result["error_message"] = str(exc)
        return result


def main() -> None:
    raw_dir = get_raw_data_dir().resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []

    for ticker in CANONICAL_TICKERS:
        path = raw_dir / f"{ticker}.csv"
        results.append(audit_one_file(path))

    audit_df = pd.DataFrame(results).sort_values("ticker")
    out_path = raw_dir / "raw_data_audit.csv"
    audit_df.to_csv(out_path, index=False)

    print("Raw data audit complete")
    print(f"- Raw directory: {raw_dir}")
    print(f"- Audit file: {out_path}")

    status_counts = audit_df["status"].value_counts(dropna=False).to_dict()
    print(f"- Status counts: {status_counts}")

    problems = audit_df[audit_df["status"] != "ok"]
    if not problems.empty:
        print("\nFiles requiring review:")
        print(problems[["ticker", "status", "missing_required_columns", "error_message"]].to_string(index=False))


if __name__ == "__main__":
    main()