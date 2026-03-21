import os
import seaborn as sns
import matplotlib.pyplot as plt
from common_utils import *

DATA = "data/processed/all_sectors_clean.csv"
OUTPUT = "cases/spdr-sector-etfs/outputs/03_analyze"

def run():

    df = load_dataset(DATA)
    df = compute_returns(df)
    df = get_common_window(df)

    pivot = pivot_returns(df)

    corr = pivot.corr()

    os.makedirs(OUTPUT, exist_ok=True)

    corr.to_csv(f"{OUTPUT}/common_window_correlation_matrix.csv")

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")

    plt.title("Sector Correlation Heatmap")

    plt.savefig(f"{OUTPUT}/correlation_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    run()