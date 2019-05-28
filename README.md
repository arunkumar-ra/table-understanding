# Table Understanding 
Python version: 3

### To run
usage: main.py [-h] [--config CONFIG] [--files FILES] [--output OUTPUT]

Run table understanding on xls/xlsx/csv files

optional arguments:
  -h, --help       show this help message and exit
  
  --config CONFIG  config file to load (default=cfg/default.yaml)
  
  --files FILES    list of files to process in yaml format. Each file is in a
                   new line preceded by '- ' (default=cfg/files.yaml)
                   
  --output OUTPUT  Output directory for all output files (default=./)


### Configuration
Settings file: cfg/test.yaml

To write a colorized excel sheet with block information:
   colorize: true/false
   (Please note that colorize works *only with xlsx files* due to the limitations of the library we are using)

To write out dataframes from detected 'value' blocks:
   output_dataframe: true/false


### This project implements the table extraction pipeline
Table understanding is divided into 3 sequential steps.

Step 1: Classify all the cells in the table using a pre-trained CRF based model. [cell_classifier]

Step 2: Group all the classified cells into blocks. [block_extractor]

Step 3: Find the relationship between different blocks. [layout_detector]

### Extending the code
You can write your own extractors for the 3 steps in the corresponding folder, by inheriting from the corresponding base classes.

Base Class Files:
cell_classifier.py, block_extractor.py, layout_detector.py

Corresponding to each layer, we have implemented an example class derived from it's base class.
example_cell_classifier.py, example_block_extractor.py, example_layout_detector.py

