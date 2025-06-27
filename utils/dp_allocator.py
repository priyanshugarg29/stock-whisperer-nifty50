# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:39:32 2025

@author: Admin
"""

# utils/dp_allocator.py

import pandas as pd

# Allocates budget across top stocks based on predicted return using greedy knapsack logic
def allocate_budget(stocks: list, opening_prices: dict, budget: float = 10000.0) -> pd.DataFrame:
    """
    Allocates budget across top N stocks using predicted return as value per unit price.

    Parameters:
        stocks (list): List of tuples (symbol, predicted_return)
        opening_prices (dict): Dict of {symbol: opening_price}
        budget (float): Total INR to allocate

    Returns:
        pd.DataFrame: Allocation plan with columns: Symbol, Price, Return, Quantity, Invested, Expected Profit
    """
    allocation = []
    remaining_budget = budget

    # Calculate return per rupee (like value/weight in knapsack)
    stocks_sorted = sorted(
        [(s, r, opening_prices.get(s)) for s, r in stocks if opening_prices.get(s) is not None],
        key=lambda x: r, reverse=True
    )

    for symbol, ret, price in stocks_sorted:
        if remaining_budget <= 0 or price == 0:
            break

        # Max quantity we can buy with remaining budget
        qty = remaining_budget / price

        # Amount invested
        invested = qty * price
        expected_profit = invested * ret  # Based on predicted return

        allocation.append({
            "Symbol": symbol,
            "Price": round(price, 2),
            "Predicted Return": round(ret, 4),
            "Quantity": round(qty, 4),
            "Invested": round(invested, 2),
            "Expected Profit": round(expected_profit, 2)
        })

        remaining_budget -= invested

    return pd.DataFrame(allocation)
