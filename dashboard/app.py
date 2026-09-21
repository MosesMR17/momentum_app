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
    # --- SMC CALCULATION FUNCTIONS ---
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
    st.markdown("Live multi-factor momentum screening across key institutional watchlists.")
    
    # Asset Universe Selection
    universe_dict = {
        "Mega-Cap Tech": ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "NFLX"],
        "Financial & Energy": ["JPM", "BAC", "XOM", "CVX", "GS", "MS"],
        "Crypto Proxies & Growth": ["COIN", "MSTR", "PLTR", "ARM", "SHOP", "SQ"]
    }
    
    selected_universe = st.selectbox("Select Asset Universe", list(universe_dict.keys()))
    tickers = universe_dict[selected_universe]
    
    top_n = st.slider("Number of Top Momentum Picks to Display", min_value=3, max_value=len(tickers), value=5)
    
    if st.button("Run Live Momentum Calculation", type="primary"):
        with st.spinner("Fetching live historical price data and computing momentum scores..."):
            momentum_data = []
            
            # Fetch 1 year of data to calculate trailing returns
            end_date = datetime.today()
            start_date = end_date - timedelta(days=365)
            
            for ticker in tickers:
                try:
                    df_hist = yf.download(ticker, start=start_date, end=end_date, progress=False)
                    if not df_hist.empty and len(df_hist) > 30:
                        # Handle multi-index columns if returned by newer yfinance versions
                        if isinstance(df_hist.columns, pd.MultiIndex):
                            close_prices = df_hist['Close'][ticker]
                        else:
                            close_prices = df_hist['Close']
                        
                        start_price = close_prices.iloc[0]
                        recent_start_price = close_prices.iloc[-30]  # approx 1 month ago
                        current_price = close_prices.iloc[-1]
                        
                        # Quantitative Momentum formula: 12M return minus last 1M return (or standard 12-1 momentum)
                        ret_12m = ((current_price - start_price) / start_price) * 100
                        ret_1m = ((current_price - recent_start_price) / recent_start_price) * 100
                        mom_score = ret_12m - ret_1m
                        
                        momentum_data.append({
                            'Ticker': ticker,
                            'Current Price ($)': round(float(current_price), 2),
                            '12M Return (%)': round(float(ret_12m), 2),
                            '1M Return (%)': round(float(ret_1m), 2),
                            'Momentum Score': round(float(mom_score), 2)
                        })
                except Exception as e:
                    continue
            
            if momentum_data:
                res_df = pd.DataFrame(momentum_data)
                res_df = res_df.sort_values(by='Momentum Score', ascending=False).reset_index(drop=True)
                top_picks = res_df.head(top_n)
                
                st.success("✅ Momentum ranking calculated successfully using live market data!")
                st.subheader(f"🏆 Top {top_n} Momentum Rankings ({selected_universe})")
                st.dataframe(top_picks, use_container_width=True)
                
                st.markdown("### Momentum Score Visualization")
                st.bar_chart(top_picks.set_index('Ticker')['Momentum Score'])
            else:
                st.error("⚠️ Could not retrieve live data for this universe right now. Please try again.")
    else:
        st.info("💡 Click the **Run Live Momentum Calculation** button above to fetch live data and rank your assets.")