
# utils/data_loader.py

import yfinance as yf
import pandas as pd

def get_stock_data(symbol, start_date, end_date):

    df = yf.download(symbol, start=start_date, end=end_date, progress=False, auto_adjust=False)

    # Flatten multi-level columns if present (caused by group_by='ticker')
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Safety check: make sure critical columns exist
    required = ["Open", "Close"]
    if not all(col in df.columns for col in required):
        print(f"Warning: Missing expected columns in {symbol} data for {start_date} → {end_date}")
        return pd.DataFrame()

    return df.reset_index()

