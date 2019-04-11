import unittest
import numpy as np
from type.cell.cell_class import CellClass
from type.block.simple_block import SimpleBlock
from layout_detector.simple_layout_detector import SimpleLayoutDetector


class TestSimpleLayoutDetector(unittest.TestCase):
    def testLayoutDetectionForSimpleTableWithTwoColumns(self):

        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = np.array([[CellClass('META'), CellClass('META')], [CellClass('DATE'), CellClass('_DATA_')],
                         [CellClass('DATE'), CellClass('_DATA_')], [CellClass('DATE'), CellClass('_DATA_')]])

        b1 = SimpleBlock("META", 0, 1, 0, 0)
        b2 = SimpleBlock("DATE", 0, 0, 1, 3)
        b3 = SimpleBlock("_DATA_", 1, 1, 1, 3)

        blocks = [b1, b2, b3]

        sld = SimpleLayoutDetector()
        layout = sld.detect_layout(sheet, tags, blocks)

        # TODO: The labels assigned to the edges here are actually wrong. Labels from block b1 should be headers.
        assert(layout.inEdges == [[], [], [('meta', 0), ('meta', 1)]])
        assert(layout.outEdges == [[('meta', 2)], [('meta', 2)], []])

