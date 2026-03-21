import os
import pandas as pd
import matplotlib.pyplot as plt
from common_utils import *

DATA = "data/processed/all_sectors_clean.csv"
OUTPUT = "cases/spdr-sector-etfs/outputs/03_analyze"

def run():

    df = load_dataset(DATA)
    df = compute_returns(df)
    df = get_common_window(df)

    pivot = pivot_returns(df)

    os.makedirs(OUTPUT, exist_ok=True)

    drawdown_df = pd.DataFrame(index=pivot.index)

    plt.figure(figsize=(12, 7))

    for ticker in pivot.columns:
        series = pivot[ticker].dropna()
        drawdown = compute_drawdown(series)

        drawdown_df[ticker] = drawdown
        drawdown.plot(label=ticker)

    drawdown_df.to_csv(f"{OUTPUT}/common_window_drawdowns.csv")

    plt.title("Sector Drawdown Curves")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()

    plt.savefig(f"{OUTPUT}/drawdown_curves.png", dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    run()