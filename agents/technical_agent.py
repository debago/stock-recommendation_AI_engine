from crewai import Agent
from tools.quant_engine import quant_screen


# -----If separate LLm instance is needed for technical agent, it can be created in config/llm_config.py and imported here-----

# from langchain_openai import ChatOpenAI

# technical_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

technical_agent = Agent(
    role="Technical Swing Trader",

    goal="Find stocks with volume surge, ATR expansion and momentum",

    backstory="Professional trader specializing in volatility breakouts",

    tools=[quant_screen],
    verbose=True
)