from crewai import Agent
from config.llm_config import llm

portfolio_agent = Agent(

    role="Portfolio Manager",

    goal="Rank best 10 swing trade stocks",

    backstory="Experienced portfolio manager optimizing risk reward",
    tools=[],
    verbose=True,
    llm=llm  # gpt-3.5-turbo : here llm instance is passed to the agent from config/llm_config.py
)