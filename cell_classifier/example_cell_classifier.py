from cell_classifier.cell_classifier import CellClassifier
from reader.sheet import Sheet
from type.cell.cell_class import CellClass
from type.cell import cell_type
import numpy as np

from typing import List


class ExampleCellClassifier(CellClassifier):
    def __init__(self):
        pass

    def classify_cells(self, sheet: Sheet) -> 'np.ndarray[CellClass]':
        cell_classification = {
            cell_type.EMPTY: 1.0  # Probability distribution of cell types
            # cell_type.META: 0.0 # etc
            # cell_type.DATA: 0
            # cell_type.DATE: 0
        }

        table_class = np.full(sheet.values.shape, CellClass(cell_classification))

        return table_class
