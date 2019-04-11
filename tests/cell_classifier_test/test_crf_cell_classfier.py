import unittest
import numpy as np
from cell_classifier.crf_cell_classifier import CRFCellClassifier
from type.cell.cell_class import CellClass
from reader.sheet import Sheet
from type.cell import cell_type


class TestCRFCellClassifier(unittest.TestCase):
    def testCRFClassificationForSimpleTableWithTwoColumns(self):

        crf = CRFCellClassifier()
        values = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = crf.classify_cells(Sheet(values, None))

        expected_tags = np.array([[CellClass({cell_type.META: 1}), CellClass({cell_type.META: 1})],
                                  [CellClass({cell_type.DATE: 1}), CellClass({cell_type.DATA: 1})],
                                  [CellClass({cell_type.DATE: 1}), CellClass({cell_type.DATA: 1})],
                                  [CellClass({cell_type.DATE: 1}), CellClass({cell_type.DATA: 1})]])

        assert np.array_equal(tags, expected_tags)
