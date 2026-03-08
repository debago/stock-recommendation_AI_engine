# tasks/universal_task.py
from crewai import Task
from agents.universe_agent import universe_agent
from tools.ticker_loader import get_nifty500_tickers

# This task only loads tickers — no calculations
def load_tickers_task():
    return get_nifty500_tickers()  # Calls your CrewAI tool

universal_task = Task(
    description="Load the list of Nifty500 stocks",
    expected_output="A list of Nifty500 stock tickers",
    agent=universe_agent,
    execute=load_tickers_task
)