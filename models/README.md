# 📁 models/

This directory contains the core machine learning logic for the **Stock Whisperer** project.  
It includes functions to prepare data, train LSTM models, and generate stock-level return predictions.

---

## Contents

### `lstm_model.py`
- Prepares time-series training data from historical stock prices
- Trains a separate LSTM model for each stock using past 7-day sequences
- Predicts next-day **intraday return** (i.e., from open to close)
- Functions:
  - `prepare_lstm_data(df)`
  - `train_lstm_model(X, y)`
  - `predict_next_return(model, recent_df, scaler)`

### `predictor.py`
- Coordinates the full prediction pipeline across NIFTY50 stocks
- Trains individual LSTM models for each stock
- Predicts next-day return for each
- Selects **top N stocks** with highest predicted returns
- Main function:
  - `get_top_n_predicted_stocks(symbol_list, start_date, end_date, top_n=5)`

---

## Design Philosophy

- Models are **trained independently per stock** to avoid overfitting a single model to heterogeneous time series
- Keeps LSTM implementation **modular and easily swappable** with other architectures (e.g., GRU, XGBoost)
- Lightweight and reproducible: trains on-the-fly using minimal features (`Open`, `High`, `Low`, `Close`, `Volume`)

---

## Data Requirements

- Input: Clean DataFrame with columns: `Open`, `High`, `Low`, `Close`, `Volume`
- Targets: Intraday return: `(Close - Open) / Open`
- All preprocessing is handled internally using `MinMaxScaler`

---

## Next Steps

- Replace or upgrade `predict_next_return()` with more complex models (e.g., attention-based or ensemble)
- Cache trained models for faster inference
- Integrate technical indicators as features (e.g., RSI, SMA)


