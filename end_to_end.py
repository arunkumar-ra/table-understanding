from annotator.yaml_annotator import YAMLAnnotator
from cell_classifier.crf_cell_classifier import CRFCellClassifier
from block_extractor.block_extractor_decision_tree import BlockExtractorDecisionTree
from block_extractor.block_extractor_v2 import BlockExtractorV2
from layout_detector.crf.crf_layout_detector import CRFLayoutDetector

from cell_classifier.cell_classifier import CellClassifier
from block_extractor.block_extractor import BlockExtractor
from layout_detector.layout_detector import LayoutDetector
from reader.file_reader import get_file_reader

import time


class EndToEnd:
    def __init__(self, input_file, cell_classifier: CellClassifier, block_extractor: BlockExtractor, layout_detector: LayoutDetector):
        self.input_file = input_file
        self.cell_classifier = cell_classifier
        self.block_extractor = block_extractor
        self.layout_detector = layout_detector

    def get_layout(self):
        start_time = time.time()

        reader = get_file_reader(self.input_file)

        tagList, blockList, layoutList = [], [], []

        for sheet in reader.get_sheets():
            tags = self.cell_classifier.classify_cells(sheet)
            blocks = self.block_extractor.extract_blocks(sheet, tags)
            if len(blocks) < 20:  ## Arbitrary number.
                layout = self.layout_detector.detect_layout(sheet, tags, blocks)
            else:
                layout = None

            tagList.append(tags)
            blockList.append(blocks)
            layoutList.append(layout)

        end_time = time.time()

        print("Time taken to process sheets : ", (end_time - start_time), "s")

        return tagList, blockList, layoutList

"""
Using crf cell classifier
and crf layout detector
You can create different functions for different combinations of classifiers 
"""
def v1():
    # file = "/Users/work/Downloads/FAOSTAT_commodity.csv"
    # file = "/Users/work/Downloads/FAOSTAT_commodity_test.csv"
    # file = "/Users/work/Downloads/FAOSTAT_crop_yields.csv"

    # file = "/Users/work/Projects/table-understanding/datamart_dataset/census/2007-11_ACS_Migration_Profile_In_Movers.xlsx"
    # Good results, "Population" should be a separate block, which is not found by the current block extractor
    # file = "/Users/work/Projects/table-understanding/datamart_dataset/census/Web_ACS2017_Educ.xlsx"
    # file = "/Users/work/Projects/table-understanding/datamart_dataset/census/Web_ACS2017_Social.xlsx"
    # file = "/Users/work/Projects/table-understanding/datamart_dataset/college-debt/OPEID.xls"
    # file = "/Users/work/Projects/table-understanding/datamart_dataset/college-debt/peps304.xlsx"
    # file = "/Users/work/Projects/table-understanding/datamart_dataset/poverty-estimation/data_gov/Education.xls"
    # Note for above: first 4 rows are header, then attribute, then value + attribute
    # file = "/Users/work/Projects/table-understanding/datamart_dataset/poverty-estimation/data_gov/PopulationEstimates.xls"


    # file = "/Users/work/Projects/elicit_alignment_OLD/m9/datasets/orig/structured/power_generation_q2_2017/example/Power Generation Q2 2017.xlsx"

    file = "/Users/work/Projects/table-understanding/datamart_dataset/census/P1_County_1yr_interim.xlsx"

    cell_classifier = CRFCellClassifier()
    block_extractor = BlockExtractorV2()

    # TODO: Layout detector does not work for 1 block?s
    layout_detector = CRFLayoutDetector()

    etoe = EndToEnd(file, cell_classifier, block_extractor, layout_detector)

    tagList, blockList, layoutList = etoe.get_layout()

    print("Number of sheets = {}".format(len(tagList)))

    for i in range(len(tagList)):
        tags = tagList[i]
        blocks = blockList[i]
        layout = layoutList[i]

        print("Sheet {}".format(i))
        print("Blocks found:")
        for idx, block in enumerate(blocks):
            print("Block id: " + str(idx) + " " + str(block))

        print("Layout")
        layout.print_layout()

        annotator = YAMLAnnotator()
        sheet_annotation = annotator.get_annotation(i, None, tags, blocks, layout)
        print(sheet_annotation)
        annotator.write_yaml(sheet_annotation, "annotator_output_{}.yaml".format(i))


def main():
    v1()


if __name__ == "__main__":
    main()
