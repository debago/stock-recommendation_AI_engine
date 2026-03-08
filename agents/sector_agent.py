from crewai import Agent
from tools.market_data_tool import get_stock_data
from tools.sector_analysis_tool import sector_strength
# from config.llm_config import llm

sector_agent = Agent(
    role="Sector Rotation Expert",
    goal="""
        Identify sectors that are currently outperforming the benchmark index (Nifty 500),
        assign sector strength to each stock.
    """,
    backstory="""
        You are a market analyst specializing in sector rotation strategies.
        Your job is to find which sectors are strong and allocate strength scores
        to stocks based on sector performance.
    """,
    tools=[get_stock_data, sector_strength],  # can fetch sector ETFs or representative stocks
    # llm=llm,
    verbose=True
)