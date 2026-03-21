from __future__ import annotations

import argparse
import pandas as pd
from common_io import save_csv_with_metadata


def parse_args():
    parser = argparse.ArgumentParser(description="Create bond reference template.")
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Single output directory for saved files."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("Creating bond reference template...")

    data = {
        "bond_id": ["2033/I"],
        "country": ["Hungary"],
        "type": ["Inflation Linked"],
        "premium": ["0.5%"],
        "redemption_fee": ["1%"]
    }

    df = pd.DataFrame(data)

    saved_path = save_csv_with_metadata(
        df=df,
        output_dir=args.output_dir,
        filename="bond_reference_template.csv"
    )

    print(f"Bond template created -> {saved_path}")


if __name__ == "__main__":
    main()