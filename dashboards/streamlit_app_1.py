import streamlit as st
from orchestrator.crew_runner import run_pipeline  # import your wrapper function

st.set_page_config(page_title="AI Stock Advisor", layout="wide")
st.title("AI Stock Advisor — Nifty500 Swing Picks")

st.write("Click the button below to analyze Nifty500 stocks and get top 10 high conviction trades.")

if st.button("Analyze Stocks"):
    with st.spinner("Running AI pipeline..."):
        try:
            result = run_pipeline()  # calls crew.kickoff() internally
            st.success("Analysis Complete!")
            st.write(result)  # show the result (could be a dict or string)
        except Exception as e:
            st.error(f"Pipeline failed: {e}")