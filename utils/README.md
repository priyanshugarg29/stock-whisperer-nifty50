#  utils/

This directory contains utility modules that support the core logic of the Stock Whisperer system — including **data loading** and **budget allocation**.

---

## Contents

### `data_loader.py`
- Downloads historical stock price data using `yfinance`
- Fetches OHLCV (Open, High, Low, Close, Volume) data for given symbols and date ranges
- Designed to work with both individual stock data and index-level data (e.g., NIFTY50)

**Main function:**
```python
get_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame
