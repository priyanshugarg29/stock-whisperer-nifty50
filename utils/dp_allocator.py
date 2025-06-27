# -*- coding: utf-8 -*-
"""
@author: Priyanshu Garg
"""

# utils/dp_allocator.py

import pandas as pd

def allocate_budget(stocks: list, opening_prices: dict, budget: float = 10000.0) -> pd.DataFrame:
    """
    Allocates budget across top N stocks using predicted return,
    ensuring no stock receives more than 1/5th of total budget unless leftover budget allows.
    """
    allocation = []
    remaining_budget = budget
    max_allocation_per_stock = budget / 5  # 1/5th limit

    # Sort stocks by predicted return (descending)
    stocks_sorted = sorted(
        [(s, r, opening_prices.get(s)) for s, r in stocks if opening_prices.get(s) is not None],
        key=lambda x: x[1],
        reverse=True
    )

    for symbol, ret, price in stocks_sorted:
        if remaining_budget <= 0 or price == 0:
            break

        allowable_budget = min(max_allocation_per_stock, remaining_budget)
        qty = allowable_budget // price

        if qty == 0:
            continue

        invested = qty * price
        expected_profit = invested * ret

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
