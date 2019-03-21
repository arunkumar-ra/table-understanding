from layout_detector.crf.estimator import CRFLayoutEstimator
from data_loader.load_training_data import LoadTrainingData
from data_loader.load_synthetic_data import LoadSyntheticData


def main():
    data_loader = LoadTrainingData()

    reg_params = [0.003, 0.01, 0.03, 0.1, 0.3, 1]
    block_list, layout_list = data_loader.load_annotation_files()

    crf_estimator = CRFLayoutEstimator(C_range=reg_params)
    crf_estimator.set_input([None] * len(block_list), [None] * len(block_list), block_list, layout_list)
    crf_model = crf_estimator.fit_crf()
    print("_________________")


def find_hyper_parameters():
    lsd = LoadSyntheticData()

    reg_params = [0.01, 0.03, 0.1]
    sheet_list, tags_list, block_list, layout_list = lsd.load_files()

    crf_estimator = CRFLayoutEstimator(C_range=reg_params, eval_against_test=False)
    crf_estimator.set_input(sheet_list, tags_list, block_list, layout_list)
    crf_estimator.fit_crf()
    print("_________________")


def evaluate_on_test_set():
    lsd = LoadSyntheticData()

    reg_params = [0.03]
    sheet_list, tags_list, block_list, layout_list = lsd.load_files()

    crf_estimator = CRFLayoutEstimator(C_range=reg_params, eval_against_test=False)
    crf_estimator.set_input(sheet_list, tags_list, block_list, layout_list)
    crf_model = crf_estimator.fit_crf()
    print("_________________")

    # Test on real data
    data_loader = LoadTrainingData()
    t_block_list, t_layout_list = data_loader.load_annotation_files()
    crf_estimator.evaluate_test_set([None] * len(t_block_list), [None] * len(t_block_list), t_block_list, t_layout_list)


if __name__ == "__main__":
    # main()
    # find_hyper_parameters()
    evaluate_on_test_set()