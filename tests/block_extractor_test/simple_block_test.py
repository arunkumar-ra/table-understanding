import unittest
from type.block.simple_block import SimpleBlock
from type.block import block_type


class TestSimpleBlock(unittest.TestCase):
    def testSimpleBlockFunctions(self):

        b1 = SimpleBlock(block_type.HEADER, 0, 1, 0, 0)
        b2 = SimpleBlock(block_type.ATTRIBUTE, 0, 0, 1, 3)
        b3 = SimpleBlock(block_type.VALUE, 1, 1, 1, 3)
        b4 = SimpleBlock(block_type.VALUE, 0, 1, 4, 4)
        b5 = SimpleBlock(block_type.VALUE, 2, 3, 1, 1)

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
