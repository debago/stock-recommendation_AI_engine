import yfinance as yf
from crewai.tools import tool
import pandas as pd
from typing import List, Dict, Union

@tool
def get_stock_data(ticker: str, period: str = "6mo", interval: str = "1d") -> Union[str, List[Dict]]:
    """
    Fetch historical price data for a given stock.
    
    Args:
        ticker: Stock symbol (e.g., 'RELIANCE.NS')
        period: Data period (e.g., '6mo', '1y')
        interval: Data frequency (e.g., '1d', '1wk')
    
    Returns:
        Last 5 rows of historical data as a list of dictionaries, or error string if failed.
    """
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty:
            return f"No data found for {ticker}"
        return df.tail(5).to_dict(orient="records")
    except Exception as e:
        return f"Error fetching data for {ticker}: {str(e)}"