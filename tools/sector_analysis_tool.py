import yfinance as yf
from crewai.tools import tool
from typing import List, Dict

@tool
def sector_strength(sector_tickers: List[str]) -> Dict[str, float]:
    """
    Compute sector strength based on 3-month returns.
    
    Args:
        sector_tickers: List of ticker symbols in the sector.
    
    Returns:
        Dictionary mapping ticker symbol to a strength score (percentage return).
    """
    scores = {}
    for ticker in sector_tickers:
        try:
            df = yf.download(ticker, period="3mo", auto_adjust=True, progress=False)
            if df.empty:
                scores[ticker] = 0.0
            else:
                returns = (df['Close'][-1] - df['Close'][0]) / df['Close'][0] * 100
                scores[ticker] = round(returns, 2)
        except Exception:
            scores[ticker] = 0.0
    return scores