# THIs is a temporary file for testing
from annotator.yaml_annotator import YAMLAnnotator
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

    cell_classifier = CRFCellClassifier()
    block_extractor = SimpleBlockExtractor()
    layout_detector = SimpleLayoutDetector()
    annotator = YAMLAnnotator()

    reader = get_file_reader(file)
    sheet_index = 0
    sheet = reader.get_sheet_by_index(sheet_index)

    tags = cell_classifier.classify_cells(sheet)
    blocks = block_extractor.extract_blocks(sheet, tags)
    layout = layout_detector.detect_layout(sheet, tags, blocks)

    print("Blocks found:")

    for idx, block in enumerate(blocks):
        print("Block id: " + str(idx) + " " + str(block))

    # print("\nLayout:")
    #
    # for idx, edges in enumerate(layout):
    #     print("FROM " + str(idx) + " TO " + str(edges))

    sheet_annotation = annotator.get_annotation(sheet_index, sheet, tags, blocks, layout)

    print(sheet_annotation)


if __name__ == "__main__":
    main()
