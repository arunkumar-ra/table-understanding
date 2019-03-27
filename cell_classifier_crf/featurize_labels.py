import numpy as np
from cell_classifier_crf.feature_utils import empty_cell

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

inverse_dict = {
    0: "EMPTY",
    1: "META",
    2: "DATE",
    3: "_DATA_"
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
