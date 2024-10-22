import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf
from sklearn.linear_model import LinearRegression

def data_type_decorator(func):
    def wrapper(self, *args, **kwargs):
        if isinstance(self.data, list):
            self.data = pd.Series(self.data)
        elif isinstance(self.data, np.ndarray):
            self.data = pd.Series(self.data)
        elif not isinstance(self.data, pd.Series):
            raise TypeError("Unsupported data type. Please provide a list, numpy array, or pandas Series.")
        return func(self, *args, **kwargs)
    return wrapper

class TimeSeries:
    def __init__(self, data):
        self.data = data
        self.results = pd.DataFrame()

    @data_type_decorator
    def moving_average(self, window_size):
        self.results['Moving_Average'] = self.data.rolling(window=window_size).mean()
        return self.results

    @data_type_decorator
    def differential(self):
        self.results['Differential'] = self.data.diff()
        return self.results

    @data_type_decorator
    def autocorrelation(self, lags):
        self.results['Autocorrelation'] = [acf(self.data, nlags=lags)[i] for i in range(lags+1)]
        return self.results

    @data_type_decorator
    def find_extremes(self):
        local_max = (self.data.shift(1) < self.data) & (self.data.shift(-1) < self.data)
        local_min = (self.data.shift(1) > self.data) & (self.data.shift(-1) > self.data)
        self.results['Local_Max'] = self.data[local_max]
        self.results['Local_Min'] = self.data[local_min]                        
        return self.results

    @data_type_decorator
    def forecast(self, steps):
        # Подготовка данных для линейной регрессии
        X = np.arange(len(self.data)).reshape(-1, 1)
        y = self.data.values

        # Обучение модели линейной регрессии
        model = LinearRegression()
        model.fit(X, y)

        # Генерация прогнозируемых значений
        last_index = len(self.data)
        for i in range(steps):
            forecast_index = np.array([[last_index + i]])
            forecast_value = model.predict(forecast_index)[0]
            yield forecast_value
