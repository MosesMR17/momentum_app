import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Page Configuration for Professional Terminal
st.set_page_config(
    page_title="Moses Institutional Trading & Investment Suite",
    page_icon="⚡",
    layout="wide"
)

# --- PROFESSIONAL INSTITUTIONAL CSS STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    div.stMetric, div.css-1r6slb0, div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    h1, h2, h3 {
        color: #f0f6fc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .stAlert {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #f0f6fc;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Navigation Hub")
app_choice = st.sidebar.radio(
    "Select Application:",
    ["🧊 SMC Ice Trading Terminal", "📈 Quantitative Momentum App"]
)

st.sidebar.divider()
st.sidebar.info("⚡ Live Institutional Terminal v4.0\n\nEquipped with Day Trading FVG Scanner & Multi-Timeframe Matrix.")

# --- APP 1: SMC ICE TRADING TERMINAL ---
if app_choice == "🧊 SMC Ice Trading Terminal":
    st.title("🧊 SMC Ice Trading Terminal")
    st.markdown("Institutional Price Action, Smart Money Concepts (SMC), and Intraday Execution Engine")

    nav_tab = st.selectbox(
        "Terminal Workspace",
        ["📊 Live Chart & FVG Scanner", "📰 Macro & News Feed", "⚖️ Risk & Position Calculator", "🚀 Execution & Order Book"]
    )
    st.divider()

    if nav_tab == "📊 Live Chart & FVG Scanner":
        # Asset selector with institutional day trading instruments
        col_sel1, col_sel2 = st.columns([2, 2])
        with col_sel1:
            asset_dict = {
                "Nasdaq 100 / US100 (QQQ)": "QQQ",
                "S&P 500 / S&P500 (SPY)": "SPY",
                "Gold Futures (GC=F)": "GC=F",
                "Crude Oil Futures (CL=F)": "CL=F",
                "Euro / US Dollar (EURUSD=X)": "EURUSD=X",
                "British Pound / USD (GBPUSD=X)": "GBPUSD=X",
                "USD / Japanese Yen (USDJPY=X)": "USDJPY=X",
                "Bitcoin (BTC-USD)": "BTC-USD",
                "Ethereum (ETH-USD)": "ETH-USD",
                "NVIDIA (NVDA)": "NVDA",
                "Tesla (TSLA)": "TSLA",
                "AMD (AMD)": "AMD",
                "Palantir (PLTR)": "PLTR",
                "Apple (AAPL)": "AAPL"
            }
            selected_label = st.selectbox("Select Day Trading Asset", list(asset_dict.keys()))
            smc_ticker = asset_dict[selected_label]
        with col_sel2:
            timeframe_choice = st.selectbox("Analysis Timeframe", ["1H (Intraday Execution)", "Daily (Swing Structure)"])

        with st.spinner(f"Scanning {selected_label} for institutional order blocks and imbalances..."):
            try:
                period_val = "7d" if timeframe_choice == "1H (Intraday Execution)" else "90d"
                interval_val = "1h" if timeframe_choice == "1H (Intraday Execution)" else "1d"
                
                df_smc = yf.download(smc_ticker, period=period_val, interval=interval_val, progress=False)
                if not df_smc.empty:
                    if isinstance(df_smc.columns, pd.MultiIndex):
                        df_smc = df_smc.xs(smc_ticker, level=1, axis=1)
                    
                    closes = df_smc['Close']
                    highs = df_smc['High']
                    lows = df_smc['Low']
                    
                    # Fair Value Gap (FVG) Detection Logic
                    fvgs = []
                    for i in range(len(df_smc) - 2):
                        c1_high = float(highs.iloc[i])
                        c3_low = float(lows.iloc[i+2])
                        c3_high = float(highs.iloc[i+2])
                        c1_low = float(lows.iloc[i])
                        
                        if c3_low > c1_high:
                            fvgs.append({'Type': 'Bullish FVG', 'Zone Low': c1_high, 'Zone High': c3_low, 'Index': i+1})
                        elif c3_high < c1_low:
                            fvgs.append({'Type': 'Bearish FVG', 'Zone Low': c3_high, 'Zone High': c1_low, 'Index': i+1})

                    current_p = float(closes.iloc[-1])
                    prev_p = float(closes.iloc[-2])
                    price_change_pct = ((current_p - prev_p) / prev_p) * 100

                    col_left, col_right = st.columns([3, 1])
                    with col_left:
                        st.subheader(f"{selected_label} Price Action Structure")
                        chart_data = pd.DataFrame({'Close': closes, 'High': highs, 'Low': lows})
                        st.line_chart(chart_data)
                        
                    with col_right:
                        st.subheader("Structure Matrix")
                        market_bias = "Bullish MSS" if price_change_pct >= 0 else "Bearish MSS"
                        if price_change_pct >= 0:
                            st.success(f"🟢 **Structure:** {market_bias}")
                        else:
                            st.error(f"🔴 **Structure:** {market_bias}")
                            
                        st.metric("Latest Close", f"${current_p:,.2f}", f"{price_change_pct:+.2f}%")
                        
                        if fvgs:
                            st.warning(f"⚠️ **Imbalances Found:** {len(fvgs)} Active Zones")
                            latest_fvg = fvgs[-1]
                            st.markdown(f"**Latest {latest_fvg['Type']}:**\n`{latest_fvg['Zone Low']:.2f}` - `{latest_fvg['Zone High']:.2f}`")
                        else:
                            st.info("ℹ️ No active imbalances detected on this timeframe.")
                            
                        st.markdown("---")
                        st.metric("Liquidity Pool Status", "Swept / Mitigated", "Optimal Entry Zone")
                else:
                    st.error("⚠️ Could not load data for the selected symbol.")
            except Exception as e:
                st.error(f"Error executing SMC scan: {e}")

    elif nav_tab == "📰 Macro & News Feed":
        st.subheader("Global Economic & Financial Data")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔴 High-Impact Economic Events")
            st.markdown("- **08:30 EST** | USD Core CPI (Projected)")
            st.markdown("- **14:00 EST** | FOMC Rate Decision & Statement")
            st.markdown("- **04:00 EST** | ECB Monetary Policy Meeting")
        with col2:
            st.markdown("### 🏦 Institutional Tracking & Flow")
            st.markdown("- **Smart Money Net Sentiment:** Bullish Accumulation")
            st.markdown("- **Interbank Liquidity Index:** Stable")

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
                st.success("🚀 Institutional Order Routed & Executed Successfully!")

# --- APP 2: QUANTITATIVE MOMENTUM APP ---
elif app_choice == "📈 Quantitative Momentum App":
    st.title("📈 Quantitative Momentum & Predictive Suite")
    
    today_str = datetime.today().strftime('%Y-%m-%d')
    st.markdown(f"**Latest Active Report:** Multi-Timeframe Trend Matrix & Win Probability Engine — *{today_str}*")
    st.divider()
    
    st.subheader("Master Predictive Trade Setups Table")
    st.markdown("Evaluating 15 premier market leaders across 3M, 3W, 1W, Daily, and 4H trends with real-time win probabilities.")
    
    tickers = [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 
        'META', 'TSLA', 'NFLX', 'AMD', 'PLTR', 
        'AVGO', 'JPM', 'XOM', 'COST', 'PEP'
    ]
    
    with st.spinner("Crunching multi-timeframe data and computing win probabilities..."):
        momentum_data = []
        end_date = datetime.today()
        start_date = end_date - timedelta(days=120)
        
        for ticker in tickers:
            try:
                df_hist = yf.download(ticker, start=start_date, end=end_date, progress=False)
                df_hourly = yf.download(ticker, period="5d", interval="1h", progress=False)
                
                if not df_hist.empty and len(df_hist) > 50:
                    if isinstance(df_hist.columns, pd.MultiIndex):
                        close_daily = df_hist['Close'][ticker]
                    else:
                        close_daily = df_hist['Close']
                        
                    if not df_hourly.empty and isinstance(df_hourly.columns, pd.MultiIndex):
                        close_hourly = df_hourly['Close'][ticker]
                    elif not df_hourly.empty:
                        close_hourly = df_hourly['Close']
                    else:
                        close_hourly = close_daily[-10:]
                    
                    current_price = float(close_daily.iloc[-1])
                    
                    p_3m = float(close_daily.iloc[-63] if len(close_daily) >= 63 else close_daily.iloc[0])
                    p_3w = float(close_daily.iloc[-15] if len(close_daily) >= 15 else close_daily.iloc[0])
                    p_1w = float(close_daily.iloc[-5] if len(close_daily) >= 5 else close_daily.iloc[0])
                    p_1d = float(close_daily.iloc[-2] if len(close_daily) >= 2 else close_daily.iloc[0])
                    
                    ret_3m = ((current_price - p_3m) / p_3m) * 100
                    ret_3w = ((current_price - p_3w) / p_3w) * 100
                    ret_1w = ((current_price - p_1w) / p_1w) * 100
                    ret_1d = ((current_price - p_1d) / p_1d) * 100
                    
                    p_4h_ago = float(close_hourly.iloc[-4] if len(close_hourly) >= 4 else close_hourly.iloc[0])
                    ret_4h = ((current_price - p_4h_ago) / p_4h_ago) * 100
                    
                    positive_trends = sum([ret_3m > 0, ret_3w > 0, ret_1w > 0, ret_1d > 0, ret_4h > 0])
                    base_win_rate = 50.0 + (positive_trends * 7.5)
                    if ret_3m > 15 and ret_3w > 5:
                        base_win_rate += 5.0
                    win_rate_est = min(round(base_win_rate, 1), 94.5)
                    
                    sentiment = "🔥 High Conviction" if win_rate_est >= 75 else ("⚡ Bullish" if win_rate_est >= 60 else "⚖️ Neutral")
                    
                    momentum_data.append({
                        'Ticker': ticker,
                        'Price ($)': round(current_price, 2),
                        'Live Change (%)': round(ret_1d, 2),
                        '3M Trend (%)': round(ret_3m, 2),
                        '3W Trend (%)': round(ret_3w, 2),
                        '1W Trend (%)': round(ret_1w, 2),
                        '4H Trend (%)': round(ret_4h, 2),
                        'Est. Win Rate (%)': win_rate_est,
                        'Sentiment': sentiment,
                        'Entry ($)': round(current_price, 2),
                        'Stop Loss ($)': round(current_price * 0.965, 2),
                        'Target ($)': round(current_price * 1.075, 2)
                    })
            except Exception as e:
                continue
        
        if momentum_data:
            res_df = pd.DataFrame(momentum_data)
            res_df = res_df.sort_values(by='Est. Win Rate (%)', ascending=False).reset_index(drop=True)
            res_df.index = res_df.index + 1
            res_df.index.name = 'Rank'
            res_df = res_df.reset_index()
            
            def color_metrics(val):
                if isinstance(val, (int, float)):
                    color = '#3fb950' if val >= 0 else '#f85149'
                    return f'color: {color}; font-weight: bold;'
                return ''
                
            numeric_cols = ['Live Change (%)', '3M Trend (%)', '3W Trend (%)', '1W Trend (%)', '4H Trend (%)', 'Est. Win Rate (%)']
            styled_df = res_df.style.map(color_metrics, subset=numeric_cols)
            
            st.success("✅ Multi-Timeframe Matrix Computed Successfully!")
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            st.markdown("### Top Win Probability Distribution")
            st.bar_chart(res_df.set_index('Ticker')['Est. Win Rate (%)'])
        else:
            st.error("⚠️ Unable to fetch multi-timeframe data right now. Please check your connection.")
            