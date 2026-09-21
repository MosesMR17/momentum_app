import pandas as pd
from modules.ingestion.fetcher import get_historical_data

def calculate_momentum(df):
    """
    Calculates a simple momentum score based on recent price percentage change.
    """
    if df.empty or len(df) < 30:
        return 0.0
    
    # Calculate percentage change over the last 30 trading days
    start_price = df['Close'].iloc[-30]
    end_price = df['Close'].iloc[-1]
    momentum_pct = ((end_price - start_price) / start_price) * 100
    return round(momentum_pct, 2)

def scan_watchlist(ticker_list):
    """
    Scans a list of tickers and returns a sorted dataframe of their momentum.
    """
    results = []
    for ticker in ticker_list:
        df = get_historical_data(ticker, period="3mo")
        score = calculate_momentum(df)
        results.append({"Ticker": ticker, "3M_Momentum_%": score})
    
    # Convert to DataFrame and sort by highest momentum
    scan_df = pd.DataFrame(results)
    scan_df = scan_df.sort_values(by="3M_Momentum_%", ascending=False).reset_index(drop=True)
    return scan_df

if __name__ == "__main__":
    # Test our screener with a few tech/momentum giants
    watchlist = ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN"]
    print("\nScanning watchlist for momentum...")
    top_stocks = scan_watchlist(watchlist)
    print("\n--- Screener Results ---")
    print(top_stocks)
    