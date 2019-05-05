from annotator.yaml_annotator import YAMLAnnotator

from cell_classifier.cell_classifier import CellClassifier
from block_extractor.block_extractor import BlockExtractor
from layout_detector.layout_detector import LayoutDetector
from reader.file_reader import get_file_reader

from util.block_colorizer import BlockColorizer
from configurator.configurator import Configurator

import sys, traceback
import time
import yaml


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
            tags, blocks, layout = [[]], [], None
            try:
                print("Processing sheet: {}".format(sheet.meta['name']))
                tags = self.cell_classifier.classify_cells(sheet)
                blocks = self.block_extractor.extract_blocks(sheet, tags)
                if len(blocks) < 20:  ## Arbitrary number.
                    layout = self.layout_detector.detect_layout(sheet, tags, blocks)
            except Exception as e:
                print(str(e))
                traceback.print_exc(file=sys.stdout)

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
def v1(file, config_file):
    print("Processing file: {}".format(file))
    config = yaml.load(open(config_file))
    print("Using configuration: {}".format(config))
    configurator = Configurator(config)

    cell_classifier = configurator.get_component("cell_classifier")
    block_extractor = configurator.get_component("block_extractor")
    layout_detector = configurator.get_component("layout_detector")

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
        if layout:
            layout.print_layout()

            annotator = YAMLAnnotator()
            sheet_annotation = annotator.get_annotation(i, None, tags, blocks, layout)
            print(sheet_annotation)
            annotator.write_yaml(sheet_annotation, "annotator_output_{}.yaml".format(i))

    # Colorize blocks
    print("Colorizing output")
    bc = BlockColorizer(file)
    bc.apply_color(blockList)


def main():
    file_list = yaml.load(open("cfg/test_files.yaml"))

    # for file in file_list:
    file = file_list[2]
    v1(file=file, config_file="cfg/test.yaml")


if __name__ == "__main__":
    main()
