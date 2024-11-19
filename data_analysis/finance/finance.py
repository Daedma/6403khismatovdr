import yfinance as yf

class Finance:
    def __init__(self, ticker):
        self._ticker = ticker

    def get_current(self):
        stock = yf.Ticker(self._ticker)
        price = stock.info['regularMarketPrice']
        return price

    def get_period(self, period='30m', interval='1m'):
        data = yf.download(self._ticker, period=period, interval=interval)
        return data["Close"].values
