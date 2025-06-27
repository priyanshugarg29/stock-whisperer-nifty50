
# models/predictor.py

import pandas as pd
from models.lstm_model import prepare_lstm_data, train_lstm_model, predict_next_return

def get_top_n_predicted_stocks(symbol_list, start_date, end_date, top_n=5):
    predictions = []

    for symbol in symbol_list:
        try:
            df = load_symbol_data(symbol, start_date, end_date)

            # Check if dataframe is valid and has enough rows
            if df is None or df.empty or df.shape[0] < 15:
                continue

            # Prepare data and train model
            X, y, scaler = prepare_lstm_data(df)

            if X.shape[0] == 0 or y.shape[0] == 0:
                continue

            model = train_lstm_model(X, y, epochs=10, verbose=0)

            recent_df = df.tail(7)

            # Ensure recent_df is not empty or malformed
            if recent_df is None or recent_df.empty or recent_df.shape[0] < 7:
                continue

            predicted_return = predict_next_return(model, recent_df, scaler)

            predictions.append((symbol, predicted_return))

        except Exception as e:
            print(f"Prediction failed for {symbol}: {e}")
            continue

    # Sort and return top N
    sorted_preds = sorted(predictions, key=lambda x: x[1], reverse=True)
    return sorted_preds[:top_n]

# Dummy loader — replace with your actual implementation
def load_symbol_data(symbol, start_date, end_date):
    from utils.data_loader import get_stock_data
    return get_stock_data(symbol, start_date, end_date)
