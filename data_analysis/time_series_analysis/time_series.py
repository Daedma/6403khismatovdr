import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf

def log_method(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

class TimeSeries:
    def __init__(self, data):
        self.data = data
        self.results = pd.DataFrame()

    @log_method
    def moving_average(self, window_size):
        self.results['Moving_Average'] = self.data.rolling(window=window_size).mean()
        return self.results

    @log_method
    def differential(self):
        self.results['Differential'] = self.data.diff()
        return self.results

    @log_method
    def autocorrelation(self, lags):
        self.results['Autocorrelation'] = [acf(self.data, nlags=lags)[i] for i in range(lags+1)]
        return self.results

    @log_method
    def find_extremes(self):
        local_max = (self.data.shift(1) < self.data) & (self.data.shift(-1) < self.data)
        local_min = (self.data.shift(1) > self.data) & (self.data.shift(-1) > self.data)
        self.results['Local_Max'] = self.data[local_max]
        self.results['Local_Min'] = self.data[local_min]
        return self.results

    @log_method
    def save_to_excel(self, filename):
        self.results.to_excel(filename, index=False)

    def result_generator(self):
        for column in self.results.columns:
            yield column, self.results[column]
