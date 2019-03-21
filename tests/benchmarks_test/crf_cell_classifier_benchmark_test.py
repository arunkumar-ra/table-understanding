import unittest
import numpy as np
from cell_classifier.simple_tag import SimpleTag
from benchmarks.crf_cell_classifier_benchmark import CRFCellClassifierBenchmark
from cell_classifier.crf_cell_classifier import CRFCellClassifier


class TestCRFCellClassifierBenchmark(unittest.TestCase):
    def testCRFCellClassifierBenchmark(self):

        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('DATE'), SimpleTag('_DATA_')],
                                  [SimpleTag('DATE'), SimpleTag('_DATA_')], [SimpleTag('DATE'), SimpleTag('_DATA_')]])

        ccc = CRFCellClassifier()
        cccb = CRFCellClassifierBenchmark(sheet, ccc, tags)

        print(cccb.get_confusion_matrix())

        c_matrix = cccb.get_confusion_matrix()

        assert np.array_equal(c_matrix, [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 3]])


    