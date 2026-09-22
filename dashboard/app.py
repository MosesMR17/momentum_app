import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
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
    div.stMetric, div[data-testid="stVerticalBlock"] > div[style*="border"] {
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

# --- ROBUST CACHED DATA FETCHER ---
@st.cache_data(ttl=60, show_spinner=False)
def get_cached_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df.empty:
        return df
    if isinstance(df.columns, pd.MultiIndex):
        try:
            df = df.xs(ticker, level=1, axis=1)
        except Exception:
            try:
                df = df.xs(ticker, level=0, axis=1)
            except Exception:
                pass
    return df

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧭 Navigation Hub")
app_choice = st.sidebar.radio(
    "Select Application:",
    ["🧊 SMC Ice Trading Terminal", "📈 Quantitative Momentum App"]
)

st.sidebar.divider()
st.sidebar.info("⚡ Live Institutional Terminal v5.7\n\nEquipped with Styled Financial Tables.")

# --- APP 1: SMC ICE TRADING TERMINAL ---
if app_choice == "🧊 SMC Ice Trading Terminal":
    st.title("🧊 SMC Ice Trading Terminal")
    st.markdown("Institutional Price Action, Smart Money Concepts (SMC), PO3 Schematics & Liquidity Mapping Engine")

    nav_tab = st.selectbox(
        "Terminal Workspace",
        ["📊 Live SMC Chart & PO3 Suite", "📰 Macro & News Feed", "⚖️ Risk & Position Calculator", "🚀 Execution & Order Book"]
    )
    st.divider()

    if nav_tab == "📊 Live SMC Chart & PO3 Suite":
        col_sel1, col_sel2 = st.columns([2, 2])
        with col_sel1:
            asset_dict = {
                "Nasdaq 100 / US100 (QQQ)": "QQQ",
                "S&P 500 / S&P500 (SPY)": "SPY",
                "Gold Futures (GC=F)": "GC=F",
                "Crude Oil Futures (CL=F)": "CL=F",
                "Euro / US Dollar (EURUSD=X)": "EURUSD=X",
                "British Pound / USD (GBPUSD=X)": "GBPUSD=X",
                "Bitcoin (BTC-USD)": "BTC-USD",
                "Ethereum (ETH-USD)": "ETH-USD",
                "NVIDIA (NVDA)": "NVDA",
                "Tesla (TSLA)": "TSLA"
            }
            selected_label = st.selectbox("Select Day Trading Asset", list(asset_dict.keys()))
            smc_ticker = asset_dict[selected_label]
            
        with col_sel2:
            tf_options = {
                "1 Year (1Y)": {"period": "1y", "interval": "1d"},
                "6 Months (6M)": {"period": "6mo", "interval": "1d"},
                "3 Months (3M)": {"period": "3mo", "interval": "1d"},
                "3 Weeks (3W)": {"period": "1mo", "interval": "1d"},
                "1 Week (1W)": {"period": "7d", "interval": "1h"},
                "Daily (1D)": {"period": "60d", "interval": "1d"},
                "4 Hour (4H)": {"period": "60d", "interval": "60m"},
                "3 Hour (3H)": {"period": "60d", "interval": "60m"},
                "1 Hour (1H)": {"period": "30d", "interval": "1h"},
                "Half Hour (30m)": {"period": "15d", "interval": "30m"},
                "15 Minutes (15m)": {"period": "10d", "interval": "15m"},
                "5 Minutes (5m)": {"period": "5d", "interval": "5m"},
                "1 Minute (1m)": {"period": "1d", "interval": "1m"}
            }
            selected_tf_label = st.selectbox("Professional Timeframe", list(tf_options.keys()))
            fetch_params = tf_options[selected_tf_label]

        with st.spinner(f"Computing SMC analytics for {selected_label} ({selected_tf_label})..."):
            try:
                df_smc = get_cached_data(smc_ticker, fetch_params["period"], fetch_params["interval"])
                
                if not df_smc.empty:
                    df_smc = df_smc.dropna()
                    opens = df_smc['Open'].squeeze()
                    highs = df_smc['High'].squeeze()
                    lows = df_smc['Low'].squeeze()
                    closes = df_smc['Close'].squeeze()
                    
                    pdh = float(highs.max())
                    pdl = float(lows.min())
                    
                    bsl_swept = any(highs > pdh)
                    ssl_swept = any(lows < pdl)
                    
                    fvgs = []
                    for i in range(len(df_smc) - 2):
                        c1_high = float(highs.iloc[i])
                        c3_low = float(lows.iloc[i+2])
                        c3_high = float(highs.iloc[i+2])
                        c1_low = float(lows.iloc[i])
                        
                        if c3_low > c1_high:
                            fvgs.append({'Type': 'Bullish FVG', 'Low': c1_high, 'High': c3_low})
                        elif c3_high < c1_low:
                            fvgs.append({'Type': 'Bearish FVG', 'Low': c3_high, 'High': c1_low})

                    bullish_obs, bearish_obs = [], []
                    for i in range(1, len(df_smc) - 1):
                        body_prev = float(closes.iloc[i-1]) - float(opens.iloc[i-1])
                        body_curr = float(closes.iloc[i]) - float(opens.iloc[i])
                        if body_prev < 0 and body_curr > 0:
                            bullish_obs.append({'Time': df_smc.index[i-1], 'Low': float(lows.iloc[i-1]), 'High': float(highs.iloc[i-1])})
                        elif body_prev > 0 and body_curr < 0:
                            bearish_obs.append({'Time': df_smc.index[i-1], 'Low': float(lows.iloc[i-1]), 'High': float(highs.iloc[i-1])})

                    recent_trend = closes.iloc[-1] - closes.iloc[-min(5, len(closes))]
                    mss_status = "Bullish Structure" if recent_trend >= 0 else "Bearish Structure"
                    
                    third_len = max(1, len(df_smc) // 3)
                    acc_zone = closes.iloc[:third_len].mean()
                    manip_zone = lows.iloc[third_len:2*third_len].min() if recent_trend >= 0 else highs.iloc[third_len:2*third_len].max()
                    dist_zone = closes.iloc[2*third_len:].max() if recent_trend >= 0 else closes.iloc[2*third_len:].min()

                    current_p = float(closes.iloc[-1])
                    prev_p = float(closes.iloc[-2]) if len(closes) > 1 else current_p
                    price_change_pct = ((current_p - prev_p) / prev_p) * 100 if prev_p > 0 else 0.0

                    col_left, col_right = st.columns([3, 1])
                    
                    with col_left:
                        st.subheader(f"{selected_label} — {selected_tf_label} Chart")
                        
                        fig = go.Figure()
                        fig.add_trace(go.Candlestick(
                            x=df_smc.index,
                            open=opens,
                            high=highs,
                            low=lows,
                            close=closes,
                            increasing_line_color='#26a69a',
                            decreasing_line_color='#ef5350',
                            name="Candles"
                        ))
                        
                        fig.add_hline(y=pdh, line_dash="dash", line_color="#26a69a", annotation_text="PDH / BSL", annotation_position="top left")
                        fig.add_hline(y=pdl, line_dash="dash", line_color="#ef5350", annotation_text="PDL / SSL", annotation_position="bottom left")

                        fig.update_layout(
                            template="plotly_dark",
                            paper_bgcolor="#0e1117",
                            plot_bgcolor="#161b22",
                            margin=dict(l=20, r=20, t=20, b=20),
                            height=580,
                            xaxis_rangeslider_visible=False,
                            yaxis_title="Price ($)"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                    with col_right:
                        st.subheader("Structure Matrix")
                        if price_change_pct >= 0:
                            st.success(f"🟢 **Bias:** {mss_status}")
                        else:
                            st.error(f"🔴 **Bias:** {mss_status}")
                            
                        st.metric("Latest Price", f"${current_p:,.2f}", f"{price_change_pct:+.2f}%")
                        
                        st.markdown("### 🌊 Liquidity Pools")
                        st.write(f"• **Buy-Side (PDH):** {'⚡ Swept' if bsl_swept else '🔒 Intact'}")
                        st.write(f"• **Sell-Side (PDL):** {'⚡ Swept' if ssl_swept else '🔒 Intact'}")
                        
                        st.markdown("### 🧩 SMC Diagnostics")
                        st.write(f"• **Active FVGs:** `{len(fvgs)} Zones`")
                        st.write(f"• **Order Blocks:** `{len(bullish_obs) + len(bearish_obs)} Detected`")
                        
                        st.markdown("### ⚙️ Power of 3 (PO3)")
                        st.write(f"• **Accumulation:** `${acc_zone:,.2f}`")
                        st.write(f"• **Manipulation:** `${manip_zone:,.2f}`")
                        st.write(f"• **Distribution:** `${dist_zone:,.2f}`")
                        
                else:
                    st.error("⚠️ No market data returned for this timeframe/asset combination.")
            except Exception as e:
                st.error(f"Error rendering chart: {e}")

    elif nav_tab == "📰 Macro & News Feed":
        st.subheader("Global Economic & Financial Data")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔴 High-Impact Events")
            st.markdown("- **08:30 EST** | USD Core CPI")
            st.markdown("- **14:00 EST** | FOMC Rate Statement")
        with col2:
            st.markdown("### 🏦 Institutional Flow")
            st.markdown("- **Smart Money Sentiment:** Accumulation")

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
    st.title("📈 Quantitative Momentum Investing App")
    
    # Header report style
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
    
    with st.spinner("Generating professional master momentum trade setups..."):
        momentum_data = []
        
        for ticker in tickers:
            try:
                df_hist = get_cached_data(ticker, "4mo", "1d")
                if not df_hist.empty:
                    close_col = df_hist['Close']
                    if isinstance(close_col, pd.DataFrame):
                        close_prices = close_col.iloc[:, 0]
                    else:
                        close_prices = close_col
                    
                    close_prices = close_prices.dropna()
                    if len(close_prices) > 20:
                        current_price = float(close_prices.iloc[-1])
                        lookback_idx = -63 if len(close_prices) >= 63 else 0
                        price_3m_ago = float(close_prices.iloc[lookback_idx])
                        ret_3m = ((current_price - price_3m_ago) / price_3m_ago) * 100
                        
                        sentiment = "🔥 Strong Bullish" if ret_3m > 10 else ("🚀 Bullish" if ret_3m > 0 else "⚖️ Neutral")
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
            
            # --- PROFESSIONAL TABLE STYLING VIA PANDAS STYLER ---
            def color_momentum(val):
                color = '#26a69a' if val > 0 else '#ef5350'
                return f'color: {color}; font-weight: bold;'

            styled_df = res_df.style.applymap(
                color_momentum, subset=['3M Momentum (%)']
            ).format({
                '3M Momentum (%)': '{:+.2f}%',
                'Entry ($)': '${:,.2f}',
                'Stop Loss ($)': '${:,.2f}',
                'Target ($)': '${:,.2f}'
            })

            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            st.markdown("### 3M Momentum Performance Distribution")
            st.bar_chart(res_df.set_index('Ticker')['3M Momentum (%)'])
        else:
            st.error("⚠️ Unable to fetch live data right now. Please check your network connection.")
            




