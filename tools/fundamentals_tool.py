from crewai.tools import tool
import yfinance as yf


@tool
def get_fundamentals(ticker: str):
    """
    Fetch key fundamental metrics for a given stock.
     - ROE
     - Debt/Equity
     - Revenue Growth
     Returns a dictionary of fundamentals.
     Note: In production, consider using a more robust data source or API.
     This is a simplified example using yfinance.
    """

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "roe": info.get("returnOnEquity"),
        "debt_equity": info.get("debtToEquity"),
        "revenue_growth": info.get("revenueGrowth")
    }