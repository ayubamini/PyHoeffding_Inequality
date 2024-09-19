import yfinance as yf
import numpy as np

# Configuration
TICKER = "AAPL"  # Stock ticker
CAPITAL = 1000.0  # Initial capital
CONFIDENCE_LEVEL = 0.8  # 80% confidence
WINDOW_SIZE = 60  # One hour window (in minutes)

def calculate_hoeffding_bound(epsilon, n):
  return np.sqrt((1/(2*n)) * np.log(2/epsilon))

def get_price_changes(ticker, window_size):
  data = yf.download(ticker, period="1d", interval="1m")
  price_changes = data["Close"].pct_change().dropna()
  return price_changes[-window_size:]

def simulate_trade(price_changes, confidence_level):
  # Calculate empirical probability of positive price change
  positive_changes = (price_changes > 0).sum() / len(price_changes)

  # Calculate Hoeffding bound
  bound = calculate_hoeffding_bound(1 - confidence_level, len(price_changes))

  # Lower bound of confidence interval
  lower_bound = positive_changes - bound

  # Trading decision based on Hoeffding bounds
  if lower_bound > 0.5:
    print("Buy signal: Confidence level above 50%")
  elif lower_bound < 0.5:
    print("Sell signal: Confidence level below 50%")
  else:
    print("No signal: Confidence level around 50%")

# Main program
price_changes = get_price_changes(TICKER, WINDOW_SIZE)
simulate_trade(price_changes, CONFIDENCE_LEVEL)
