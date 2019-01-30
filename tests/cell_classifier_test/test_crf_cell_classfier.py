import unittest
import numpy as np
from cell_classifier.crf_cell_classifier import CRFCellClassifier
from cell_classifier.simple_tag import SimpleTag


class TestCRFCellClassifier(unittest.TestCase):
    def testCRFClassificationForSimpleTableWithTwoColumns(self):

        crf = CRFCellClassifier()
        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = crf.classify_cells(sheet)

        expected_tags = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('DATE'), SimpleTag('_DATA_')],
                                  [SimpleTag('DATE'), SimpleTag('_DATA_')], [SimpleTag('DATE'), SimpleTag('_DATA_')]])

        assert np.array_equal(tags, expected_tags)
