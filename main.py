from dataframe_extractor.dataframe_extractor import DataFrameExtractor
from util.block_colorizer import BlockColorizer
from configurator.configurator import Configurator

from annotator.yaml_annotator import YAMLAnnotator
from end_to_end import EndToEnd

import yaml
import argparse
import os

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
def v1(file_name, config_file, output_dir):
    base_name = os.path.basename(file_name)  # Returns only the file name
    print("Processing file: {}".format(file_name))
    config = yaml.load(open(config_file))
    print("Using configuration: {}".format(config))
    configurator = Configurator(config)

    cell_classifier = configurator.get_component("cell_classifier")
    block_extractor = configurator.get_component("block_extractor")
    layout_detector = configurator.get_component("layout_detector")

    etoe = EndToEnd(cell_classifier, block_extractor, layout_detector)

    sheetList, tagList, blockList, layoutList = etoe.get_layout(file_name)

    print("Number of sheets = {}".format(len(tagList)))

    for i in range(len(sheetList)):
        print_details(i, tagList[i], blockList[i], layoutList[i])

        layout = layoutList[i]
        if layout:
            annotator = YAMLAnnotator()
            sheet_annotation = annotator.get_annotation(i, None, tagList[i], blockList[i], layoutList[i])
            print(sheet_annotation)
            fn = base_name + ("_" + str(i) + "_" + sheetList[i].meta['name'] if 'name' in sheetList[i].meta else "")\
                 + ".yaml"
            annotator.write_yaml(sheet_annotation, os.path.join(args.output, fn))

    # Colorize blocks
    if config['colorize']:
        print("Colorizing output")
        if file_name.endswith(".xls") or file_name.endswith(".csv"):
            print("Colorizing not enabled in xls/csv files")
        else:
            bc = BlockColorizer(file_name, output_dir)
            bc.apply_color(blockList)

    if config['output_dataframe']:
        print("Extracting dataframes from sheet")
        dataframes = []
        for i in range(len(sheetList)):
            dfe = DataFrameExtractor(sheetList[i], tagList[i], blockList[i], layoutList[i])
            dataframe = dfe.extract_dataframe()
            if dataframe is not None:
                dataframes.append(dataframe)
                fn = base_name +\
                     ("_" + str(i) + "_" + sheetList[i].meta['name'] if 'name' in sheetList[i].meta else "") + ".csv"
                dataframe.to_csv(os.path.join(args.output, fn))

        return dataframes

    return None


def main(args):

    file_list = yaml.load(open(args.files))

    # Try: Web_ACS2017_Educ.xlsx, P1_County_1yr_interim.xlsx,
    # alabama.xlsx, 2018 County Health Rankings Alabama Data - v3.xlsx
    for file_name in file_list:
        dataframes = v1(file_name=file_name, config_file=args.config, output_dir=args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run table understanding on xls/xlsx/csv files')
    parser.add_argument("--config", default="cfg/default.yaml", help="config file to load")
    parser.add_argument("--files", default="cfg/files.yaml", help="list of files to process in yaml format. Each file" +
                        " is in a new line preceded by '- '")
    parser.add_argument("--output", default="./", help="Output directory for all output files")  # Default is current directory

    args = parser.parse_args()

    main(args)

## fix colorization in cmo file