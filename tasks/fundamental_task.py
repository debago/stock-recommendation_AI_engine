from crewai import Task
from agents.fundamental_agent import fundamental_agent

fundamental_task = Task(
    description="""
    Evaluate fundamental health of each stock:
    - ROE
    - Debt-to-equity ratio
    - Revenue growth
    Return fundamentally strong stocks.
    """,
    expected_output="Fundamentally strong stock list",
    agent=fundamental_agent
)