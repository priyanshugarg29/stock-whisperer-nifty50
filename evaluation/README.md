#  evaluation/

This module implements the **backtesting engine** for the Stock Whisperer project.

---

## Contents

### `backtester.py`
- Simulates the investment strategy over a configurable number of past trading days
- For each day:
  1. Trains an LSTM on past 60 days of stock data
  2. Predicts top 5 stocks for the next day
  3. Allocates budget using dynamic programming
  4. Fetches real open and close prices
  5. Calculates realized profit/loss for that day
- Results are saved to `data/evaluation_results.csv`

**Main function:**
```python
backtest_strategy(symbols, num_days: int, budget: float, save_path: str = None) -> pd.DataFrame
