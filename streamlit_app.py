import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

# --- Page Config ---
st.set_page_config(page_title="Quantitative Momentum & SMC Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- High-Tech Terminal CSS Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .stTextInput input, .stSlider {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ QUANTITATIVE MOMENTUM & SMC TERMINAL")
st.markdown("---")

# --- Helper Functions for SMC & Momentum Scanning ---
@st.cache_data
def fetch_market_leaders():
    tickers = ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "AMD", "AVGO", "JPM", "XOM", "COST", "LLY", "UNH"]
    report_data = []
    
    for t in tickers:
        try:
            df = yf.download(t, period="6mo", interval="1d", progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex):
                    close = df['Close'].iloc[:, 0]
                    high = df['High'].iloc[:, 0]
                    low = df['Low'].iloc[:, 0]
                else:
                    close = df['Close']
                    high = df['High']
                    low = df['Low']
                
                curr_price = float(close.iloc[-1])
                mom_3m = float((close.iloc[-1] / close.iloc[-60] - 1) * 100) if len(close) >= 60 else 0.0
                
                # SMC Structural Calculations & Order Block Metrics
                recent_high = float(high.iloc[-20:].max())
                recent_low = float(low.iloc[-20:].min())
                bos_status = "BOS Bullish Break" if curr_price >= recent_high * 0.99 else "Mitigation Zone"
                
                sentiment = "Very Bullish" if mom_3m > 30 else ("Bullish" if mom_3m > 10 else "Neutral")
                entry = round(curr_price, 2)
                stop_loss = round(recent_low * 0.98, 2)
                target = round(curr_price * 1.12, 2)
                
                report_data.append({
                    "Ticker": t,
                    "3M Momentum (%)": f"{mom_3m:+.1f}%",
                    "SMC Structure": bos_status,
                    "Sentiment": sentiment,
                    "Entry ($)": entry,
                    "Stop Loss ($)": stop_loss,
                    "Target ($)": target,
                    "Action": "Strong Momentum" if mom_3m > 25 else "Hold / Accumulate"
                })
        except Exception:
            continue
            
    return pd.DataFrame(report_data)

def run_momentum_backtest(prices, lookback_window=20):
    df = pd.DataFrame(index=prices.index)
    df['Price'] = prices
    df['Return'] = df['Price'].pct_change()
    df['Momentum'] = df['Price'].pct_change(lookback_window)
    df['Signal'] = 0
    df.loc[df['Momentum'] > 0, 'Signal'] = 1
    df['Strategy_Return'] = df['Signal'].shift(1) * df['Return']
    
    df['Buy_Hold_Cum'] = (1 + df['Return'].fillna(0)).cumprod()
    df['Strategy_Cum'] = (1 + df['Strategy_Return'].fillna(0)).cumprod()
    return df.dropna()

# --- Unified Multi-Tab Layout on One Page ---
tab1, tab2 = st.tabs(["📊 LIVE SMC TERMINAL & SCREENER", "⚙️ QUANTITATIVE BACKTEST ENGINE"])

with tab1:
    st.subheader("Institutional Order Block & Liquidity Tracking")
    st.caption("Real-time market scanning incorporating BOS structural breaks and quantitative momentum ratings.")

    with st.spinner("Executing live institutional data stream..."):
        df_leaders = fetch_market_leaders()

    if not df_leaders.empty:
        def highlight_table(row):
            if row['Sentiment'] == 'Very Bullish':
                return ['background-color: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: bold;'] * len(row)
            elif row['Sentiment'] == 'Bullish':
                return ['background-color: rgba(59, 130, 246, 0.15); color: #60a5fa;'] * len(row)
            return ['color: #cbd5e1;'] * len(row)

        styled_df = df_leaders.style.apply(highlight_table, axis=1)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.error("Unable to load live market data feeds at the moment.")

with tab2:
    st.subheader("Strategy Simulation & Performance Analytics")
    st.write("Backtest quantitative momentum strategies against traditional Buy & Hold benchmarks.")

    col_input1, col_input2 = st.columns([2, 2])
    with col_input1:
        ticker_input = st.text_input("Target Ticker Symbol", value="NVDA").upper()
    with col_input2:
        lookback = st.slider("Lookback Window (Days)", min_value=5, max_value=100, value=20)

    if st.button("RUN SIMULATION", type="primary"):
        with st.spinner(f"Simulating quantitative algorithms for {ticker_input}..."):
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
                    title=f"SMC Momentum Strategy vs Buy & Hold ({ticker_input})"
                )
                fig.update_layout(
                    plot_bgcolor='#0b0f19',
                    paper_bgcolor='#0b0f19',
                    font_color='#e2e8f0',
                    legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                final_bh = results['Buy_Hold_Cum'].iloc[-1] - 1
                final_strat = results['Strategy_Cum'].iloc[-1] - 1
                
                m1, m2 = st.columns(2)
                with m1:
                    st.metric("Buy & Hold Benchmark", f"{final_bh:.2%}")
                with m2:
                    st.metric("SMC Strategy Alpha", f"{final_strat:.2%}")
            else:
                st.error(f"Could not retrieve ticker data for '{ticker_input}'. Please check symbol validity.")
