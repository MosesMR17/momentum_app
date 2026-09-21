def calculate_trade_levels(current_price, atr=None):
    """
    Calculates entry, stop-loss, and target profit levels based on current price.
    Using standard percentage-based risk rules as a baseline.
    """
    entry_price = round(current_price, 2)
    
    # Risk management rules:
    # - Stop loss: 4% below entry
    # - Target 1 (Conservative): 6% above entry
    # - Target 2 (Aggressive): 12% above entry
    
    stop_loss = round(entry_price * 0.96, 2)
    target_1 = round(entry_price * 1.06, 2)
    target_2 = round(entry_price * 1.12, 2)
    
    return {
        "Entry_Price": entry_price,
        "Stop_Loss": stop_loss,
        "Target_1": target_1,
        "Target_2": target_2,
        "Risk_Reward_Ratio": "1 : 1.5 (T1) / 1 : 3 (T2)"
    }

if __name__ == "__main__":
    # Test with a mock stock price of $150.00
    test_price = 150.00
    print(f"\n--- Risk & Trade Setup Test (Price: ${test_price}) ---")
    levels = calculate_trade_levels(test_price)
    for key, val in levels.items():
        print(f"{key}: {val}")
        