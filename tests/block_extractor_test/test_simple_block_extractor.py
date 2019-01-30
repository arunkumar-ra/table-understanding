import unittest
import numpy as np
from block_extractor.simple_block_extractor import SimpleBlockExtractor
from cell_classifier.simple_tag import SimpleTag
from block_extractor.simple_block import SimpleBlock


class TestSimpleBlockExtractor(unittest.TestCase):
    def testBlockExtractorForSimpleTableWithTwoColumns(self):

        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('DATE'), SimpleTag('_DATA_')],
                                  [SimpleTag('DATE'), SimpleTag('_DATA_')], [SimpleTag('DATE'), SimpleTag('_DATA_')]])

        sbe = SimpleBlockExtractor()
        blocks = sbe.extract_blocks(sheet, tags)

        # Order of blocks in the list shouldn't actually matter. Write a better test to compare without any known order
        b1 = SimpleBlock("META", 0, 1, 0, 0)
        b2 = SimpleBlock("DATE", 0, 0, 1, 3)
        b3 = SimpleBlock("_DATA_", 1, 1, 1, 3)

        assert blocks[0] == b1
        assert blocks[1] == b2
        assert blocks[2] == b3
