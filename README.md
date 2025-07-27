# Stock Whisperer: Hear What the NIFTY50 Will Say Tomorrow (Under Development)

**Stock Whisperer** is an intelligent dashboard that predicts the top 5 NIFTY50 stocks likely to generate the highest intraday profit tomorrow — and allocates a given budget across them using dynamic programming.

This project combines deep learning (LSTM), dynamic portfolio allocation, and real-world backtesting to simulate how a ₹10,000 investment strategy would perform if followed daily based on market-close data.

---

## Disclaimer
This project is intended solely for exploratory, academic, and educational purposes.

The predictions and returns shown are based on historical data and simplified assumptions. They do not account for transaction costs, slippage, execution latency, liquidity, or real-world brokerage constraints.

Do not use this project to make actual investment decisions.
The project author does not offer financial advice and assumes no liability for any losses incurred.

Always consult a licensed financial professional before making trading or investment decisions.

---

## Project Highlights

- **Daily LSTM Predictions**: Uses past 7-day stock data to forecast next-day intraday returns (open → close).
- **Dynamic Budget Allocation**: Applies a greedy knapsack-based approach to invest ₹10,000 optimally across top 5 predicted stocks.
- **Real-World Evaluation**: Simulates and evaluates model performance over the past 10 trading days using actual NIFTY50 price data.
- **Streamlit Dashboard**: Interactive UI to view predictions, budget strategy, and profit/loss visualizations.
- **Modular Codebase**: Cleanly separated logic for prediction, allocation, evaluation, and UI.

---

## Motivation

This project began as an exploration into how sequential deep learning models like LSTM could support tactical trading decisions. By combining data-driven forecasting with optimization, it attempts to bridge the gap between **signal generation** and **capital allocation** — all within a reproducible and interactive environment.

---

## Real-World Relevance

If this system were live, a user could:
- Log in after the stock market closes
- View the top 5 stocks predicted to rise next day
- See how ₹10,000 would be split across them
- Review how well the model has performed over recent days

While this is currently a simulation, it mimics the real decision process for short-term, post-market strategy design.

---

## Tech Stack

| Component      | Tools Used                             |
|----------------|----------------------------------------|
| Data Source     | `yfinance` for historical stock prices |
| Prediction      | LSTM via TensorFlow/Keras              |
| Optimization    | Greedy dynamic allocation (Knapsack)   |
| Backtesting     | Custom evaluator using true returns    |
| Dashboard       | Streamlit                              |
| Deployment      | GitHub + Streamlit Cloud               |

---

## Academic Value

This project demonstrates practical application of:
- Time series modeling with LSTM
- Budget allocation with greedy dynamic programming
- Rolling-window evaluation and model validation
- Model interpretability through predictions vs real outcomes

It’s suitable for students or researchers working in finance, machine learning, or applied analytics.

---

## Example Dashboard Features

- Predicted Top 5 Stocks for Next Trading Day
- Budget Allocation Table with Expected Profit
- Daily and Cumulative Realized Profit from Backtesting
- User-Defined Investment Budget Input
- Trading Date Context (Today, Last Close, Next Trade)

---

## How to Run Locally

```bash
git clone https://github.com/your-username/stock-whisperer-nifty50.git
cd stock-whisperer-nifty50

# (Optional) Create environment
conda create -n stockwhisperer python=3.11
conda activate stockwhisperer

pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## Project Structure

```

stock-whisperer-nifty50/
│
├── app.py                        # Main Streamlit dashboard
├── requirements.txt              # All required libraries
├── README.md                     # This file
│
├── data/
|   ├── README.md                 # README file for data directory
│   └── evaluation_results.csv    # Backtest output (precomputed)
│
├── models/
│   ├── lstm_model.py             # LSTM model training + prediction
│   └── predictor.py              # Predict top 5 stocks
│
├── utils/
│   ├── data_loader.py            # Load historical price data
│   └── dp_allocator.py           # Budget allocation strategy
│
├── evaluation/
│   └── backtester.py             # Rolling 10-day evaluation logic

```

---

## Contact

For academic collaborations, technical queries, or feedback, feel free to connect via GitHub or LinkedIn.

https://www.linkedin.com/in/priyanshu-garg-60544a178/

---
