
# evaluation/backtester.py

from models.predictor import get_top_n_predicted_stocks
from utils.data_loader import get_stock_data
from utils.dp_allocator import allocate_budget
from utils.date_utils import get_previous_weekday
import os
import pandas as pd
from datetime import datetime, timedelta
from time import time


def backtest_strategy(symbols, num_days: int = 10, budget: float = 10000.0, save_path: str = None):
    start_time = time()
    results = []
    today = datetime.today().date()
    test_day = today
    days_tested = 0

    while days_tested < num_days:
        print(f"Backtest Day {days_tested + 1}/{num_days} | Test Date: {test_day}")
        train_start = test_day - timedelta(days=60)
        train_end = test_day - timedelta(days=1)
        print(f"Training window: {train_start} → {train_end}")

        try:
            top_stocks = get_top_n_predicted_stocks(
                symbol_list=symbols,
                start_date=train_start.strftime("%Y-%m-%d"),
                end_date=train_end.strftime("%Y-%m-%d"),
                top_n=5
            )

            prices = {}
            for symbol, _ in top_stocks:
                df = get_stock_data(
                    symbol,
                    test_day.strftime("%Y-%m-%d"),
                    (test_day + timedelta(days=1)).strftime("%Y-%m-%d")
                )
                if df.empty:
                    continue
                row = df.iloc[0]
                open_price = row["Open"]
                close_price = row["Close"]

                # Ensure values are scalar
                if isinstance(open_price, pd.Series) or isinstance(close_price, pd.Series):
                    print(f"Ambiguous Series data for {symbol} on {test_day}, skipping.")
                    continue

                prices[symbol] = {"Open": float(open_price), "Close": float(close_price)}

            if not prices:
                print(f"No price data on {test_day}, skipping.")
                days_tested += 1
                test_day = get_previous_weekday(test_day)
                continue

            opening_prices = {s: prices[s]["Open"] for s in prices}
            allocation_df = allocate_budget(top_stocks, opening_prices, budget)

            total_profit = 0.0
            per_stock_profits = []

            for _, row in allocation_df.iterrows():
                sym = row["Symbol"]
                qty = row["Quantity"]
                buy_price = row["Price"]
                sell_price = prices[sym]["Close"]
                profit = (sell_price - buy_price) * qty

                allocation_df.at[_, "Real Close"] = round(sell_price, 2)
                allocation_df.at[_, "Realized Profit"] = round(profit, 2)

                per_stock_profits.append({
                    "Symbol": sym,
                    "Invested": round(row["Invested"], 2),
                    "Realized Profit": round(profit, 2)
                })

                total_profit += profit

            results.append({
                "Date": test_day.strftime("%Y-%m-%d"),
                "Top Stocks": [s[0] for s in top_stocks],
                "Investments": allocation_df[["Symbol", "Invested"]].to_dict("records"),
                "Profits": per_stock_profits,
                "Total Invested": round(budget, 2),
                "Realized Profit": round(total_profit, 2)
            })

        except Exception as e:
            print(f"Error on {test_day}: {e}")

        days_tested += 1
        test_day = get_previous_weekday(test_day)

    if save_path and results:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        json_path = save_path.replace(".csv", ".json")
        pd.DataFrame(results).to_json(json_path, orient='records', lines=True)
        print(f"Saved backtest results to {json_path}")
    else:
        print("No valid backtest results to save.")

    print(f"Backtest complete in {round(time() - start_time, 2)} seconds")
    return pd.DataFrame(results)


if __name__ == "__main__":
    NIFTY50 = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS",
        "ITC.NS", "KOTAKBANK.NS", "SBIN.NS", "HINDUNILVR.NS"
    ]
    backtest_strategy(NIFTY50, num_days=10, save_path="data/evaluation_results.csv")
