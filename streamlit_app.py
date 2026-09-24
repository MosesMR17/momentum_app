import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

# Ensure root directory is in python path for cloud imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.backtest.engine import run_momentum_backtest

# --- Page Config ---
st.set_page_config(page_title="Quantitative Momentum Dashboard", layout="wide")

st.title("📈 Quantitative Momentum & Backtest Engine")
st.write("Welcome to your institutional-grade momentum screening and backtesting platform.")

# --- Section 1: Master Trade Setups & Report ---
st.subheader("📊 Latest Active Report: Quantitative Momentum")
st.caption("Active Report Date: 2026-09-24")
st.markdown("Top 15 institutional market leaders ranked by trailing 3-month quantitative momentum with actionable trade parameters.")

mock_leaders = pd.DataFrame({
    "Ticker": ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "AMD", "AVGO", "JPM", "XOM", "COST", "LLY", "UNH"],
    "3M Momentum (%)": ["+34.2%", "+52.8%", "+28.5%", "+25.1%", "+31.4%", "+45.6%", "+22.3%", "+29.8%", "+41.2%", "+38.7%", "+15.4%", "+18.9%", "+20.5%", "+33.1%", "+16.2%"],
    "Sentiment": ["Bullish", "Very Bullish", "Bullish", "Neutral", "Bullish", "Very Bullish", "Watch", "Bullish", "Very Bullish", "Bullish", "Neutral", "Neutral", "Bullish", "Very Bullish", "Neutral"],
    "Entry ($)": [225.50, 118.20, 420.00, 175.30, 185.00, 510.40, 240.00, 650.00, 155.80, 1420.50, 195.00, 115.40, 850.20, 920.00, 525.00],
    "Stop Loss ($)": [214.00, 110.00, 400.00, 168.00, 176.00, 485.00, 225.00, 615.00, 148.00, 1350.00, 188.00, 110.00, 815.00, 880.00, 500.00],
    "Target ($)": [250.00, 140.00, 460.00, 195.00, 205.00, 570.00, 275.00, 720.00, 175.00, 1580.00, 215.00, 128.00, 920.00, 1020.00, 580.00],
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
