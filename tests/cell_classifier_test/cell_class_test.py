import unittest
from type.cell.cell_class import CellClass


class TestCellClass(unittest.TestCase):
    def testCellClass(self):
        cell_class_dict = {
            "_DATA_": 0.51,
            "META": 0.49
        }

        c1 = CellClass(cell_class_dict)

        assert c1.get_best_class() == "_DATA_"
        assert c1.get_classes() == cell_class_dict
