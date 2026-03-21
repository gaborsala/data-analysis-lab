from __future__ import annotations

import argparse
import json
from pathlib import Path

from prepare_dataset_audit import build_summary


TEMPLATE = """# PREPARE SUPPORT OUTPUT

## Canonical dataset
- Source kind: {source_kind}
- Source path: `{source_path}`
- Canonical dataset: `{canonical_dataset}`

## Dataset size
- Rows: {row_count}
- Columns: {column_count}
- Date range: {min_date} → {max_date}
- Unique tickers: {unique_tickers}
- Unique sectors: {unique_sectors}

## File inventory
{file_inventory}

## Integrity checks
{checks}

## Missing by column
{missing}

## Ticker coverage
{ticker_coverage}
"""


def format_bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items) if items else "- None"



def main() -> None:
    parser = argparse.ArgumentParser(description="Convenience wrapper for PREPARE-phase audit outputs.")
    parser.add_argument("input_path", help="Path to ZIP archive or CSV file")
    parser.add_argument("--extract-dir", default=None, help="Extraction directory for ZIP inputs")
    parser.add_argument("--output-dir", default="prepare_outputs", help="Directory to save JSON and markdown support outputs")
    args = parser.parse_args()

    input_path = Path(args.input_path).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = build_summary(input_path, Path(args.extract_dir).resolve() if args.extract_dir else None)

    json_path = output_dir / "prepare_audit_summary.json"
    md_path = output_dir / "prepare_support_output.md"

    json_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    file_inventory = format_bullets([
        f"{row['relative_path']} | columns={row['column_count']} | {', '.join(row['columns'])}"
        for row in summary["file_inventory"]
    ])
    checks = format_bullets([
        f"{row['name']}: {row['value']} [{row['status']}] {row['notes']}`".rstrip("`")
        for row in summary["integrity_checks"]
    ])
    missing = format_bullets([
        f"{k}: {v}" for k, v in summary["missing_by_column"].items()
    ])
    ticker_coverage = format_bullets([
        f"{row['ticker']}: {row['min']} → {row['max']} | rows={row['count']}"
        for row in summary.get("ticker_date_coverage", [])
    ])

    md = TEMPLATE.format(
        source_kind=summary.get("source_kind"),
        source_path=summary.get("source_path"),
        canonical_dataset=summary.get("canonical_dataset"),
        row_count=summary.get("row_count"),
        column_count=summary.get("column_count"),
        min_date=summary.get("min_date"),
        max_date=summary.get("max_date"),
        unique_tickers=summary.get("unique_tickers"),
        unique_sectors=summary.get("unique_sectors"),
        file_inventory=file_inventory,
        checks=checks,
        missing=missing,
        ticker_coverage=ticker_coverage,
    )
    md_path.write_text(md, encoding="utf-8")

    print(f"Saved: {json_path}")
    print(f"Saved: {md_path}")


if __name__ == "__main__":
    main()
