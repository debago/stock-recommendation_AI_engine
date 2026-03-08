from crewai import Agent
from tools.ticker_loader import get_nifty500_tickers

universe_agent = Agent(
    role="Stock Universe Specialist",
    goal="Provide the list of Nifty500 stocks",
    backstory="Expert in Indian stock market universe construction",
    tools=[get_nifty500_tickers],
    verbose=True
)