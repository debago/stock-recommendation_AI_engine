import pandas as pd
from crewai.tools import tool


def load_nifty500_tickers():
    df = pd.read_csv("data/ind_nifty100list.csv")

    tickers = (
        df["Symbol"]
        .dropna()
        .str.strip()
        .apply(lambda x: f"{x}.NS")
        .tolist()
    )

    return tickers


@tool
def get_nifty500_tickers():
    """
    Load and return Nifty500 tickers
    """
    return load_nifty500_tickers()