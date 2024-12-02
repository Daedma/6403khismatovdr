import yfinance as yf


class FinanceData:
    """
    Класс для получения финансовых данных с использованием библиотеки yfinance.

    Атрибуты:
    ---------
    _ticker : str
        Тикер акции для получения финансовых данных.
    """

    def __init__(self, ticker: str):
        """
        Инициализация объекта FinanceData.

        Параметры:
        ----------
        ticker : str
            Тикер акции для получения финансовых данных.
        """
        self._ticker = ticker

    def get_current(self) -> float:
        """
        Получает текущую цену закрытия акции.

        Возвращает:
        ----------
        float
            Текущая цена закрытия акции.
        """
        stock = yf.Ticker(self._ticker)
        current_price = stock.history(period="1d")["Close"][0]
        return current_price

    def get_period(self, period: str = "1mo", interval: str = "1d") -> list:
        """
        Получает исторические данные цен закрытия акции за указанный период и интервал.

        Параметры:
        ----------
        period : str, optional
            Период для получения данных (по умолчанию "1mo" - один месяц).
        interval : str, optional
            Интервал для получения данных (по умолчанию "1d" - один день).

        Возвращает:
        ----------
        list
            Список исторических цен закрытия акции за указанный период и интервал.
        """
        data = yf.download(self._ticker, period=period, interval=interval)
        return data["Close"].values
