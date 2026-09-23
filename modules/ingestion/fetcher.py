import yfinance as yf
import pandas as pd

def get_historical_data(ticker_symbol, period="6mo"):
    """
    Fetches historical daily price data for a given stock ticker with robust error handling.
    """
    print(f"Fetching data for {ticker_symbol}...")
    try:
        stock = yf.Ticker(ticker_symbol)
        df = stock.history(period=period)
        
        if df.empty:
            print(f"⚠️ Warning: No data returned for {ticker_symbol}")
            return pd.DataFrame()
            
        # Normalize column names to handle case variations
        df.columns = [str(col).capitalize() for col in df.columns]
        
        if 'Close' not in df.columns:
            close_cols = [c for c in df.columns if 'close' in str(c).lower()]
            if close_cols:
                df['Close'] = df[close_cols[0]]
                
        return df
    except Exception as e:
        print(f"❌ Error fetching data for {ticker_symbol}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    data = get_historical_data("AAPL")
    print(data.tail())
    