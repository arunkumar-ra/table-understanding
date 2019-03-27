import unittest
import numpy as np
from cell_classifier.simple_tag import SimpleTag
from block_extractor.simple_block import SimpleBlock
from block_extractor import new_block_types


class TestSimpleBlock(unittest.TestCase):
    def testSimpleBlockFunctions(self):

        b1 = SimpleBlock(new_block_types.HEADER, 0, 1, 0, 0)
        b2 = SimpleBlock(new_block_types.ATTRIBUTE, 0, 0, 1, 3)
        b3 = SimpleBlock(new_block_types.VALUE, 1, 1, 1, 3)
        b4 = SimpleBlock(new_block_types.VALUE, 0, 1, 4, 4)
        b5 = SimpleBlock(new_block_types.VALUE, 2, 3, 1, 1)

        assert b1.is_adjacent(b2)
        assert b2.is_adjacent(b1)
        assert b2.is_adjacent(b3)
        assert b3.is_adjacent(b2)
        assert b1.is_adjacent(b3)
        assert b3.is_adjacent(b1)
        assert not b1.is_adjacent(b4)
        assert not b4.is_adjacent(b1)
        assert not b1.is_adjacent(b5)
        assert not b5.is_adjacent(b1)
