from crewai import Agent
from tools.quant_engine import quant_screen

trend_agent = Agent(

    role="Trend Following Specialist",

    goal="Identify strong uptrending stocks",

    backstory="Expert in moving average trend analysis",

    tools=[quant_screen],

    verbose=True
)