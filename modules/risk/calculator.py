import pandas as pd
import numpy as np

def calculate_atr(df, period=14):
    """
    Calculates the Average True Range (ATR) for volatility-based risk sizing.
    """
    if df.empty or len(df) < period + 1:
        return None
        
    high = df['High']
    low = df['Low']
    close = df['Close']
    
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean().iloc[-1]
    return atr

def calculate_trade_levels(current_price, df=None):
    """
    Calculates entry, stop-loss, and target profit levels using ATR volatility 
    scaling if historical data is provided, otherwise falls back to percentage rules.
    """
    entry_price = round(current_price, 2)
    
    # Try calculating using ATR (2x ATR for stop loss, 3x ATR for target 1)
    atr = calculate_atr(df) if df is not None else None
    
    if atr and not np.isnan(atr):
        stop_loss = round(entry_price - (2.0 * atr), 2)
        target_1 = round(entry_price + (3.0 * atr), 2)
        target_2 = round(entry_price + (6.0 * atr), 2)
        method = "ATR-based (Volatility Scaled)"
    else:
        # Fallback to standard percentage rules if ATR is unavailable
        stop_loss = round(entry_price * 0.96, 2)
        target_1 = round(entry_price * 1.06, 2)
        target_2 = round(entry_price * 1.12, 2)
        method = "Percentage-based (Fallback)"
        
    return {
        "Entry_Price": entry_price,
        "Stop_Loss": stop_loss,
        "Target_1": target_1,
        "Target_2": target_2,
        "Method": method
    }

if __name__ == "__main__":
    test_price = 150.00
    print(f"\n--- Risk & Trade Setup Test (Price: ${test_price}) ---")
    levels = calculate_trade_levels(test_price)
    for key, val in levels.items():
        print(f"{key}: {val}")
        