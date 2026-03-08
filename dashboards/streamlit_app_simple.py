import streamlit as st
from orchestrator.crew_runner import crew

st.title("AI Stock Advisor")

if st.button("Analyze Nifty500 Stocks"):
    result = crew.kickoff()
    st.write(result)