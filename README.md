## Python Finance Info
[Link to Website](https://python-finance-info.onrender.com/)

### Tools used
- Yahoo! Finance's API: yfinance
- Front-end: JavaScript
- Back-end: Python Flask

### Functionality
A Web service that fetches and displays the current day's stock price.
Features
- Intraday Change Calculation i.e. (Closing Price - Opening Price)
- Handles errors gracefully
  - Provides a clear error when Yahoo Finance cannot be reached (network or service outage)
  - Validates input and clearly reports unknown or invalid ticker symbols
