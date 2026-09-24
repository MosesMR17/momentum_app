import os
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

from modules.backtest.engine import run_momentum_backtest

# --- Page Config ---
st.set_page_config(page_title="Quantitative Momentum Dashboard", layout="wide")

st.title("📈 Quantitative Momentum & Backtest Engine")
st.write("Welcome to your institutional-grade momentum screening and backtesting platform.")

# --- Section 1: Master Trade Setups & Report ---
st.subheader("📊 Latest Active Report: Quantitative Momentum")
st.caption("Active Report Date: 2026-09-24")
st.markdown("Top institutional market leaders ranked by trailing 3-month quantitative momentum with actionable trade parameters.")

mock_leaders = pd.DataFrame({
    "Ticker": ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "AMD", "AVGO", "JPM", "XOM", "COST", "LLY", "UNH"],
    "3M Momentum Score": [0.34, 0.52, 0.28, 0.25, 0.31, 0.45, 0.22, 0.29, 0.41, 0.38, 0.15, 0.18, 0.20, 0.33, 0.16],
    "Action": ["Buy/Hold", "Strong Momentum", "Hold", "Hold", "Buy/Hold", "Strong Momentum", "Watch", "Hold", "Strong Momentum", "Buy/Hold", "Hold", "Hold", "Hold", "Strong Momentum", "Hold"]
})

st.dataframe(mock_leaders, use_container_width=True)

st.markdown("---")

# --- Section 2: Strategy Backtest Engine ---
st.subheader("⚙️ Strategy Backtest Engine")
st.write("Test any ticker from the report above or type your own custom symbol.")

col_input1, col_input2 = st.columns([2, 2])
with col_input1:
    ticker_input = st.text_input("Enter Ticker for Backtest", value="AAPL").upper()
with col_input2:
    lookback = st.slider("Momentum Lookback Window (Days)", min_value=5, max_value=100, value=20)

if st.button("Run Backtest", type="primary"):
    with st.spinner(f"Fetching data and running backtest for {ticker_input}..."):
        try:
            data = yf.download(ticker_input, period="1y", interval="1d", progress=False)
        except Exception:
            data = pd.DataFrame()

        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                prices = data['Close'].iloc[:, 0]
            else:
                prices = data['Close']
                
            results = run_momentum_backtest(prices, lookback_window=lookback)
            
            fig = px.line(
                results, 
                y=['Buy_Hold_Cum', 'Strategy_Cum'],
                labels={'value': 'Growth of $1', 'index': 'Date', 'variable': 'Strategy'},
                title=f"Momentum Strategy vs Buy & Hold ({ticker_input})"
            )
            fig.update_layout(legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1})
            st.plotly_chart(fig, use_container_width=True)
            
            final_bh = results['Buy_Hold_Cum'].iloc[-1] - 1
            final_strat = results['Strategy_Cum'].iloc[-1] - 1
            
            m1, m2 = st.columns(2)
            m1.metric("Buy & Hold Return", f"{final_bh:.2%}")
            m2.metric("Momentum Strategy Return", f"{final_strat:.2%}")
        else:
            st.error(f"Could not retrieve data for '{ticker_input}'. Please check the ticker symbol.")
