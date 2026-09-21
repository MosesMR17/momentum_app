import pandas as pd
from datetime import datetime
from modules.ingestion.fetcher import get_historical_data
from modules.screener.scanner import scan_watchlist
from modules.sentiment.analyzer import analyze_news_sentiment
from modules.risk.calculator import calculate_trade_levels

def run_momentum_app():
    print("=" * 60)
    print("🚀 RUNNING QUANTITATIVE MOMENTUM & TRADE SETUP SYSTEM")
    print("=" * 60)
    
    # 1. Define our expanded stock watchlist
    watchlist = [
        "AAPL", "NVDA", "TSLA", "MSFT", "AMZN", 
        "GOOGL", "META", "AMD", "NFLX", "PLTR", 
        "JPM", "DIS", "COIN", "BA", "INTC"
    ]
    
    # 2. Run Screener (Module 2)
    print("\n[1/3] Screening watchlist for momentum...")
    screener_df = scan_watchlist(watchlist)
    
    # 3. Process top results with Sentiment (Module 3) & Risk (Module 4)
    print("[2/3] Analyzing sentiment and calculating trade setups...")
    
    master_records = []
    for index, row in screener_df.iterrows():
        ticker = row["Ticker"]
        momentum = row["3M_Momentum_%"]
        
        # Get latest price for risk calculations
        df = get_historical_data(ticker, period="1mo")
        current_price = df['Close'].iloc[-1] if not df.empty else 0.0
        
        # Get Sentiment
        sentiment_data = analyze_news_sentiment(ticker)
        
        # Get Risk/Trade Setup Levels
        trade_levels = calculate_trade_levels(current_price)
        
        master_records.append({
            "Rank": index + 1,
            "Ticker": ticker,
            "3M Momentum (%)": momentum,
            "Sentiment": sentiment_data["Outlook"],
            "Entry ($)": trade_levels["Entry_Price"],
            "Stop Loss ($)": trade_levels["Stop_Loss"],
            "Target 1 ($)": trade_levels["Target_1"]
        })
        
    # 4. Display Master Dashboard
    print("\n" + "=" * 60)
    print("📊 FINAL TRADING DASHBOARD & TRADE SETUPS")
    print("=" * 60)
    
    dashboard_df = pd.DataFrame(master_records)
    print(dashboard_df.to_string(index=False))
    print("=" * 60)
    
    # 5. Export to CSV File
    filename = f"momentum_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    dashboard_df.to_csv(filename, index=False)
    print(f"📁 Dashboard successfully saved to {filename}!")
    print("=" * 60)

if __name__ == "__main__":
    run_momentum_app()
