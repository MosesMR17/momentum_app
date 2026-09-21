import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration for Professional Terminal
st.set_page_config(
    page_title="SMC Ice Trading Terminal",
    page_icon="🧊",
    layout="wide"
)

# Custom Styling & Header
st.title("🧊 SMC Ice Trading Terminal")
st.markdown("Institutional Price Action, Smart Money Concepts (SMC), and Execution Engine")

# Main Navigation Hub
nav_tab = st.selectbox(
    "Terminal Workspace",
    ["📊 Live Chart & SMC Scanner", "📰 Macro & News Feed", "⚖️ Risk & Position Calculator", "🚀 Execution & Order Book"]
)

st.divider()

# --- WORKSPACE 1: CHARTS & SMC SCANNER ---
if nav_tab == "📊 Live Chart & SMC Scanner":
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.subheader("Price Action Structure (1H / 4H)")
        st.info("Interactive Candlestick & Liquidity Sweep Module Loading...")
        
        # Mock price chart visualization
        chart_df = pd.DataFrame(
            np.random.randn(60, 2).cumsum(axis=0) + 100,
            columns=['Price', 'Institutional Benchmark']
        )
        st.line_chart(chart_df)
        
    with col_right:
        st.subheader("Structure Matrix")
        st.success("🟢 **Market Structure:** Bullish MSS Confirmed")
        st.warning("⚠️ **Active FVG:** 4,120.50 - 4,135.00")
        st.info("ℹ️ **PO3 Phase:** Manipulation / Expansion")
        st.markdown("---")
        st.metric("Liquidity Sweep Status", "Cleaned Equal Highs", "Bullish")

# --- WORKSPACE 2: MACRO & NEWS FEED ---
elif nav_tab == "📰 Macro & News Feed":
    st.subheader("Global Economic & Financial Data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔴 High-Impact Economic Events")
        st.markdown("- **08:30 EST** | USD Core CPI (Actual: 3.2% | Forecast: 3.1%)")
        st.markdown("- **14:00 EST** | FOMC Rate Decision & Press Conference")
        st.markdown("- **20:30 EST** | AUD Employment Change")
        
    with col2:
        st.markdown("### 🏦 Institutional Tracking & Flow")
        st.markdown("- **Smart Money Sentiment:** Net Long (Energy & Commodities)")
        st.markdown("- **Retail Sentiment:** 74% Short (Contrarian Bullish Signal)")
        st.markdown("- **Order Block Mitigations:** 3 Active zones tested today")

# --- WORKSPACE 3: RISK & POSITION CALCULATOR ---
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
        
    # Calculations
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

# --- WORKSPACE 4: EXECUTION & ORDER BOOK ---
elif nav_tab == "🚀 Execution & Order Book":
    st.subheader("Order Execution Engine")
    
    col_ex1, col_ex2 = st.columns(2)
    
    with col_ex1:
        direction = st.radio("Execution Bias", ["🟢 Long (Bullish)", "🔴 Short (Bearish)"], horizontal=True)
        order_type = st.selectbox("Order Execution Type", ["Market Order", "Limit Order (POI Entry)", "Stop Entry"])
        timeframe = st.selectbox("Execution Timeframe", ["1m", "5m", "15m", "1H", "4H"])
        
    with col_ex2:
        st.markdown("### Order Summary")
        st.markdown(f"- **Bias:** {direction}")
        st.markdown(f"- **Type:** {order_type}")
        st.markdown(f"- **Timeframe:** {timeframe}")
        
        if st.button("Execute Live Order", type="primary"):
            if "Long" in direction:
                st.success("🚀 Long Order Executed Successfully across Liquidity Zone!")
            else:
                st.error("📉 Short Order Executed Successfully at Supply Zone!")