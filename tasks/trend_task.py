from crewai import Task
from agents.trend_agent import trend_agent

trend_task = Task(
    description="""
    Analyze the stock universe for strong uptrends:
    - EMA20 > EMA50
    - ADX confirming trend strength
    Return stocks with confirmed trend.
    """,
    expected_output="Stocks with confirmed uptrend",
    agent=trend_agent
)