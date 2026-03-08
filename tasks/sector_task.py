from crewai import Task
from agents.sector_agent import sector_agent

sector_task = Task(
    description="""
        For each stock in Nifty500:
        - Identify the sector
        - Compare sector performance vs benchmark index
        - Assign sector strength score (1-10)
        Return stocks with strong sectors only.
    """,
    expected_output="Stocks ranked by sector strength",
    agent=sector_agent
)