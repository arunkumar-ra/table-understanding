"""
Experimental code. Subject to change
"""


from layout_detector.crf.featurizer import Featurize
from typing import List
from pystruct.models import EdgeFeatureGraphCRF
from pystruct.learners import OneSlackSSVM
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_recall_fscore_support
from layout_detector.crf.label_space import edge_labels, inv_edge_labels, label_list, label_keys
import numpy as np
from sklearn.model_selection import train_test_split


class CRFLayoutEstimator:
    def __init__(self, max_iter=50, C=0.03, tol=0.01):
        self.max_iter = max_iter
        self.C = C
        self.tol = tol

    def fit_crf(self, sheetList: List, tagsList: List, blocksList: List, layoutList: List):
        ## Featurize input
        featurizer = Featurize(sheetList, tagsList, blocksList)

        print("Preparing data...")
        X_graph = np.array(featurizer.get_input_features())
        y_graph = np.array(featurizer.get_label_map(layoutList))

        ## Remove tables with only one link (Base case)
        X_g = []
        y_g = []
        for i in range(len(X_graph)):
            if len(X_graph[i][1]) != 0:
                X_g.append(X_graph[i])
                y_g.append(y_graph[i])

        X_graph = np.array(X_g)
        y_graph = np.array(y_g)

        # 60, 20, 20 split

        X_train, X_dev_test, y_train, y_dev_test = train_test_split(X_graph, y_graph, train_size=0.6, random_state=21)
        X_dev, X_test, y_dev, y_test = train_test_split(X_dev_test, y_dev_test, test_size=0.5, random_state=22)

        print("Train size: ", len(X_train))
        print("Dev size: ", len(X_dev))
        print("Test size: ", len(X_test))

        total_score = 0.0

        full_list_of_predictions = []
        full_list_of_ytrue = []

        model = EdgeFeatureGraphCRF(inference_method="ad3")  # , symmetric_edge_features=range(2))
        # ssvm = FrankWolfeSSVM(model=model, max_iter=20)
        ssvm = OneSlackSSVM(model, inference_cache=50, C=self.C, tol=self.tol, max_iter=self.max_iter, n_jobs=4, verbose=False)

        ssvm.fit(X_train, y_train)

        predictions = [x for x in ssvm.predict(X_dev)]

        for (prediction, actual) in zip(predictions, y_dev):

            dataset_score = accuracy_score(actual, prediction)
            print(dataset_score)

            full_list_of_predictions.extend(prediction)
            full_list_of_ytrue.extend(actual)

            total_score += dataset_score

            if dataset_score != 1.0:
                cnf_matrix = confusion_matrix(actual, prediction, labels=range(len(label_list)))
                # plot_confusion_matrix(cnf_matrix, classes=label_list)

                print(prediction)
                print(actual)

        print("C value = ", self.C)
        print("Precision, Recall, F-Score, Support")
        print(precision_recall_fscore_support(full_list_of_ytrue, full_list_of_predictions))
        print("F1 Score: ", f1_score(full_list_of_ytrue, full_list_of_predictions, average=None, labels=label_keys))

        #TODO: Train on the whole dataset

        # model = EdgeFeatureGraphCRF(inference_method="ad3")
        # ssvm = OneSlackSSVM(model, inference_cache=50, C=self.C, tol=self.tol, max_iter=self.max_iter, n_jobs=4,
        #                     verbose=True)
        # ssvm.fit(X_graph, y_graph)

        return ssvm
