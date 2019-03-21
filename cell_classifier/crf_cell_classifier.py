from cell_classifier.cell_classifier import CellClassifier
import pickle
from crf.featurize_input import featurize_input
import numpy as np
from crf.edge_features import get_edge_map_and_features
from crf.featurize_labels import inverse_dict
from config import config, get_full_path
from cell_classifier.simple_tag import SimpleTag
from cell_classifier.tag import Tag
from typing import List


class CRFCellClassifier(CellClassifier):
    def __init__(self):
        # TODO: Use config file? or full path
        crf_model_file = get_full_path(config['crf']['model_file'])
        with open(crf_model_file, 'rb') as infile:
            self.model = pickle.load(infile, encoding='latin1')  # latin1 encoding since we are reading a python2 pickle file

    def __predict_wrapper(self, prediction, r, c):
        pred = np.empty((r, c), dtype=SimpleTag)
        for i in range(r):
            for j in range(c):
                pred[i][j] = SimpleTag(inverse_dict[prediction[i * c + j]])

        return pred

    def __get_features(self, sheet: np.array):
        x = sheet
        x_fz = featurize_input(sheet)
        num_features = x_fz.shape[2]
        x_graph = (
                    (np.reshape(x_fz, (x_fz.shape[0] * x_fz.shape[1], num_features)),) +
                    get_edge_map_and_features(x, x_fz, dist=1)
        )
        return np.array(x_graph)

    def classify_cells(self, sheet: np.array) -> np.array:
        x_graph = self.__get_features(sheet)
        predictions = self.model.predict([x_graph])[0]  # TODO: Direct access by index should be avoided
        tags = self.__predict_wrapper(predictions, sheet.shape[0], sheet.shape[1])
        # print(tags)

        return tags
