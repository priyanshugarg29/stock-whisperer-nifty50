# -*- coding: utf-8 -*-
"""
@author: Priyanshu Garg
"""

# app.py

import streamlit as st
import pandas as pd
import datetime
from utils.dp_allocator import allocate_budget

# --- Utility functions ---

def load_evaluation_data(path="data/evaluation_results.csv"):
    try:
        return pd.read_csv(path)
    except:
        st.warning("Evaluation results not found.")
        return pd.DataFrame()

def format_currency(value):
    return f"₹{value:,.2f}"

# --- Streamlit layout ---

st.set_page_config(page_title="Stock Whisperer", layout="wide")
st.title("Stock Whisperer")
st.caption("Hear what the NIFTY50 will say tomorrow")

# --- Section 1: Market Calendar ---

today = datetime.date.today()
next_trading_day = today + datetime.timedelta(days=1)
prev_close_day = today - datetime.timedelta(days=1)

st.subheader("Market Calendar")
col1, col2, col3 = st.columns(3)
col1.metric("Today", today.strftime('%A, %d %B %Y'))
col2.metric("Previous Close", prev_close_day.strftime('%A, %d %B %Y'))
col3.metric("Next Trading Day", next_trading_day.strftime('%A, %d %B %Y'))

# --- Section 2: User Budget ---

st.subheader("Investment Configuration")
budget = st.number_input(
    label="Investment Budget (INR)",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=500
)

# --- Section 3: Prediction & Allocation Strategy ---

st.subheader("Predicted Top 5 Stocks and Allocation Strategy")

# Placeholder prediction results (replace with live model later)
predicted = [("TCS.NS", 0.015), ("INFY.NS", 0.012), ("SBIN.NS", 0.009), ("ITC.NS", 0.008), ("RELIANCE.NS", 0.007)]
opening_prices = {"TCS.NS": 3845, "INFY.NS": 1490, "SBIN.NS": 650, "ITC.NS": 425, "RELIANCE.NS": 2810}

alloc_df = allocate_budget(predicted, opening_prices, budget)

if not alloc_df.empty:
    alloc_df['Predicted Return (%)'] = alloc_df['Predicted Return'] * 100
    alloc_df = alloc_df.drop(columns='Predicted Return')
    st.dataframe(alloc_df.style.format({
        "Price": "₹{:.2f}",
        "Invested": "₹{:.2f}",
        "Expected Profit": "₹{:.2f}",
        "Predicted Return (%)": "{:.2f}%"
    }))
else:
    st.info("Allocation data could not be generated.")

# --- Section 4: Evaluation Results ---

st.subheader("Backtest Evaluation (Last 10 Trading Days)")

eval_df = load_evaluation_data()

if not eval_df.empty:
    eval_df["Cumulative Profit"] = eval_df["Realized Profit"].cumsum()
    
    total_profit = eval_df["Realized Profit"].sum()
    st.metric("Total Realized Profit", format_currency(total_profit), delta_color="normal" if total_profit >= 0 else "inverse")

    # Line chart for daily vs cumulative returns
    chart_df = eval_df.set_index("Date")[["Realized Profit", "Cumulative Profit"]]
    st.line_chart(chart_df)

    # Show evaluation table
    st.dataframe(eval_df.style.format({
        "Realized Profit": "₹{:.2f}",
        "Cumulative Profit": "₹{:.2f}"
    }))
else:
    st.info("Backtest results not available. Run the evaluation script to generate data.")
    
st.markdown("---")
st.caption(
    "Disclaimer: This dashboard is intended for educational and exploratory use only. "
    "It does not constitute financial advice. Past performance does not guarantee future results."
)
