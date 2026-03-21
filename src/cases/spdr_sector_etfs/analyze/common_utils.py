import pandas as pd
import numpy as np

COMMON_WINDOW_START = "2018-06-20"

def load_dataset(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["ticker", "date"])
    return df

def compute_returns(df):
    df = df.copy()
    df["return"] = df.groupby("ticker")["close"].pct_change()
    return df

def pivot_returns(df):
    return df.pivot(index="date", columns="ticker", values="return")

def get_common_window(df):
    return df[df["date"] >= COMMON_WINDOW_START]

def annualize_return(daily_returns):
    daily_returns = daily_returns.dropna()

    compounded = (1 + daily_returns).prod()

    years = len(daily_returns) / 252

    return compounded ** (1 / years) - 1

def annualize_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(252)

def compute_drawdown(price_series):
    cumulative = (1 + price_series).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown