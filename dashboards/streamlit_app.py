import streamlit as st
from orchestrator.crew_runner import run_pipeline
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Nifty500 Swing Trading AI", layout="wide")
st.title("📈 Nifty500 AI Swing Trading Dashboard")

if st.button("Analyze Stocks"):
    with st.spinner("Running AI pipeline..."):
        result = run_pipeline()  # runs all 5 agents
        st.success("Analysis Complete!")

        # Assume result is a list of dicts
        # Example: [{"ticker": "RELIANCE", "entry": 2500, "target": 2700, "sl": 2450, "upside": 8.0}]
        df = pd.DataFrame(result)

        st.subheader("Top 10 Swing Trade Stocks")
        st.dataframe(df)

        # Example: Plot Upside Potential
        fig = px.bar(df, x="ticker", y="upside", text="upside",
                     labels={"upside": "Upside Potential (%)"}, title="Upside Potential of Top Stocks")
        st.plotly_chart(fig, use_container_width=True)


from dashboards.plots import plot_upside

fig = plot_upside(df)
st.plotly_chart(fig, use_container_width=True)