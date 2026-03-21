import os
import matplotlib.pyplot as plt
from common_utils import *

DATA = "data/processed/all_sectors_clean.csv"
OUTPUT = "cases/spdr-sector-etfs/outputs/03_analyze"

def run():

    df = load_dataset(DATA)
    df = compute_returns(df)
    df = get_common_window(df)

    pivot = pivot_returns(df)

    dispersion = pivot.std(axis=1).rename("dispersion")

    os.makedirs(OUTPUT, exist_ok=True)

    dispersion.to_csv(f"{OUTPUT}/cross_sectional_dispersion.csv")

    plt.figure(figsize=(12, 6))
    dispersion.plot()

    plt.title("Cross-Sectional Sector Dispersion")
    plt.xlabel("Date")
    plt.ylabel("Dispersion")

    plt.savefig(f"{OUTPUT}/cross_sectional_dispersion.png", dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    run()