import yfinance as yf
data = yf.download('AAPL', period='1d', interval='5m')
print(data)
