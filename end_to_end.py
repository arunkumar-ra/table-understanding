
from cell_classifier.cell_classifier import CellClassifier
from block_extractor.block_extractor import BlockExtractor
from layout_detector.layout_detector import LayoutDetector
from reader.file_reader import get_file_reader


import sys, traceback
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

        sheetList, tagList, blockList, layoutList = [], [], [], []

        for sheet in reader.get_sheets():
            tags, blocks, layout = [[]], [], None
            try:
                print("Processing sheet: {}".format(sheet.meta['name']))
                tags = self.cell_classifier.classify_cells(sheet)
                blocks = self.block_extractor.extract_blocks(sheet, tags)
                layout = self.layout_detector.detect_layout(sheet, tags, blocks)
            except Exception as e:
                print(str(e))
                traceback.print_exc(file=sys.stdout)

            sheetList.append(sheet)
            tagList.append(tags)
            blockList.append(blocks)
            layoutList.append(layout)

        end_time = time.time()

        print("Time taken to process sheets : ", (end_time - start_time), "s")

        return sheetList, tagList, blockList, layoutList

