import yfinance as yf


def load_market_data(tickers):
    """
    Download OHLCV data for multiple tickers at once
    """

    data = yf.download(
        tickers,
        period="6mo",
        group_by="ticker",
        progress=False
    )

    return data