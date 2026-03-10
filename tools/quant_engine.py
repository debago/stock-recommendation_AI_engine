# tools/quant_engine.py
import ta
import yfinance as yf
from crewai.tools import tool


def compute_indicators(df):
    """
    Compute technical indicators for a stock dataframe.
    Returns a dict or None if df is empty/invalid.
    """
    if df.empty:
        return None  # Safe return for empty data

    df = df.dropna()
    if df.shape[0] < 20:  # Not enough data to compute rolling indicators
        return None

    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()
    volume = df["Volume"].squeeze()

    df["rsi"] = ta.momentum.RSIIndicator(close).rsi()
    df["atr"] = ta.volatility.AverageTrueRange(high, low, close).average_true_range()
    df["ema20"] = df["Close"].ewm(span=20).mean()
    df["ema50"] = df["Close"].ewm(span=50).mean()
    volume_avg = volume.rolling(20).mean()

    latest = df.iloc[-1]

    # Safely convert scalars
    def safe_float(val):
        if hasattr(val, "iloc"):
            return float(val.iloc[0])
        return float(val)

    return {
        "volume_surge": latest["Volume"] > 2 * volume_avg.iloc[-1],
        "momentum": latest["rsi"] > 0,
        "trend": latest["ema20"] > latest["ema50"],
        "atr": safe_float(latest["atr"]),
        "rsi": safe_float(latest["rsi"]),
    }


@tool("quant_screen")
def quant_screen(stock: str) -> dict:
    """
    Screen a stock for technical signals.
    Returns None if data is missing or invalid.
    """
    try:
        df = yf.download(stock, period="6mo", auto_adjust=True, progress=False)
        result = compute_indicators(df)
        if result is None:
            print(f"Skipping {stock}: insufficient data")
        return result
    except Exception as e:
        print(f"Failed to process {stock}: {e}")
        return None