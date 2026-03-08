from crewai import Agent
from tools.fundamentals_tool import get_fundamentals


fundamental_agent = Agent(

    role="Equity Research Analyst",

    goal="Filter fundamentally strong companies",

    backstory="Expert in company financial analysis",

    tools=[get_fundamentals],

    verbose=True
)