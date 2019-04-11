import abc
import numpy as np
from reader.sheet import Sheet
from type.cell.cell_class import CellClass
from typing import List


class CellClassifier(abc.ABC):
    @abc.abstractmethod
    def classify_cells(self, sheet: Sheet) -> 'np.ndarray[CellClass]':  # Single quotes doesn't seem to actually enforce any check.
        pass


## TODO: Implement a base version of cell classifier ExampleBlock_ which returns empty tag for all cells.
## TODO: Implement a base version of cell classifier ExampleLayout_ which returns empty tag for all cells.
