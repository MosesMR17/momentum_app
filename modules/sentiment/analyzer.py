import random

def analyze_news_sentiment(ticker):
    """
    Simulates fetching and scoring news sentiment for a given ticker.
    (We will hook this up to live news APIs in a later upgrade!)
    """
    # Placeholder sentiment generation mimicking NLP scoring (-1.0 to 1.0)
    print(f"Analyzing market sentiment for {ticker}...")
    
    # Random score for demonstration; positive bias for momentum stocks
    score = round(random.uniform(0.1, 0.9), 2)
    
    if score >= 0.6:
        sentiment = "Bullish"
    elif score >= 0.3:
        sentiment = "Neutral-Positive"
    else:
        sentiment = "Cautious"
        
    return {"Ticker": ticker, "Sentiment_Score": score, "Outlook": sentiment}

if __name__ == "__main__":
    # Test sentiment check
    print("\n--- Sentiment Analysis Test ---")
    result = analyze_news_sentiment("NVDA")
    print(result)
    