from layout_detector.crf.estimator import CRFLayoutEstimator
from data_loader.load_training_data import LoadTrainingData


def main():
    data_loader = LoadTrainingData()

    reg_params = [0.003, 0.01, 0.03, 0.1, 0.3, 1]
    block_list, layout_list = data_loader.load_annotation_files()

    for C in reg_params:
        crf_estimator = CRFLayoutEstimator(C=C)
        crf_model = crf_estimator.fit_crf([None] * len(block_list), [None] * len(block_list), block_list, layout_list)
        print("_________________")

if __name__ == "__main__":
    main()
