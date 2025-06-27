# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:37:32 2025

@author: Admin
"""

# models/predictor.py

from models.lstm_model import prepare_lstm_data, train_lstm_model, predict_next_return
from utils.data_loader import get_stock_data
import pandas as pd

# Predicts next-day returns for multiple stocks and selects top N
def get_top_n_predicted_stocks(symbol_list: list, start_date: str, end_date: str, top_n: int = 5) -> list:
    """
    Trains and predicts next-day intraday return for each stock.
    Returns top N stocks sorted by predicted return.

    Parameters:
        symbol_list (list): List of stock symbols (e.g., ["RELIANCE.NS", "TCS.NS"])
        start_date (str): Start date for historical data (e.g., "2024-04-01")
        end_date (str): End date for training + prediction data (e.g., "2024-06-20")
        top_n (int): Number of top stocks to return

    Returns:
        List[Tuple]: [(symbol, predicted_return), ...] sorted descending
    """
    predictions = []

    for symbol in symbol_list:
        # Step 1: Load historical data
        df = get_stock_data(symbol, start_date, end_date)

        if df is None or df.shape[0] < 15:
            continue  # Skip stocks with insufficient data

        try:
            # Step 2: Prepare and train LSTM model
            X, y, scaler = prepare_lstm_data(df)
            model = train_lstm_model(X, y, epochs=30, batch_size=8, verbose=0)

            # Step 3: Predict return using most recent 7 days
            recent_df = df.tail(7)
            predicted_return = predict_next_return(model, recent_df, scaler)

            predictions.append((symbol, predicted_return))

        except Exception as e:
            print(f"Error processing {symbol}: {e}")

    # Sort stocks by predicted return
    predictions.sort(key=lambda x: x[1], reverse=True)

    return predictions[:top_n]
