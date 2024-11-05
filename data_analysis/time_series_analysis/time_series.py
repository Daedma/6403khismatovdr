import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from typing import Generator, Any, Tuple


def require_min_data_size(min_size: int):
    """
    Декоратор для проверки минимального размера данных.

    :param min_size: Минимальный размер данных.
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if len(self.data) < min_size:
                raise ValueError(f"Data must contain at least {min_size} elements")
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class TimeSeries:
    """
    Класс для работы с временными рядами.
    """

    def __init__(self, data: list):
        """
        Инициализация временного ряда.

        :param data: Данные временного ряда (список, numpy.array или pandas.DataFrame).
        """
        if isinstance(data, list):
            self.data = np.array(data)
        elif isinstance(data, np.ndarray):
            self.data = data
        elif isinstance(data, pd.DataFrame):
            if data.shape[1] != 1:
                raise ValueError("DataFrame must contain exactly one column")
            self.data = data.values.flatten()
        else:
            raise TypeError("Unsupported data type")

    def smoothed(self, window_size: int) -> Generator[float, Any, Any]:
        """
        Генератор для сглаживания временного ряда с использованием скользящего среднего.

        :param window_size: Размер окна для скользящего среднего.
        :return: Сглаженные значения временного ряда.
        """
        if window_size <= 0:
            raise ValueError("Размер окна должен быть положительным числом.")

        window = []
        for value in self.data:
            window.append(value)
            if len(window) > window_size:
                window.pop(0)
            if len(window) == window_size:
                yield sum(window) / window_size

    @require_min_data_size(2)
    def difference(self) -> Generator[float, Any, Any]:
        """
        Генератор для дифференцирования временного ряда.

        :return: Дифференцированные значения временного ряда.
        """
        for i in range(1, len(self.data)):
            yield self.data[i] - self.data[i - 1]

    def autocorrelation(self, lag: int) -> Generator[float, Any, Any]:
        """
        Генератор для вычисления автокорреляции временного ряда.

        :param lag: Лаг для вычисления автокорреляции.
        :return: Значения автокорреляции.
        """
        n = len(self.data)
        mean = np.mean(self.data)
        c0 = np.sum((self.data - mean) ** 2)

        for k in range(lag + 1):
            if k == 0:
                yield 1.0
            else:
                ck = np.sum((self.data[:-k] - mean) * (self.data[k:] - mean))
                yield ck / c0

    @require_min_data_size(3)
    def find_extrema(self) -> Generator[Tuple[int, float, str], Any, Any]:
        """
        Генератор для нахождения точек экстремума (локальных максимумов и минимумов) в временном ряду.

        :return: Кортежи с индексами, значениями и типами экстремумов.
        """
        if len(self.data) < 3:
            raise ValueError(
                "Для нахождения экстремумов необходимо минимум три значения."
            )

        for i in range(1, len(self.data) - 1):
            if self.data[i] > self.data[i - 1] and self.data[i] > self.data[i + 1]:
                yield (i, self.data[i], "max")
            elif self.data[i] < self.data[i - 1] and self.data[i] < self.data[i + 1]:
                yield (i, self.data[i], "min")

    @require_min_data_size(3)
    def forecast(
        self, steps: int, order: Tuple[int, int, int] = (1, 1, 1)
    ) -> Generator[float, Any, Any]:
        """
        Генератор для прогнозирования будущих значений временного ряда с использованием модели ARIMA.

        :param steps: Количество шагов для прогнозирования.
        :param order: Порядок модели ARIMA (p, d, q).
        :return: Прогнозируемые значения.
        """
        model = ARIMA(self.data, order=order)
        model_fit = model.fit()

        for _ in range(steps):
            forecast_value = model_fit.forecast()[0]
            yield forecast_value
