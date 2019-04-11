import numpy as np
from cell_classifier_crf.feature_utils import empty_cell
from type.cell import cell_type

# Fill empty values with empty
label_dict = {
    "EMPTY": 0,
    "META": 1,
    "DATE": 2,
    "DATA": 3,
    "_DATA_": 3,
    "empty": 0,
    "meta": 1,
    "date": 2,
    "data": 3
}


# TODO: (medium) Inverse dict should be bound with declaration of cell_type instances
inverse_dict = {
    0: cell_type.EMPTY,
    1: cell_type.META,
    2: cell_type.DATE,
    3: cell_type.DATA
}


def featurize_labels(x, y):

    r, c = y.shape
    ydash = np.zeros(y.shape, dtype=int)

    for j in range(r):
        for k in range(c):
            if y[j][k] == '':
                y[j][k] = "EMPTY"
            # TODO: Add other empty cases
            elif x[j][k] in empty_cell:
                y[j][k] = "EMPTY"
            ydash[j][k] = label_dict[y[j][k]]

    return ydash
