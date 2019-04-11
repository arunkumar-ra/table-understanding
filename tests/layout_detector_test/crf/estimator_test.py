import unittest
import numpy as np
from type.cell.cell_class import CellClass
from type.block.simple_block import SimpleBlock
from type.layout.layout_graph import LayoutGraph
from layout_detector.crf.estimator import CRFLayoutEstimator

class TestCRFEstimator(unittest.TestCase):

    def testCRFEstimator(self):

        # Table 1
        sheet1 = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags1 = np.array([[CellClass('META'), CellClass('META')], [CellClass('DATE'), CellClass('_DATA_')],
                          [CellClass('DATE'), CellClass('_DATA_')], [CellClass('DATE'), CellClass('_DATA_')]])
        b1_1 = SimpleBlock("META", 0, 1, 0, 0)
        b1_2 = SimpleBlock("DATE", 0, 0, 1, 3)
        b1_3 = SimpleBlock("_DATA_", 1, 1, 1, 3)
        blocks1 = [b1_1, b1_2, b1_3]

        # Table 2
        sheet2 = np.array([['date', 'value'], ['10.0', '2001'], ['11.0', '2002'], ['12.0', '2003']])
        tags2 = np.array([[CellClass('META'), CellClass('META')], [CellClass('_DATA_'), CellClass('DATE')],
                          [CellClass('_DATA_'), CellClass('DATE')], [CellClass('_DATA_'), CellClass('DATE')]])
        b2_1 = SimpleBlock("META", 0, 1, 0, 0)
        b2_2 = SimpleBlock("_DATA_", 0, 0, 1, 3)
        b2_3 = SimpleBlock("DATE", 1, 1, 1, 3)
        blocks2 = [b2_1, b2_2, b2_3]

        layoutGraph1 = LayoutGraph(blocks1)
        layoutGraph1.add_edge("header", 0, 1)
        layoutGraph1.add_edge("header", 0, 2)
        layoutGraph1.add_edge("meta", 1, 2)

        layoutGraph2 = LayoutGraph(blocks1)
        layoutGraph2.add_edge("header", 0, 1)
        layoutGraph2.add_edge("header", 0, 2)
        layoutGraph2.add_edge("meta", 2, 1)

        estimator = CRFLayoutEstimator()
        crf_layout_detector = estimator.fit_crf([sheet1, sheet2, sheet1, sheet2],
                                                [tags1, tags2, tags1, tags2],
                                                [blocks1, blocks2, blocks1, blocks2],
                                                [layoutGraph1, layoutGraph2, layoutGraph1, layoutGraph2])

