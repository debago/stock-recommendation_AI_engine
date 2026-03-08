from crewai import Task
from agents.portfolio_agent import portfolio_agent


portfolio_task = Task(

    description="""
    Combine insights from technical, trend, sector and fundamental analysis.

    Select top 10 stocks suitable for 2-6 week swing trades.

    Inputs include:
    - Technical signals (volume surge, ATR expansion, momentum)
    - Trend strength (EMA, uptrend)
    - Sector performance (sectors beating benchmark)
    - Fundamental strength (ROE, debt-to-equity, revenue growth)

    For each stock, provide:
    1. Entry price (numeric)
    2. Target price (numeric)
    3. Stop-loss (SL, numeric)
    4. Upside percentage (numeric) = (Target - Entry)/Entry * 100
    5. Risk-Reward ratio (string or numeric) = (Target - Entry)/(Entry - SL)
    6. Justification for recommendation
    7. Risks

    **Return ONLY JSON array of 10 dictionaries**, each dictionary must include keys:

    "Rank", "Stock", "Sector", "Entry", "Target", "SL", "Upside (%)", "Risk-Reward", "Justification", "Risk"

    Example:

    [
    {
        "Rank": 1,
        "Stock": "L&T",
        "Sector": "Infrastructure",
        "Entry": 3720,
        "Target": 4150,
        "SL": 3550,
        "Upside (%)": 11,
        "Risk-Reward": "1:2.5",
        "Justification": "Volume surge, ATR expansion, strong trend, sector outperforming",
        "Risk": "Earnings next week, RSI overbought"
    },
    ...
    ]
        Justification
        Risks
        """,

    expected_output="Top 10 ranked stocks",

    agent=portfolio_agent
)