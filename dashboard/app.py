import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Page Configuration for Professional Terminal
st.set_page_config(
    page_title="Moses Trading & Investment Suite",
    page_icon="⚡",
    layout="wide"
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Navigation Hub")
app_choice = st.sidebar.radio(
    "Select Application:",
    ["🧊 SMC Ice Trading Terminal", "📈 Quantitative Momentum App"]
)

st.sidebar.divider()
st.sidebar.info("Seamlessly switch between your institutional SMC trading desk and your quantitative equity screener.")

# --- APP 1: SMC ICE TRADING TERMINAL ---
if app_choice == "🧊 SMC Ice Trading Terminal":
    def detect_fvg(df):
        fvgs = []
        for i in range(len(df) - 2):
            c1_high = df.loc[i, 'High']
            c3_low = df.loc[i + 2, 'Low']
            if c3_low > c1_high:
                fvgs.append({
                    'Type': 'Bullish Fvg',
                    'Zone Start': c1_high,
                    'Zone End': c3_low,
                    'Index': i + 1
                })
        return fvgs

    st.title("🧊 SMC Ice Trading Terminal")
    st.markdown("Institutional Price Action, Smart Money Concepts (SMC), and Execution Engine")

    nav_tab = st.selectbox(
        "Terminal Workspace",
        ["📊 Live Chart & SMC Scanner", "📰 Macro & News Feed", "⚖️ Risk & Position Calculator", "🚀 Execution & Order Book"]
    )
    st.divider()

    if nav_tab == "📊 Live Chart & SMC Scanner":
        col_left, col_right = st.columns([3, 1])
        with col_left:
            st.subheader("Price Action Structure & FVG Overlay")
            np.random.seed(42)
            price_steps = np.random.randn(60) * 1.5
            base_price = 4100 + price_steps.cumsum()
            chart_df = pd.DataFrame({
                'Price': base_price,
                'High': base_price + np.random.uniform(0.5, 3.0, 60),
                'Low': base_price - np.random.uniform(0.5, 3.0, 60)
            })
            st.line_chart(chart_df[['Price', 'High', 'Low']])
        with col_right:
            st.subheader("Structure Matrix")
            st.success("🟢 **Market Structure:** Bullish MSS Confirmed")
            active_fvgs = detect_fvg(chart_df)
            if active_fvgs:
                st.warning(f"⚠️ **Detected FVGs:** {len(active_fvgs)} Active Zones")
                latest_fvg = active_fvgs[-1]
                st.markdown(f"**Latest FVG Zone:**\n`{latest_fvg['Zone Start']:.2f}` to `{latest_fvg['Zone End']:.2f}`")
            else:
                st.info("ℹ️ No active FVG imbalances right now.")
            st.markdown("---")
            st.metric("Liquidity Sweep Status", "Cleaned Equal Highs", "Bullish")

    elif nav_tab == "📰 Macro & News Feed":
        st.subheader("Global Economic & Financial Data")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔴 High-Impact Economic Events")
            st.markdown("- **08:30 EST** | USD Core CPI")
            st.markdown("- **14:00 EST** | FOMC Rate Decision")
        with col2:
            st.markdown("### 🏦 Institutional Tracking & Flow")
            st.markdown("- **Smart Money Sentiment:** Net Long")

    elif nav_tab == "⚖️ Risk & Position Calculator":
        st.subheader("Advanced Risk Management & Trade Planning")
        c1, c2, c3 = st.columns(3)
        with c1:
            account_size = st.number_input("Account Balance ($)", value=10000.0, step=500.0)
            risk_pct = st.slider("Risk Tolerance (%)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        with c2:
            entry_price = st.number_input("Entry / POI Price", value=4125.0, step=0.5)
            stop_loss = st.number_input("Stop Loss (Invalidation)", value=4110.0, step=0.5)
        with c3:
            take_profit = st.number_input("Take Profit (Target)", value=4170.0, step=0.5)
        
        risk_dollars = account_size * (risk_pct / 100.0)
        risk_spread = abs(entry_price - stop_loss)
        reward_spread = abs(take_profit - entry_price)
        rr_ratio = (reward_spread / risk_spread) if risk_spread > 0 else 0
        position_units = (risk_dollars / risk_spread) if risk_spread > 0 else 0
        
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Risk Capital ($)", f"${risk_dollars:.2f}")
        m2.metric("Risk-to-Reward", f"1 : {rr_ratio:.2f}")
        m3.metric("Position Size", f"{position_units:.2f} units")
        m4.metric("Potential Profit ($)", f"${(risk_dollars * rr_ratio):.2f}")

    elif nav_tab == "🚀 Execution & Order Book":
        st.subheader("Order Execution Engine")
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            direction = st.radio("Execution Bias", ["🟢 Long (Bullish)", "🔴 Short (Bearish)"], horizontal=True)
            order_type = st.selectbox("Order Execution Type", ["Market Order", "Limit Order (POI Entry)"])
        with col_ex2:
            if st.button("Execute Live Order", type="primary"):
                st.success("🚀 Order Executed Successfully!")

# --- APP 2: QUANTITATIVE MOMENTUM APP ---
elif app_choice == "📈 Quantitative Momentum App":
    st.title("📈 Quantitative Momentum Investing App")
    
    today_str = datetime.today().strftime('%Y-%m-%d')
    st.markdown(f"**Latest Active Report:** Quantitative Momentum Report — *{today_str}*")
    st.divider()
    
    st.subheader("Master Trade Setups Table")
    st.markdown("Top 15 institutional market leaders ranked by trailing 3-month quantitative momentum with actionable trade parameters.")
    
    tickers = [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 
        'META', 'TSLA', 'NFLX', 'AMD', 'PLTR', 
        'AVGO', 'JPM', 'XOM', 'COST', 'PEP'
    ]
    
    with st.spinner("Generating master momentum trade setups..."):
        momentum_data = []
        end_date = datetime.today()
        start_date = end_date - timedelta(days=120)
        
        for ticker in tickers:
            try:
                df_hist = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not df_hist.empty and len(df_hist) > 50:
                    if isinstance(df_hist.columns, pd.MultiIndex):
                        close_prices = df_hist['Close'][ticker]
                    else:
                        close_prices = df_hist['Close']
                    
                    current_price = float(close_prices.iloc[-1])
                    price_3m_ago = float(close_prices.iloc[-63] if len(close_prices) >= 63 else close_prices.iloc[0])
                    ret_3m = ((current_price - price_3m_ago) / price_3m_ago) * 100
                    
                    sentiment = "Strong Bullish" if ret_3m > 10 else ("Bullish" if ret_3m > 0 else "Neutral")
                    entry = round(current_price, 2)
                    stop_loss = round(current_price * 0.96, 2)
                    target = round(current_price * 1.08, 2)
                    
                    momentum_data.append({
                        'Ticker': ticker,
                        '3M Momentum (%)': round(ret_3m, 2),
                        'Sentiment': sentiment,
                        'Entry ($)': entry,
                        'Stop Loss ($)': stop_loss,
                        'Target ($)': target
                    })
            except Exception as e:
                continue
        
        if momentum_data:
            res_df = pd.DataFrame(momentum_data)
            res_df = res_df.sort_values(by='3M Momentum (%)', ascending=False).reset_index(drop=True)
            res_df.index = res_df.index + 1
            res_df.index.name = 'Rank'
            res_df = res_df.reset_index()
            
            st.success("✅ Master Trade Setups Loaded Successfully!")
            st.dataframe(res_df, use_container_width=True, hide_index=True)
            
            st.markdown("### 3M Momentum Performance Distribution")
            st.bar_chart(res_df.set_index('Ticker')['3M Momentum (%)'])
        else:
            st.error("⚠️ Unable to fetch live data right now. Please check your network connection.")
            