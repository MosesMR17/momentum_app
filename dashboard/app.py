import glob
import os
import sys
import pandas as pd
import streamlit as st

# Add parent directory to system path so Python can locate 'modules'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.execution.main import run_momentum_app

# Page Setup
st.set_page_config(
    page_title="Quantitative Momentum Dashboard",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Quantitative Momentum & Trade Setup Dashboard")
st.markdown(
    "Real-time momentum scanning, news sentiment analysis, and automated risk management setups."
)

# Sidebar Action Controls
st.sidebar.header("Controls")
if st.sidebar.button("⚡ Run Fresh Pipeline Scan", type="primary"):
    with st.spinner(
        "Scanning watchlist, fetching market data, and calculating risk levels..."
    ):
        run_momentum_app()
    st.sidebar.success("Scan completed successfully!")

# Check for generated CSV reports in root directory
list_of_files = glob.glob("momentum_report_*.csv")

if list_of_files:
    # Select the most recently created report file
    latest_file = max(list_of_files, key=os.path.getctime)
    df = pd.read_csv(latest_file)

    st.subheader(f"📊 Latest Active Report: `{os.path.basename(latest_file)}`")

    # High-level Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Stocks Analyzed", len(df))

    if not df.empty:
        top_ticker = df.iloc[0]["Ticker"]
        top_mom = df.iloc[0]["3M Momentum (%)"]
        col2.metric("Top Momentum Stock", top_ticker, f"{top_mom:.2f}%")

    bullish_count = len(df[df["Sentiment"] == "Bullish"])
    col3.metric("Bullish Sentiment Stocks", f"{bullish_count} / {len(df)}")

    st.divider()

    # Main Data Table
    st.subheader("📋 Master Trade Setups Table")
    st.dataframe(df, use_container_width=True)

    st.divider()

    # Visual Bar Chart
    st.subheader("📈 3-Month Momentum Comparison (%)")
    st.bar_chart(data=df, x="Ticker", y="3M Momentum (%)")

else:
    st.info(
        "👋 No existing report found. Click **'⚡ Run Fresh Pipeline Scan'** in the sidebar on the left to start!"
    )

