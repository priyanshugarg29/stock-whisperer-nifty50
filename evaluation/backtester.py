# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:40:31 2025

@author: Admin
"""

# evaluation/backtester.py

from models.predictor import get_top_n_predicted_stocks
from utils.data_loader import get_stock_data
from utils.dp_allocator import allocate_budget
import pandas as pd
from datetime import datetime, timedelta

# Simulates strategy over last N days and computes real profit/loss
def backtest_strategy(symbols, num_days: int = 10, budget: float = 10000.0):
    """
    Runs the full prediction + allocation + evaluation loop over past num_days.

    Parameters:
        symbols (list): NIFTY50 stock symbols
        num_days (int): How many trading days to evaluate
        budget (float): Budget used for each simulated day

    Returns:
        pd.DataFrame: Daily performance table
    """
    results = []

    today = datetime.today().date()

    for offset in range(num_days, 0, -1):
        test_day = today - timedelta(days=offset)
        train_start = test_day - timedelta(days=60)
        train_end = test_day - timedelta(days=1)

        try:
            # Step 1: Predict top 5 stocks using LSTM
            top_stocks = get_top_n_predicted_stocks(
                symbol_list=symbols,
                start_date=train_start.strftime("%Y-%m-%d"),
                end_date=train_end.strftime("%Y-%m-%d"),
                top_n=5
            )

            # Step 2: Get real open and close prices for test_day
            prices = {}
            for symbol, _ in top_stocks:
                df = get_stock_data(symbol, test_day.strftime("%Y-%m-%d"), (test_day + timedelta(days=1)).strftime("%Y-%m-%d"))
                if df.empty:
                    continue
                row = df.iloc[0]
                prices[symbol] = {"Open": row["Open"], "Close": row["Close"]}

            # Step 3: Allocate budget based on predictions
            opening_prices = {s: prices[s]["Open"] for s in prices}
            allocation_df = allocate_budget(top_stocks, opening_prices, budget)

            # Step 4: Compute realized profit using real close price
            total_profit = 0.0
            for i, row in allocation_df.iterrows():
                sym = row["Symbol"]
                qty = row["Quantity"]
                buy_price = row["Price"]
                sell_price = prices[sym]["Close"]
                profit = (sell_price - buy_price) * qty
                allocation_df.at[i, "Real Close"] = round(sell_price, 2)
                allocation_df.at[i, "Realized Profit"] = round(profit, 2)
                total_profit += profit

            results.append({
                "Date": test_day.strftime("%Y-%m-%d"),
                "Top Stocks": [s[0] for s in top_stocks],
                "Total Invested": budget,
                "Realized Profit": round(total_profit, 2)
            })

        except Exception as e:
            print(f"Error on {test_day}: {e}")
            continue

    return pd.DataFrame(results)

def backtest_strategy(symbols, num_days: int = 10, budget: float = 10000.0, save_path: str = None):
    # ... existing code ...

    result_df = pd.DataFrame(results)

    if save_path:
        result_df.to_csv(save_path, index=False)
        print(f"[✔] Evaluation results saved to {save_path}")

    return result_df
