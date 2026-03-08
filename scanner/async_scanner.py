import yfinance as yf
import pandas as pd
import asyncio
import concurrent.futures

from tools.quant_engine import compute_indicators


def fetch_stock_data(ticker):

    try:
        df = yf.download(ticker, period="3mo", interval="1d", progress=False)

        if df.empty:
            return None

        indicators = compute_indicators(df)

        if (
            indicators["volume_surge"]
            and indicators["momentum"]
            and indicators["trend"]
        ):
            return ticker

    except Exception:
        return None

    return None


async def scan_market(tickers):

    loop = asyncio.get_event_loop()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

        tasks = [
            loop.run_in_executor(executor, fetch_stock_data, ticker)
            for ticker in tickers
        ]

        results = await asyncio.gather(*tasks)

    filtered = [r for r in results if r is not None]

    return filtered