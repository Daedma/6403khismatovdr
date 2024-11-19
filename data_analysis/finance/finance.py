import yfinance as yf

class Finance:
    def __init__(self, ticker):
        self._ticker = ticker

    def get_current(self):
        stock = yf.Ticker(self._ticker)
        price = stock.info['regularMarketPrice']
        return price

    def get_period(self, period):
        data = yf.download(self._ticker, period=period)
        return data["Close"].values
