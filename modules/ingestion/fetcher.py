import yfinance as yf
import pandas as pd

def get_historical_data(ticker_symbol, period="6mo"):
    """
    Fetches historical daily price data for a given stock ticker.
    """
    print(f"Fetching data for {ticker_symbol}...")
    stock = yf.Ticker(ticker_symbol)
    df = stock.history(period=period)
    return df

if __name__ == "__main__":
    # Quick test with Apple (AAPL)
    data = get_historical_data("AAPL")
    print(data.tail())