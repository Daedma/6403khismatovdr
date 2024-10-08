import unittest
import pandas as pd
from time_series_analysis.time_series import TimeSeries

class TestTimeSeries(unittest.TestCase):
    def setUp(self):
        self.data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.ts = TimeSeries(self.data)

    def test_moving_average(self):
        result = self.ts.moving_average(3)
        self.assertIsNotNone(result['Moving_Average'])

    def test_differential(self):
        result = self.ts.differential()
        self.assertIsNotNone(result['Differential'])

    def test_autocorrelation(self):
        result = self.ts.autocorrelation(5)
        self.assertIsNotNone(result['Autocorrelation'])

    def test_find_extremes(self):
        result = self.ts.find_extremes()
        self.assertIsNotNone(result['Local_Max'])
        self.assertIsNotNone(result['Local_Min'])

    def test_save_to_excel(self):
        self.ts.save_to_excel('test_output.xlsx')

    def test_result_generator(self):
        self.ts.moving_average(3)
        generator = self.ts.result_generator()
        for column, data in generator:
            self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
