from annotator.yaml_annotator import YAMLAnnotator

from cell_classifier.cell_classifier import CellClassifier
from block_extractor.block_extractor import BlockExtractor
from layout_detector.layout_detector import LayoutDetector
from reader.file_reader import get_file_reader

from dataframe_extractor.dataframe_extractor import DataFrameExtractor
from util.block_colorizer import BlockColorizer
from configurator.configurator import Configurator

import sys, traceback
import time
import yaml
import sys
import getopt

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
                # print("Processing sheet: {}".format(sheet.meta['name']))
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

def print_details(idx, tags, blocks, layout):
    print("Sheet {}".format(idx))
    print("Blocks found:")
    for idx, block in enumerate(blocks):
        print("Block id: " + str(idx) + " " + str(block))

    print("Layout")
    if layout:
        layout.print_layout()


"""
Using crf cell classifier
and crf layout detector
You can create different functions for different combinations of classifiers 
"""
def v1(file_name, config_file, block, layout):
    print("Processing file: {}".format(file_name))
    config = yaml.load(open(config_file))
    print("Using configuration: {}".format(config))
    configurator = Configurator(config)

    cell_classifier = configurator.get_component("cell_classifier")
    if block == "heur":
        block_extractor = configurator.get_component("block_extractor_heuristic")
    else:
        block_extractor = configurator.get_component("block_extractor")
    layout_detector = configurator.get_component("layout_detector")

    etoe = EndToEnd(file_name, cell_classifier, block_extractor, layout_detector)

    sheetList, tagList, blockList, layoutList = etoe.get_layout()

    print("Number of sheets = {}".format(len(tagList)))

    for i in range(len(sheetList)):
        print_details(i, tagList[i], blockList[i], layoutList[i])

        layout = layoutList[i]
        if layout:
            annotator = YAMLAnnotator()
            sheet_annotation = annotator.get_annotation(i, None, tagList[i], blockList[i], layoutList[i])
            print(sheet_annotation)
            annotator.write_yaml(sheet_annotation, "annotator_output_{}.yaml".format(i))

    # Colorize blocks
    if config['colorize']:
        print("Colorizing output")
        if file_name.endswith(".xls") or file_name.endswith(".csv"):
            print("Colorizing not enabled in xls/csv files")
        else:
            bc = BlockColorizer(file_name)
            bc.apply_color(blockList)

    if config['output_dataframe']:
        print("Extracting dataframes from sheet")
        dataframes = []
        for i in range(len(sheetList)):
            dfe = DataFrameExtractor(sheetList[i], tagList[i], blockList[i], layoutList[i])
            dataframe = dfe.extract_dataframe()
            if dataframe is not None:
                dataframes.append(dataframe)
                dataframe.to_csv(file_name + "_" + str(i) + ".csv")

        return dataframes

    return None


"""
Instructions to run the program
"""
def usage():    
    print("Usage: python end_to_end.py -b <institute> -l <model_type>")
    print("<model_type> must be either 'prob' or 'heur'.")    

"""
Incorrect way of running the program
Print instructions and exit 
"""  
def print_usage():
    print('Incorrect usage')
    usage()
    sys.exit(2)

def main(argv):
    try:
        options, args = getopt.getopt(argv, "hb:l:f:")
    except getopt.GetoptError:
        print_usage()
    block, layout = "prob", "prob"
    
    for option, arg in options:
        if option == 'h':
            print_usage()
        if option in ("-b"):
            block = arg            
        elif option in ("-l"):
            layout = arg        

    if (block != "prob" and block != "heur") or (layout != "prob" and layout != "heur"):
        print_usage()    

    file_list = yaml.load(open("cfg/test_files.yaml"))

    # Try: Web_ACS2017_Educ.xlsx, P1_County_1yr_interim.xlsx,
    # alabama.xlsx, 2018 County Health Rankings Alabama Data - v3.xlsx
    # for file_name in file_list:
    file_name = file_list[8] # 5, 4, 11, 9
    dataframes = v1(file_name=file_name, config_file="cfg/test.yaml", block=block, layout=layout)


if __name__ == "__main__":
    main(sys.argv[1:])
