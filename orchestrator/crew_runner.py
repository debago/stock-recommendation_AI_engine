import json
import pandas as pd
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
# Crew Definition
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
# Convert any value → scalar
# -----------------------------
def make_scalar(value):

    if isinstance(value, dict):
        return json.dumps(value)

    if isinstance(value, (list, tuple, set)):
        return ", ".join(map(str, value))

    return value


# -----------------------------
# Run Full Pipeline
# -----------------------------
def run_pipeline(batch_size=50):

    tickers = load_nifty500_tickers()

    if not tickers:
        print("No tickers loaded.")
        return []

    all_results = []

    total = len(tickers)

    for idx in range(0, total, batch_size):

        batch = tickers[idx: idx + batch_size]

        print(f"\nProcessing batch {idx//batch_size + 1} | Stocks {idx}-{idx+len(batch)}")

        result = crew.kickoff(
            inputs={"stocks": batch}
        )

        print("CREW RESULT TYPE:", type(result))

        # -----------------------------
        # Parse Crew Output Robustly
        # -----------------------------
        parsed = None

        try:

            if hasattr(result, "raw"):
                parsed = json.loads(result.raw)

            elif isinstance(result, str):
                parsed = json.loads(result)

            else:
                parsed = result

        except Exception as e:

            print("Parsing failed:", e)
            print("Raw result:", result)
            continue


        if isinstance(parsed, list):
            all_results.extend(parsed)

        elif isinstance(parsed, dict):
            all_results.append(parsed)


    if not all_results:
        print("No valid results returned by Crew.")
        return []


    # -----------------------------
    # Convert to DataFrame
    # -----------------------------
    df = pd.DataFrame(all_results)

    print("\nColumn Type Debug:")
    print(df.applymap(type).head())


    # -----------------------------
    # Force Arrow-safe values
    # -----------------------------
    for col in df.columns:
        df[col] = df[col].apply(make_scalar)


    # -----------------------------
    # Limit to Top 10
    # -----------------------------
    if len(df) > 10:
        df = df.head(10)


    print("\nFinal Output:")
    print(df.head())

    return df.to_dict(orient="records")