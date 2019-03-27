import unittest
import numpy as np
from block_extractor.block_extractor_v2 import BlockExtractorV2
from cell_classifier.simple_tag import SimpleTag
from block_extractor.simple_block import SimpleBlock
from block_extractor import new_block_types


class TestBlockExtractorV2(unittest.TestCase):
    def testBlockExtractorV2ForSimpleTableWithTwoColumns(self):

        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('DATE'), SimpleTag('_DATA_')],
                                  [SimpleTag('DATE'), SimpleTag('_DATA_')], [SimpleTag('DATE'), SimpleTag('_DATA_')]])

        sbe = BlockExtractorV2()
        blocks = sbe.extract_blocks(sheet, tags)

        for block in blocks:
            print(block)

        # Order of blocks in the list shouldn't actually matter. Write a better test to compare without any known order
        b1 = SimpleBlock(new_block_types.HEADER, 0, 1, 0, 0)
        b2 = SimpleBlock(new_block_types.HEADER, 0, 0, 1, 3)  # Todo: This is not correct
        b3 = SimpleBlock(new_block_types.VALUE, 1, 1, 1, 3)

        assert blocks[0] == b1
        assert blocks[1] == b2
        assert blocks[2] == b3
