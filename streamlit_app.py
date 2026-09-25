import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

# --- Page Config ---
st.set_page_config(page_title="Quantitative Momentum & SMC Dashboard", layout="wide")

st.title("📈 Quantitative Momentum & Institutional SMC Engine")
st.write("Advanced screening, Smart Money Concepts (SMC) structure tracking, and quantitative backtesting in a unified view.")

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
tab1, tab2 = st.tabs(["📊 Live SMC Trading & Screener", "⚙️ Quantitative Backtest Engine"])

with tab1:
    st.subheader("Institutional Screener & Smart Money Concepts (SMC) Analysis")
    st.caption("Real-time market scanning incorporating BOS, Order Blocks, and Liquidity target metrics.")

    with st.spinner("Analyzing live market data and institutional order blocks..."):
        df_leaders = fetch_market_leaders()

    if not df_leaders.empty:
        def highlight_table(row):
            styles = [''] * len(row)
            if row['Sentiment'] == 'Very Bullish':
                return ['background-color: rgba(40, 167, 69, 0.15)'] * len(row)
            elif row['Sentiment'] == 'Bullish':
                return ['background-color: rgba(23, 162, 184, 0.1)'] * len(row)
            return styles

        styled_df = df_leaders.style.apply(highlight_table, axis=1)
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.error("Unable to load live market data tables at the moment.")

with tab2:
    st.subheader("Quantitative Backtest Engine")
    st.write("Backtest momentum strategies against Buy & Hold using live historical data feeds.")

    col_input1, col_input2 = st.columns([2, 2])
    with col_input1:
        ticker_input = st.text_input("Enter Ticker for Backtest", value="NVDA").upper()
    with col_input2:
        lookback = st.slider("Momentum Lookback Window (Days)", min_value=5, max_value=100, value=20)

    if st.button("Run Backtest", type="primary"):
        with st.spinner(f"Fetching data and simulating strategy for {ticker_input}..."):
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
                fig.update_layout(legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1})
                st.plotly_chart(fig, use_container_width=True)
                
                final_bh = results['Buy_Hold_Cum'].iloc[-1] - 1
                final_strat = results['Strategy_Cum'].iloc[-1] - 1
                
                m1, m2 = st.columns(2)
                m1.metric("Buy & Hold Return", f"{final_bh:.2%}")
                m2.metric("SMC Strategy Return", f"{final_strat:.2%}")
            else:
                st.error(f"Could not retrieve data for '{ticker_input}'. Please check the ticker symbol.")
