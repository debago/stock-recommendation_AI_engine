# dashboards/streamlit_uiapp.py
import sys
import os

# -----------------------------
# 1️⃣ Ensure project root is in Python path
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -----------------------------
# 2️⃣ Imports
# -----------------------------
import streamlit as st
import pandas as pd
from tools.ticker_loader import load_nifty500_tickers
from orchestrator.crew_runner import run_pipeline
import ast
import time

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="AI Stock Advisor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("AI Stock Advisor — Nifty500 Swing Picks")
st.write("Click the button below to analyze Nifty500 stocks and get top 10 high conviction trades.")

# -----------------------------
# Button to run the pipeline
# -----------------------------
if st.button("Analyze Stocks"):
    with st.spinner("Running AI pipeline..."):

        try:
            # 1️⃣ Load Nifty500 tickers safely
            tickers = load_nifty500_tickers()
            if not tickers:
                st.warning("No tickers found in CSV. Please check data/ind_nifty500list.csv")
                st.stop()

            # 2️⃣ Initialize progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # 3️⃣ Process in batches
            batch_size = 50
            all_results = []
            total_batches = (len(tickers) + batch_size - 1) // batch_size

            for idx in range(0, len(tickers), batch_size):
                batch = tickers[idx: idx + batch_size]
                status_text.text(f"Processing batch {idx // batch_size + 1} of {total_batches}...")
                
                # Run Crew pipeline on this batch
                batch_result = run_pipeline(batch, batch_size=batch_size)

                if batch_result:
                    all_results.extend(batch_result)

                # Update progress bar
                progress = min(1.0, (idx + batch_size) / len(tickers))
                progress_bar.progress(progress)
                time.sleep(0.1)  # slight delay for UI update

            # 4️⃣ Handle no results
            if not all_results:
                st.warning("No valid stock signals returned. Check tool executions or data availability.")
                st.stop()

            # 5️⃣ Convert to DataFrame
            if isinstance(all_results, str):
                all_results = ast.literal_eval(all_results)

            df = pd.DataFrame(all_results)

            if df.empty:
                st.warning("Crew returned an empty result. Check logs for errors.")
                st.stop()

            # 6️⃣ Rename columns for user-friendly display
            df = df.rename(columns={
                "Rank": "Rank",
                "Stock": "Ticker",
                "Sector": "Sector",
                "Entry": "Entry Price",
                "Target": "Target Price",
                "SL": "Stoploss",
                "Upside (%)": "Upside (%)",
                "Risk-Reward": "Risk/Reward",
                "Justification": "Justification",
                "Risk": "Risk"
            })

            # 7️⃣ Display results
            st.success("Analysis Complete! Top 10 Stocks:")
            st.dataframe(df, width=True)

        except Exception as e:
            st.error(f"Pipeline failed: {e}")