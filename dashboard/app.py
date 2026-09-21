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
    
    with st.spinner("Generating master momentum trade setups..."):
        momentum_data = []
        end_date = datetime.today()
        start_date = end_date - timedelta(days=120)  # ~3-4 months for 3M history
        
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
                    
                    # Actionable trade parameters based on momentum
                    sentiment = "Strong Bullish" if ret_3m > 10 else ("Bullish" if ret_3m > 0 else "Neutral")
                    entry = round(current_price, 2)
                    stop_loss = round(current_price * 0.96, 2)  # 4% risk buffer
                    target = round(current_price * 1.08, 2)     # 8% upside target
                    
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
            res_df.index = res_df.index + 1  # Rank from 1 to 15
            res_df.index.name = 'Rank'
            res_df = res_df.reset_index()
            
            st.success("✅ Master Trade Setups Loaded Successfully!")
            st.dataframe(res_df, use_container_width=True, hide_index=True)
            
            st.markdown("### 3M Momentum Performance Distribution")
            st.bar_chart(res_df.set_index('Ticker')['3M Momentum (%)'])
        else:
            st.error("⚠️ Unable to fetch live data right now. Please check your network connection.")
            