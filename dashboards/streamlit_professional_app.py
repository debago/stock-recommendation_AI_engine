import sys
import os
import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from orchestrator.crew_runner import run_pipeline


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Stock Advisor",
    layout="wide"
)

st.title("AI Stock Advisor — Nifty500 Swing Picks")

st.write(
    "Click the button below to analyze Nifty500 stocks and generate top swing trade opportunities."
)


# -----------------------------
# Run Analysis
# -----------------------------
if st.button("Analyze Stocks"):

    progress_bar = st.progress(0)
    status = st.empty()

    try:

        status.text("Running AI analysis on Nifty500...")

        results = run_pipeline()

        progress_bar.progress(1.0)

        if not results or len(results) == 0:

            st.warning("No valid signals returned by AI.")
            st.stop()


        df = pd.DataFrame(results)

        if df.empty:

            st.warning("No stocks selected.")
            st.stop()


        st.success("Analysis Complete")

        st.dataframe(df, width="stretch")


    except Exception as e:

        st.error(f"Pipeline failed: {e}")