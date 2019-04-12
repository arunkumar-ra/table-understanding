import unittest
import numpy as np
from type.cell.cell_type_pmf import CellTypePMF
from type.block.simple_block import SimpleBlock
from layout_detector.example_layout_detector import ExampleLayoutDetector
from reader.sheet import Sheet
from type.cell import cell_type

from type.block.block_type_pmf import BlockTypePMF
from type.block import block_type
from type.layout import edge_type

class TestExampleLayoutDetector(unittest.TestCase):
    def testLayoutDetectionForSimpleTableWithTwoColumns(self):

        values = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        sheet = Sheet(values, None)
        tags = np.array([[CellTypePMF({cell_type.META: 1}), CellTypePMF({cell_type.META: 1})],
                         [CellTypePMF({cell_type.DATE: 1}), CellTypePMF({cell_type.DATA: 1})],
                         [CellTypePMF({cell_type.DATE: 1}), CellTypePMF({cell_type.DATA: 1})],
                         [CellTypePMF({cell_type.DATE: 1}), CellTypePMF({cell_type.DATA: 1})]])

        ATTRIBUTE = BlockTypePMF({block_type.ATTRIBUTE: 1.0})
        VALUE = BlockTypePMF({block_type.VALUE: 1.0})

        b1 = SimpleBlock(ATTRIBUTE, 0, 1, 0, 0)
        b2 = SimpleBlock(ATTRIBUTE, 0, 0, 1, 3)  # Todo: This is not correct
        b3 = SimpleBlock(VALUE, 1, 1, 1, 3)

        blocks = [b1, b2, b3]

        sld = ExampleLayoutDetector()
        layout = sld.detect_layout(sheet, tags, blocks)

        # TODO: The labels assigned to the edges here are actually wrong. Labels from block b1 should be headers.
        assert(layout.inEdges == [[], [], [(edge_type.ATTRIBUTE, 0), (edge_type.ATTRIBUTE, 1)]])
        assert(layout.outEdges == [[(edge_type.ATTRIBUTE, 2)], [(edge_type.ATTRIBUTE, 2)], []])

