import asyncio
from tools.ticker_loader import load_nifty500_tickers
from scanner.async_scanner import scan_market
from orchestrator.crew_runner import run_pipeline

if __name__ == "__main__":
    tickers = load_nifty500_tickers()
    print("Scanning market...")

    filtered_stocks = asyncio.run(scan_market(tickers))
    print(f"Scanner selected {len(filtered_stocks)} stocks")

    if not filtered_stocks:
        print("No stocks selected by scanner. Exiting.")
        exit()

    results = run_pipeline(filtered_stocks)

    # Pretty print
    import pandas as pd
    df = pd.DataFrame(results)
    print(df)