import unittest
from reader.csv_reader import CsvReader
import numpy as np

## Run as python -m unittest tests.reader_test.test_csv_reader

class TestCSVReader(unittest.TestCase):
    def testFileIsReadCorrectly(self):
        reader = CsvReader("tests/data/test.csv")

        sheet_gen = reader.get_sheets()
        sheet = next(sheet_gen)

        expected_sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])

        assert np.array_equal(sheet, expected_sheet)
