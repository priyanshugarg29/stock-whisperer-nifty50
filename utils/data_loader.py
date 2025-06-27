# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:09:54 2025

@author: Priyanshu Garg
"""

# utils/data_loader.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Fetches daily stock data for a single symbol from Yahoo Finance
def get_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads historical stock data for a given symbol between start_date and end_date.

    Parameters:
        symbol (str): Ticker symbol (e.g., "RELIANCE.NS")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.DataFrame: DataFrame containing Date, Open, Close, High, Low, Volume
    """
    try:
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)
        df.reset_index(inplace=True)

        # Keep only required columns
        return df[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

