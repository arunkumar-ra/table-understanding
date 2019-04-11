import numpy as np


"""    
    Sheet:
        - np.array of cell values
        - dict/feature vector of cell format for each cell
"""


class Sheet:
    def __init__(self, values: np.array, meta: np.array):
        self.values = values
        self.meta = meta
