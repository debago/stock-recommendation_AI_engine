# dashboards/streamlit_uiapp.py
import sys
import os
import time

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
from orchestrator.crew_runner import run_pipeline

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
            # 1️⃣ Load tickers inside run_pipeline if not provided
            # Optionally you can pass tickers from CSV here

            # 2️⃣ Initialize progress bar and status text
            progress_bar = st.progress(0)
            status_text = st.empty()

            batch_size = 50  # adjust batch size as needed
            all_results = []

            # Get tickers list first
            from tools.ticker_loader import load_nifty500_tickers
            tickers = load_nifty500_tickers()
            total_batches = (len(tickers) + batch_size - 1) // batch_size

            for idx in range(0, len(tickers), batch_size):
                batch = tickers[idx: idx + batch_size]
                status_text.text(f"Processing batch {idx // batch_size + 1} of {total_batches}...")

                # 3️⃣ Run pipeline on current batch
                batch_results = run_pipeline(batch, batch_size=batch_size)
                if batch_results:
                    all_results.extend(batch_results)

                # 4️⃣ Update progress bar
                progress = min(1.0, (idx + batch_size) / len(tickers))
                progress_bar.progress(progress)
                time.sleep(0.1)  # slight delay for UI update

            # -----------------------------
            # 5️⃣ Handle empty results
            # -----------------------------
            if not all_results:
                st.warning("No valid stock signals returned. Check tool executions or data availability.")
                st.stop()

            # -----------------------------
            # 6️⃣ Convert to DataFrame
            # -----------------------------
            df = pd.DataFrame(all_results)

            if df.empty:
                st.warning("Crew returned an empty result. Check logs for errors.")
                st.stop()

            # -----------------------------
            # 7️⃣ Rename columns for display
            # -----------------------------
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

            # -----------------------------
            # 8️⃣ Display results
            # -----------------------------
            st.success("Analysis Complete! Top 10 Stocks:")
            st.dataframe(df.head(10), use_container_width=True)

        except Exception as e:
            st.error(f"Pipeline failed: {e}")