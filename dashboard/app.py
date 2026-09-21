# --- APP 2: QUANTITATIVE MOMENTUM APP ---
elif app_choice == "📈 Quantitative Momentum App":
    st.title("📈 Quantitative Momentum Investing App")
    st.markdown("Precision institutional momentum ranking across 15 premier market leaders.")
    
    # Curated list of 15 high-liquidity market leaders
    tickers = [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 
        'META', 'TSLA', 'NFLX', 'AMD', 'PLTR', 
        'AVGO', 'JPM', 'XOM', 'COST', 'PEP'
    ]
    
    st.info(f"📊 Tracking and ranking all **{len(tickers)} core stocks** based on trailing quantitative momentum.")
    
    with st.spinner("Computing live quantitative rankings..."):
        momentum_data = []
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)
        
        for ticker in tickers:
            try:
                df_hist = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not df_hist.empty and len(df_hist) > 30:
                    if isinstance(df_hist.columns, pd.MultiIndex):
                        close_prices = df_hist['Close'][ticker]
                    else:
                        close_prices = df_hist['Close']
                    
                    start_price = close_prices.iloc[0]
                    recent_start_price = close_prices.iloc[-30]  # ~1 month ago
                    current_price = close_prices.iloc[-1]
                    
                    ret_12m = ((current_price - start_price) / start_price) * 100
                    ret_1m = ((current_price - recent_start_price) / recent_start_price) * 100
                    mom_score = ret_12m - ret_1m
                    
                    momentum_data.append({
                        'Ticker': ticker,
                        'Price ($)': round(float(current_price), 2),
                        '12M Return (%)': round(float(ret_12m), 2),
                        '1M Return (%)': round(float(ret_1m), 2),
                        'Momentum Score': round(float(mom_score), 2)
                    })
            except Exception as e:
                continue
        
        if momentum_data:
            res_df = pd.DataFrame(momentum_data)
            res_df = res_df.sort_values(by='Momentum Score', ascending=False).reset_index(drop=True)
            res_df.index = res_df.index + 1  # Start ranking from 1 to 15
            
            st.success("✅ Quantitative Rankings Loaded Successfully!")
            st.dataframe(res_df, use_container_width=True)
            
            st.markdown("### Top Momentum Distribution")
            st.bar_chart(res_df.set_index('Ticker')['Momentum Score'])
        else:
            st.error("⚠️ Unable to fetch live data right now. Please check your network connection.")