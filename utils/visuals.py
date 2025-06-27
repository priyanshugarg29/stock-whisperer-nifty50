# -*- coding: utf-8 -*-
"""
@author: Priyanshu Garg
"""
# utils/visuals.py
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def plot_profit_chart(eval_df):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Format dates for clarity
    eval_df = eval_df.sort_values("Date")
    dates = pd.to_datetime(eval_df["Date"]).dt.strftime("%d %b")
    profits = eval_df["Realized Profit"]
    cum_profits = eval_df["Cumulative Profit"]

    # Color based on gain/loss
    bar_colors = ['#4CAF50' if p >= 0 else '#F44336' for p in profits]

    # Bar: Daily Profit/Loss
    bars = ax1.bar(dates, profits, color=bar_colors, alpha=0.7, label="Daily Profit/Loss")

    # Annotate top gains/losses
    for i, (x, y) in enumerate(zip(dates, profits)):
        if abs(y) > 40:
            ax1.annotate(f'₹{y:.1f}', xy=(x, y), xytext=(0, 8 if y > 0 else -12),
                         textcoords='offset points', ha='center', fontsize=8, color='black')

    # Line: Cumulative Profit
    ax2 = ax1.twinx()
    ax2.plot(dates, cum_profits, color="navy", linewidth=2.5, marker='o', label="Cumulative Profit")

    # Grid, ticks & styling
    ax1.axhline(0, color='gray', linewidth=0.8, linestyle='--')
    ax1.set_ylabel("₹ Daily Profit/Loss", fontsize=11)
    ax2.set_ylabel("₹ Cumulative Profit", fontsize=11)
    ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
    ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('₹{x:,.0f}'))
    ax1.tick_params(axis='x', rotation=45)

    # Legends
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Title
    plt.title("📈 Backtest Profit Evaluation Over Time", fontsize=14, pad=15)

    # Layout adjustment
    plt.tight_layout()
    return fig


