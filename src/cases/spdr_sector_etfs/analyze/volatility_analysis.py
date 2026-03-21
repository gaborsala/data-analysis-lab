import matplotlib.pyplot as plt
import pandas as pd
from common_utils import *

DATA = "data/processed/all_sectors_clean.csv"

def run():

    df = load_dataset(DATA)
    df = compute_returns(df)
    df = get_common_window(df)

    pivot = pivot_returns(df)

    # Boxplot
    plt.figure()

    pivot.plot.box()
    plt.title("Sector Daily Return Distribution")

    plt.savefig("cases/spdr-sector-etfs/outputs/03_analyze/sector_return_boxplot.png")

    # Rolling volatility
    rolling_vol = pivot.rolling(90).std() * (252 ** 0.5)

    plt.figure()
    rolling_vol.plot()

    plt.title("Rolling 90-Day Volatility")
    plt.savefig("cases/spdr-sector-etfs/outputs/03_analyze/rolling_90d_volatility.png")


if __name__ == "__main__":
    run()