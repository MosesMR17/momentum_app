# modules/international_watchlist.py

# 5 Viral/High-Institutional-Interest International Stocks (ADRs or Global Giants)
INTERNATIONAL_VIRAL_STOCKS = {
    "TSM": "Taiwan Semiconductor Manufacturing (Global AI/Chip Anchor)",
    "ASML": "ASML Holding NV (European Semiconductor Monopoly)",
    "TM": "Toyota Motor Corp (Global Automotive Leader)",
    "NVO": "Novo Nordisk A/S (Pharmaceutical/Viral Health Giant)",
    "SAP": "SAP SE (European Enterprise Software Leader)"
}

def get_international_watchlist():
    """Returns the list of tickers for viral international stocks heavily backed by institutions."""
    return list(INTERNATIONAL_VIRAL_STOCKS.keys())

def print_international_info():
    print("Tracking International Institutional Focus Stocks:")
    for ticker, desc in INTERNATIONAL_VIRAL_STOCKS.items():
        print(f" - {ticker}: {desc}")

if __name__ == "__main__":
    print_international_info()
    