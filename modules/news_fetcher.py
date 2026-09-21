import yfinance as yf

def get_latest_headlines(ticker_symbol, count=3):
    """
    Fetches recent news headlines for a given ticker symbol using yfinance.
    Returns a list of headline strings.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        news_items = ticker.news
        
        headlines = []
        if news_items:
            for item in news_items[:count]:
                # Depending on yfinance version, structure can be nested under 'content' or direct
                if "content" in item and "title" in item["content"]:
                    headlines.append(item["content"]["title"])
                elif "title" in item:
                    headlines.append(item["title"])
                    
        return headlines if headlines else ["No recent news headlines found."]
    except Exception as e:
        return [f"Could not fetch news: {str(e)}"]

if __name__ == "__main__":
    # Quick test for AAPL news
    test_ticker = "AAPL"
    print(f"\n--- Testing Live News Fetcher for {test_ticker} ---")
    results = get_latest_headlines(test_ticker)
    for h in results:
        print(f"- {h}")
        