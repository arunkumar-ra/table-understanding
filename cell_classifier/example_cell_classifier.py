from cell_classifier.cell_classifier import CellClassifier
from reader.sheet import Sheet
from type.cell.cell_type_pmf import CellTypePMF
from type.cell import cell_type
import numpy as np


class ExampleCellClassifier(CellClassifier):
    def __init__(self):
        pass

    def classify_cells(self, sheet: Sheet) -> 'np.ndarray[CellTypePMF]':
        cell_classification = {
            cell_type.EMPTY: 0.9,  # Probability distribution of cell types
            cell_type.META: 0.1 # etc
            # cell_type.DATA: 0
            # cell_type.DATE: 0
        }

        table_class = np.full(sheet.values.shape, CellTypePMF(cell_classification))

        return table_class
