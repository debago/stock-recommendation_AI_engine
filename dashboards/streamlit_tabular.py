import ast
import pandas as pd
import streamlit as st
from orchestrator.crew_runner import crew

if st.button("Run Analysis"):
    with st.spinner("Analyzing stocks, please wait..."):
        result = crew.kickoff()  # Portfolio Agent output as JSON string
    
    # Convert JSON string to Python list
    stock_list = ast.literal_eval(result)
    df = pd.DataFrame(stock_list)

    # Display sorted by Rank
    df.sort_values("Rank", inplace=True)
    st.subheader("Top 10 Stocks with Risk-Reward")
    st.dataframe(df, use_container_width=True)