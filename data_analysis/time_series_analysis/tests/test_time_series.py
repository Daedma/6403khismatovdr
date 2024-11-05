import unittest
from statsmodels.tsa.stattools import acf
from time_series_analysis.time_series import TimeSeries
from numpy.testing import assert_almost_equal


class TestTimeSeries(unittest.TestCase):

    def setUp(self):
        self.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.ts = TimeSeries(self.data)

    def test_smoothed(self):
        smoothed_data = list(self.ts.smoothed(3))
        expected_data = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        self.assertEqual(smoothed_data, expected_data)

    def test_smoothed_invalid_window_size(self):
        with self.assertRaises(ValueError):
            list(self.ts.smoothed(0))

    def test_difference(self):
        difference_data = list(self.ts.difference())
        expected_data = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(difference_data, expected_data)

    def test_difference_insufficient_data(self):
        ts = TimeSeries([1])
        with self.assertRaises(ValueError):
            list(ts.difference())

    def test_autocorrelation(self):
        autocorrelation_data = list(self.ts.autocorrelation(3))
        expected_data = acf(self.data, nlags=3)
        assert_almost_equal(autocorrelation_data, expected_data, 5)

    def test_find_extrema(self):
        extrema_data = list(self.ts.find_extrema())
        expected_data = []
        self.assertEqual(extrema_data, expected_data)

    def test_find_extrema_insufficient_data(self):
        ts = TimeSeries([1, 2])
        with self.assertRaises(ValueError):
            list(ts.find_extrema())

    def test_forecast(self):
        forecast_data = list(self.ts.forecast(3))
        self.assertEqual(len(forecast_data), 3)

    def test_forecast_insufficient_data(self):
        ts = TimeSeries([1, 2])
        with self.assertRaises(ValueError):
            list(ts.forecast(3))


if __name__ == "__main__":
    unittest.main()
