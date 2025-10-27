from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import socket
import yfinance as yf
import ZoneInfo
import datetime as dt
# Main Functionality methods

def check_network(host: str = "www.finance.yahoo.com", port: int = 443, timeout: float = 3.0) -> bool:
  try:
    with socket.create_connection((host, port), timeout):
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

def get_info(ticker_symbol):
  ticker_data = yf.Ticker(ticker_symbol)
  df = ticker_data.history(period="1d")

  open = df['Open'].iloc[-1]
  close = df['Close'].iloc[-1]

  info = ticker_data.info
  current_price = info.get('currentPrice')
  company_name = info.get('longName','N/A')
  symbol = info.get('symbol', 'N/A')

  return open, close, current_price, company_name, symbol

def handler(ticker_symbol):
  if not check_network():
    return "Error: Yahoo Finance API is down.\nPlease try again later."

  if not is_ticker_valid(ticker_symbol):
    return f"Error: Ticker Symbol: [{ticker_symbol}] is not a valid Ticker Symbol."
  
  open, close, current_price, company_name, symbol = get_info(ticker_symbol)

  value = calculate_value(close, open)
  percentage = calculate_percentage(close, open)

  now = dt.datetime.now(ZoneInfo('America/Los_Angeles'))

  return f"""Current Date and Time: {now.strftime('%a %b %d %I:%S')} PDT
Company Name: {company_name} ({symbol})
Stock Price: {current_price} {value} ({percentage}%)
"""

# /End

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit_data():
  ticker_symbol = request.get_json()

  data = handler(ticker_symbol)

  response = {
    'message' : f'{data}'
  }

  return jsonify(response)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)