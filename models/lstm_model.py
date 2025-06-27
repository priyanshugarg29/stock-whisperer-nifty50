# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 11:18:39 2025

@author: Priyanshu Garg
"""

# models/lstm_model.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Prepares sequential input-output pairs for LSTM model training
def prepare_lstm_data(df: pd.DataFrame, sequence_length: int = 7):
    """
    Prepares feature and label arrays for LSTM from stock DataFrame.

    Parameters:
        df (pd.DataFrame): Stock data with columns ['Open', 'Close', 'High', 'Low', 'Volume']
        sequence_length (int): Number of past days to use as input sequence

    Returns:
        X (np.array): Feature tensor of shape (samples, sequence_length, features)
        y (np.array): Target next-day intraday return values
        scaler (MinMaxScaler): Fitted scaler for future use
    """
    df = df.copy()

    # Calculate target: intraday return (% change)
    df['Return'] = (df['Close'] - df['Open']) / df['Open']

    # Drop rows with NaNs
    df.dropna(inplace=True)

    # Features used for LSTM input
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    target = 'Return'

    # Normalize features to scale 0-1
    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])

    X, y = [], []

    for i in range(sequence_length, len(df) - 1):  # leave room for next-day return
        seq_x = df[features].iloc[i - sequence_length:i].values
        seq_y = df[target].iloc[i + 1]  # predict D+1 return
        X.append(seq_x)
        y.append(seq_y)

    return np.array(X), np.array(y), scaler



# Builds and trains an LSTM model on given time series data
def train_lstm_model(X, y, epochs=50, batch_size=16, verbose=0):
    """
    Trains an LSTM model to predict next-day returns.

    Parameters:
        X (np.array): Feature sequences of shape (samples, timesteps, features)
        y (np.array): Target values (next-day returns)
        epochs (int): Number of training epochs
        batch_size (int): Mini-batch size for training
        verbose (int): Keras verbosity level (0 = silent, 1 = progress bar)

    Returns:
        model (keras.Model): Trained LSTM model
    """
    model = Sequential()
    model.add(LSTM(50, return_sequences=False, input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))  # Single output: next-day return

    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    return model


# Predicts next-day intraday return using trained model and last 7 days of data
def predict_next_return(model, recent_df: pd.DataFrame, scaler: MinMaxScaler, sequence_length: int = 7):
    """
    Predicts next-day intraday return using last N days of data.

    Parameters:
        model (keras.Model): Trained LSTM model
        recent_df (pd.DataFrame): DataFrame with last 7 days of ['Open', 'High', 'Low', 'Close', 'Volume']
        scaler (MinMaxScaler): Scaler used during training
        sequence_length (int): Number of timesteps in input sequence

    Returns:
        float: Predicted next-day return (e.g., 0.012 means +1.2%)
    """
    df = recent_df.copy()

    # Check if we have enough data
    if df.shape[0] < sequence_length:
        return 0.0

    # Only use required features
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    df[features] = scaler.transform(df[features])  # Apply same scaling

    # Format into shape (1, 7, features)
    input_seq = df[features].tail(sequence_length).values
    input_seq = np.expand_dims(input_seq, axis=0)

    # Predict next-day return
    predicted_return = model.predict(input_seq, verbose=0)[0][0]

    return float(predicted_return)


