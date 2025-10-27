from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import socket
import yfinance as yf
import datetime as dt
# Main Functionality methods

def check_network(host: str = "www.finance.yahoo.com", port: int = 443, timeout: float = 3.0) -> bool:
  try:
    with socket.create_connection((host, port), timeout:=timeout):
      return True
  except OSError:
    return False
  
def is_ticker_valid(ticker_symbol):
  try:
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.history(period="1d")
    if info.empty:
      return False
    return True
  except Exception:
    return False

def calculate_value(close, open):
  result = round(close - open, 2)
  if result > 0:
    return f"+{str(result)}"
  else:
    return str(result)

def calculate_percentage(close, open):
  result = round((close - open)/open * 100, 2)
  if result > 0:
    return f"+{str(result)}"
  else:
    return str(result)

def get_prices(ticker_symbol):
  ticker_data = yf.Ticker(ticker_symbol)
  df = ticker_data.history(period="1d")

  open = df['Open'].iloc[-1]
  close = df['Close'].iloc[-1]

  info = ticker_data.info
  current_price = info.get('currentPrice')

  return open, close, current_price

def handler(ticker_symbol):
  if check_network():
    return """
Error: Yahoo Finance API is down.

Please try again later.
"""

  if not is_ticker_valid(ticker_symbol):
    return f"Error: Ticker symbol: {ticker_symbol} is not valid"
  
  ticker_prices = get_prices(ticker_symbol)

  values = calculate_value(ticker_prices.close, ticker_prices.open)
  percentages = calculate_percentage(ticker_prices.close, ticker_prices.open)

# /End

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit_data():
  ticker_symbol = request.get_json()

  response = handler(ticker_symbol)

  return jsonify(response)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)