# --- APP 2: QUANTITATIVE MOMENTUM APP ---
elif app_choice == "📈 Quantitative Momentum App":
    st.title("📈 Quantitative Momentum Investing App")
    
    today_str = datetime.today().strftime('%Y-%m-%d')
    st.markdown(f"**Latest Active Report:** Multi-Timeframe Momentum & Win Rate Prediction — *{today_str}*")
    st.divider()
    
    st.subheader("Master Predictive Trade Setups Table")
    st.markdown("Evaluating 15 premier market leaders across 3M, 3W, 1W, Daily, and 4H trends to estimate institutional win probabilities.")
    
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
                # Fetch daily data for 3M, 3W, 1W, Daily
                df_hist = yf.download(ticker, start=start_date, end=end_date, progress=False)
                # Fetch recent hourly data to approximate 4-hour trend action
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
                        close_hourly = close_daily[-10:] # Fallback
                    
                    current_price = float(close_daily.iloc[-1])
                    
                    # Horizon calculations
                    p_3m = float(close_daily.iloc[-63] if len(close_daily) >= 63 else close_daily.iloc[0])
                    p_3w = float(close_daily.iloc[-15] if len(close_daily) >= 15 else close_daily.iloc[0])
                    p_1w = float(close_daily.iloc[-5] if len(close_daily) >= 5 else close_daily.iloc[0])
                    p_1d = float(close_daily.iloc[-2] if len(close_daily) >= 2 else close_daily.iloc[0])
                    
                    ret_3m = ((current_price - p_3m) / p_3m) * 100
                    ret_3w = ((current_price - p_3w) / p_3w) * 100
                    ret_1w = ((current_price - p_1w) / p_1w) * 100
                    ret_1d = ((current_price - p_1d) / p_1d) * 100
                    
                    # 4-hour trend check (using recent hourly slope)
                    p_4h_ago = float(close_hourly.iloc[-4] if len(close_hourly) >= 4 else close_hourly.iloc[0])
                    ret_4h = ((current_price - p_4h_ago) / p_4h_ago) * 100
                    
                    # Win Rate Prediction Heuristic based on trend alignment consensus
                    positive_trends = sum([ret_3m > 0, ret_3w > 0, ret_1w > 0, ret_1d > 0, ret_4h > 0])
                    base_win_rate = 50.0 + (positive_trends * 7.5)  # Ranges from 50% to 87.5%
                    if ret_3m > 15 and ret_3w > 5:
                        base_win_rate += 5.0  # Strong momentum booster
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
            
            st.success("✅ Multi-Timeframe Matrix Computed Successfully!")
            st.dataframe(res_df, use_container_width=True, hide_index=True)
            
            st.markdown("### Top Win Probability Distribution")
            st.bar_chart(res_df.set_index('Ticker')['Est. Win Rate (%)'])
        else:
            st.error("⚠️ Unable to fetch multi-timeframe data right now. Please check your connection.")
            