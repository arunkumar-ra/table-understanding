import unittest
import numpy as np
from block_extractor.block_extractor_v2 import BlockExtractorV2
from type.cell.cell_class import CellClass
from type.block.simple_block import SimpleBlock
from type.block import block_type
from type.block.block_class import BlockClass
from type.cell import cell_type
from reader.sheet import Sheet


class TestBlockExtractorV2(unittest.TestCase):
    def testBlockExtractorV2ForSimpleTableWithTwoColumns(self):

        values = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        sheet = Sheet(values, None)
        tags = np.array([[CellClass({cell_type.META: 1}), CellClass({cell_type.META: 1})],
                          [CellClass({cell_type.DATE: 1}), CellClass({cell_type.DATA: 1})],
                          [CellClass({cell_type.DATE: 1}), CellClass({cell_type.DATA: 1})],
                          [CellClass({cell_type.DATE: 1}), CellClass({cell_type.DATA: 1})]])

        sbe = BlockExtractorV2()
        blocks = sbe.extract_blocks(sheet, tags)
        HEADER = BlockClass({block_type.HEADER: 1.0})
        VALUE = BlockClass({block_type.VALUE: 1.0})

        for block in blocks:
            print(block)

        # Order of blocks in the list shouldn't actually matter. Write a better test to compare without any known order
        b1 = SimpleBlock(HEADER, 0, 1, 0, 0)
        b2 = SimpleBlock(HEADER, 0, 0, 1, 3)  # Todo: This is not correct
        b3 = SimpleBlock(VALUE, 1, 1, 1, 3)

        assert blocks[0] == b1
        assert blocks[1] == b2
        assert blocks[2] == b3
