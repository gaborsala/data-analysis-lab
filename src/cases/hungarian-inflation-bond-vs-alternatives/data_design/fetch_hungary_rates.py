from __future__ import annotations

import argparse
import pandas as pd
from common_io import save_csv_with_metadata


def parse_args():
    parser = argparse.ArgumentParser(description="Download Hungary 10Y yield data.")
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Single output directory for saved files."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Downloading Hungary 10Y yield...")

    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IRLTLT01HUM156N"
    df = pd.read_csv(url)
    df.columns = ["date", "yield_10y"]

    saved_path = save_csv_with_metadata(
        df=df,
        output_dir=args.output_dir,
        filename="hungary_10y_yield.csv"
    )

    print(f"Yield dataset saved -> {saved_path}")


if __name__ == "__main__":
    main()