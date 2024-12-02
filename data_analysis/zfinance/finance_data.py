import yfinance as yf


class FinanceData:
    def __init__(self, ticker):
        self._ticker = ticker

    def get_current(self):
        stock = yf.Ticker(self._ticker)
        current_price = stock.history(period="1d")["Close"][0]
        return current_price

    def get_period(self, period="1mo", interval="1d"):
        data = yf.download(self._ticker, period=period, interval=interval)
        return data["Close"].values
