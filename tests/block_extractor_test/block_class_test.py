import unittest
from type.block import block_type
from type.block.block_class import BlockClass


class TestBlockClass(unittest.TestCase):
    def testBlockClass(self):

        block_dict = {
            block_type.EMPTY: 0.9,
            block_type.ATTRIBUTE: 0.1
        }

        bc = BlockClass(block_dict)
        assert bc.get_classes() == block_dict
        assert bc.get_best_class() == block_type.EMPTY
