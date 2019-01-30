import abc
import numpy as np
from cell_classifier.tag import Tag


class CellClassifier(abc.ABC):
    @abc.abstractmethod
    def classify_cells(self, sheet) -> np.array:  # Should return a 2d numpy array of type Tag
        pass
