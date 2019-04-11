import unittest
import numpy as np
from type.cell.cell_class import CellClass
from benchmarks.crf_cell_classifier_benchmark import CRFCellClassifierBenchmark
from cell_classifier.crf_cell_classifier import CRFCellClassifier


class TestCRFCellClassifierBenchmark(unittest.TestCase):
    def testCRFCellClassifierBenchmark(self):

        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = np.array([[CellClass('META'), CellClass('META')], [CellClass('DATE'), CellClass('_DATA_')],
                         [CellClass('DATE'), CellClass('_DATA_')], [CellClass('DATE'), CellClass('_DATA_')]])

        ccc = CRFCellClassifier()
        cccb = CRFCellClassifierBenchmark(sheet, ccc, tags)

        print(cccb.get_confusion_matrix())

        c_matrix = cccb.get_confusion_matrix()

        assert np.array_equal(c_matrix, [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 3]])


    