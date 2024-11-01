import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima.model import ARIMA


def require_min_data_size(min_size):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if len(self.data) < min_size:
                raise ValueError(f"Data must contain at least {min_size} elements")
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class TimeSeries:
    def __init__(self, data):
        self.data = data

    def smoothed(self, window_size):
        """
        Генератор для сглаживания временного ряда с использованием скользящего среднего.

        :param window_size: Размер окна для скользящего среднего.
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
    def difference(self):
        """
        Генератор для дифференцирования временного ряда.
        """
        for i in range(1, len(self.data)):
            yield self.data[i] - self.data[i - 1]

    def autocorrelation(self, lag):
        """
        Генератор для вычисления автокорреляции временного ряда.

        :param lag: Лаг для вычисления автокорреляции.
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
    def find_extrema(self):
        """
        Генератор для нахождения точек экстремума (локальных максимумов и минимумов) в временном ряду.
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
    def forecast(self, steps, order=(1, 1, 1)):
        """
        Генератор для прогнозирования будущих значений временного ряда с использованием модели ARIMA.

        :param steps: Количество шагов для прогнозирования.
        :param order: Порядок модели ARIMA (p, d, q).
        """
        model = ARIMA(self.data, order=order)
        model_fit = model.fit()

        for _ in range(steps):
            forecast_value = model_fit.forecast()[0]
            yield forecast_value
