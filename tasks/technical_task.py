from crewai import Task
from agents.technical_agent import technical_agent

technical_task = Task(
    description="""
    Use the Quant Engine to identify stocks with:
    - Volume surge
    - ATR expansion
    - Momentum (RSI > threshold)
    - EMA trend confirmation
    Return top candidates for further analysis.
    """,
    expected_output="List of technical candidate stocks",
    agent=technical_agent
)