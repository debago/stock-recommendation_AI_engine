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
# Create Crew
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
    process="sequential",
    verbose=True
)

# -----------------------------
# Helper to recursively flatten nested values
# -----------------------------
def flatten_scalar(value):
    if isinstance(value, dict):
        return {k: flatten_scalar(v) for k, v in value.items()}
    elif isinstance(value, (list, tuple, set)):
        return ", ".join(map(str, value))
    else:
        return value

# -----------------------------
# Run pipeline function
# -----------------------------
def run_pipeline(tickers=None, batch_size=50):
    """
    Run Crew pipeline in batches of tickers.
    Ensures all outputs are fully scalar (no nested lists/dicts) so that
    UI or DataFrame conversions never fail.
    """
    if tickers is None:
        # Load from universal task if not provided
        tickers = load_nifty500_tickers()

    if not tickers:
        return []

    all_results = []
    total_batches = (len(tickers) + batch_size - 1) // batch_size

    for idx in range(0, len(tickers), batch_size):
        batch = tickers[idx: idx + batch_size]

        # Run Crew pipeline for this batch
        batch_result = crew.kickoff(inputs={"stocks": batch})

        if batch_result:
            if isinstance(batch_result, list):
                for r in batch_result:
                    if r is not None and isinstance(r, dict):
                        flattened = {k: flatten_scalar(v) for k, v in r.items()}
                        all_results.append(flattened)
            elif isinstance(batch_result, dict):
                all_results.append({k: flatten_scalar(v) for k, v in batch_result.items()})
            else:
                # If batch_result is a scalar/string, just append
                all_results.append(batch_result)

    # Keep only top 10 results if more than 10
    if len(all_results) > 10:
        all_results = all_results[:10]

    return all_results

# -----------------------------
# Optional standalone run
# -----------------------------
if __name__ == "__main__":
    top_stocks = run_pipeline()
    print("Top Stocks:", top_stocks)