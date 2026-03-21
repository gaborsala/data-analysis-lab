from __future__ import annotations

import argparse
import pandas as pd
from common_io import save_csv_with_metadata


def parse_args():
    parser = argparse.ArgumentParser(description="Download Hungary CPI data.")
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Single output directory for saved files."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Downloading Hungary CPI data...")

    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=HUNCPALTT01CTGYM"
    df = pd.read_csv(url)
    df.columns = ["date", "cpi_yoy"]

    saved_path = save_csv_with_metadata(
        df=df,
        output_dir=args.output_dir,
        filename="hungary_cpi_yoy.csv"
    )

    print(f"CPI dataset saved -> {saved_path}")


if __name__ == "__main__":
    main()