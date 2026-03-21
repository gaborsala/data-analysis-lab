import pandas as pd
from common_utils import *

DATA = "data/processed/all_sectors_clean.csv"

def run():

    df = load_dataset(DATA)
    df = compute_returns(df)

    pivot = pivot_returns(df)

    summary = []

    for ticker in pivot.columns:

        series = pivot[ticker].dropna()

        summary.append({
            "ticker": ticker,
            "annual_return": annualize_return(series),
            "annual_volatility": annualize_volatility(series),
            "observations": len(series)
        })

    out = pd.DataFrame(summary)
    out.to_csv("cases/spdr-sector-etfs/outputs/03_analyze/returns_summary_full_history.csv", index=False)

    # common window
    cw = get_common_window(df)
    pivot_cw = pivot_returns(cw)

    summary = []

    for ticker in pivot_cw.columns:

        series = pivot_cw[ticker].dropna()

        summary.append({
            "ticker": ticker,
            "annual_return": annualize_return(series),
            "annual_volatility": annualize_volatility(series),
            "observations": len(series)
        })

    out = pd.DataFrame(summary)
    out.to_csv("cases/spdr-sector-etfs/outputs/03_analyze/returns_summary_common_window.csv", index=False)


if __name__ == "__main__":
    run()