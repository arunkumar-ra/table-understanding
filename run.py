# THIs is a temporary file for testing
from annotator.annotate import Annotator
from cell_classifier.crf_cell_classifier import CRFCellClassifier
from block_extractor.simple_block_extractor import SimpleBlockExtractor
from layout_detector.simple_layout_detector import SimpleLayoutDetector
from reader.file_reader import get_file_reader


def main():
    # file = "/Users/work/Documents/ts_data_samples/data1.csv"
    # file = "/Users/work/Documents/Timeseries Extraction/table_extraction_deprecated_check_Projects_slash_arunk-projects/data/_train" \
    #        "/power_generation_q2_2017/example/Power Generation Q2 2017.xlsx"

    # file = "/Users/work/Downloads/FAOSTAT_South_Sudan_Food_Aid_data_2014-2015.csv"
    #file = "/Users/work/Downloads/FAOSTAT_crop_yields.csv"
    file = "/Users/work/Downloads/Crops_TrendAnalysis_2014-2016.csv"

    classifier = CRFCellClassifier()
    block_extractor = SimpleBlockExtractor()
    layout_detector = SimpleLayoutDetector()

    reader = get_file_reader(file)
    sheet_index = 0
    sheet = reader.get_sheet_by_index(sheet_index)
    annotator = Annotator()

    sheet_annotation = annotator.get_annotation(sheet_index, sheet, classifier, block_extractor, layout_detector)

    # print(sheet_annotation)


if __name__ == "__main__":
    main()
