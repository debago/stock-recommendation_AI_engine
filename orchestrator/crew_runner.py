# orchestrator/crew_runner.py
from crewai import Crew
from agents.universe_agent import universe_agent
from agents.technical_agent import technical_agent
from agents.trend_agent import trend_agent
from agents.sector_agent import sector_agent
from agents.fundamental_agent import fundamental_agent
from agents.portfolio_agent import portfolio_agent

from tasks.universal_task import universal_task
from tasks.technical_task import technical_task
from tasks.trend_task import trend_task
from tasks.sector_task import sector_task
from tasks.fundamental_task import fundamental_task
from tasks.portfolio_task import portfolio_task
from tools.ticker_loader import load_nifty500_tickers


# -----------------------------
# Create the Crew
# -----------------------------
crew = Crew(
    agents=[
        universe_agent,
        technical_agent,
        trend_agent,
        sector_agent,
        fundamental_agent,
        portfolio_agent
    ],
    tasks=[
        universal_task,
        technical_task,
        trend_task,
        sector_task,
        fundamental_task,
        portfolio_task
    ],
    process="sequential",  # Or "parallel" if tasks are independent
    verbose=True
)


# -----------------------------
# Pipeline runner
# -----------------------------
# orchestrator/crew_runner.py
def run_pipeline(tickers=None, batch_size=50):
    """
    Run the Crew pipeline in batches.
    tickers: list of tickers to process
    batch_size: batch size for Crew kickoff
    """
    if tickers is None:
        # Load tickers from CSV if not provided
        from tools.ticker_loader import load_nifty500_tickers
        tickers = load_nifty500_tickers()

    if not tickers:
        return []

    results = []

    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        output = crew.kickoff(inputs={"stocks": batch})

        if isinstance(output, list):
            valid_output = [r for r in output if r is not None]
            results.extend(valid_output)
        elif output is not None:
            results.append(output)

    if len(results) > 10:
        results = results[:10]

    return results


# -----------------------------
# Optional standalone run
# -----------------------------
if __name__ == "__main__":
    top_stocks = run_pipeline()
    print("Top Stocks:", top_stocks)