import unittest
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf
from sklearn.linear_model import LinearRegression
from time_series_analysis.time_series import TimeSeries

class TestTimeSeries(unittest.TestCase):

    def setUp(self):
        self.data_list = [1, 2, 3, 4, 5]
        self.data_array = np.array([1, 2, 3, 4, 5])
        self.data_series = pd.Series([1, 2, 3, 4, 5])

    def test_moving_average_list(self):
        ts = TimeSeries(self.data_list)
        result = ts.moving_average(window_size=2)
        expected = pd.Series([np.nan, 1.5, 2.5, 3.5, 4.5], name='Moving_Average')
        pd.testing.assert_series_equal(result['Moving_Average'], expected)

    def test_moving_average_array(self):
        ts = TimeSeries(self.data_array)
        result = ts.moving_average(window_size=2)
        expected = pd.Series([np.nan, 1.5, 2.5, 3.5, 4.5], name='Moving_Average')
        pd.testing.assert_series_equal(result['Moving_Average'], expected)

    def test_moving_average_series(self):
        ts = TimeSeries(self.data_series)
        result = ts.moving_average(window_size=2)
        expected = pd.Series([np.nan, 1.5, 2.5, 3.5, 4.5], name='Moving_Average')
        pd.testing.assert_series_equal(result['Moving_Average'], expected)

    def test_differential_list(self):
        ts = TimeSeries(self.data_list)
        result = ts.differential()
        expected = pd.Series([np.nan, 1.0, 1.0, 1.0, 1.0], name='Differential')
        pd.testing.assert_series_equal(result['Differential'], expected)

    def test_differential_array(self):
        ts = TimeSeries(self.data_array)
        result = ts.differential()
        expected = pd.Series([np.nan, 1.0, 1.0, 1.0, 1.0], name='Differential')
        pd.testing.assert_series_equal(result['Differential'], expected)

    def test_differential_series(self):
        ts = TimeSeries(self.data_series)
        result = ts.differential()
        expected = pd.Series([np.nan, 1.0, 1.0, 1.0, 1.0], name='Differential')
        pd.testing.assert_series_equal(result['Differential'], expected)

    def test_autocorrelation_list(self):
        ts = TimeSeries(self.data_list)
        result = ts.autocorrelation(lags=2)
        expected = pd.Series([1.0, 0.5, -0.5], name='Autocorrelation')
        pd.testing.assert_series_equal(result['Autocorrelation'], expected)

    def test_autocorrelation_array(self):
        ts = TimeSeries(self.data_array)
        result = ts.autocorrelation(lags=2)
        expected = pd.Series([1.0, 0.5, -0.5], name='Autocorrelation')
        pd.testing.assert_series_equal(result['Autocorrelation'], expected)

    def test_autocorrelation_series(self):
        ts = TimeSeries(self.data_series)
        result = ts.autocorrelation(lags=2)
        expected = pd.Series([1.0, 0.5, -0.5], name='Autocorrelation')
        pd.testing.assert_series_equal(result['Autocorrelation'], expected)

    def test_find_extremes_list(self):
        ts = TimeSeries(self.data_list)
        result = ts.find_extremes()
        expected_max = pd.Series([np.nan, np.nan, np.nan, np.nan, 5.0], name='Local_Max')
        expected_min = pd.Series([1.0, np.nan, np.nan, np.nan, np.nan], name='Local_Min')
        pd.testing.assert_series_equal(result['Local_Max'], expected_max)
        pd.testing.assert_series_equal(result['Local_Min'], expected_min)

    def test_find_extremes_array(self):
        ts = TimeSeries(self.data_array)
        result = ts.find_extremes()
        expected_max = pd.Series([np.nan, np.nan, np.nan, np.nan, 5.0], name='Local_Max')
        expected_min = pd.Series([1.0, np.nan, np.nan, np.nan, np.nan], name='Local_Min')
        pd.testing.assert_series_equal(result['Local_Max'], expected_max)
        pd.testing.assert_series_equal(result['Local_Min'], expected_min)

    def test_find_extremes_series(self):
        ts = TimeSeries(self.data_series)
        result = ts.find_extremes()
        expected_max = pd.Series([np.nan, np.nan, np.nan, np.nan, 5.0], name='Local_Max')
        expected_min = pd.Series([1.0, np.nan, np.nan, np.nan, np.nan], name='Local_Min')
        pd.testing.assert_series_equal(result['Local_Max'], expected_max)
        pd.testing.assert_series_equal(result['Local_Min'], expected_min)

    def test_forecast_list(self):
        ts = TimeSeries(self.data_list)
        result = list(ts.forecast(steps=2))
        expected = [6.0, 7.0]
        self.assertEqual(result, expected)

    def test_forecast_array(self):
        ts = TimeSeries(self.data_array)
        result = list(ts.forecast(steps=2))
        expected = [6.0, 7.0]
        self.assertEqual(result, expected)

    def test_forecast_series(self):
        ts = TimeSeries(self.data_series)
        result = list(ts.forecast(steps=2))
        expected = [6.0, 7.0]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
