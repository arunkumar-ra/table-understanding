# Table Understanding 
Python version: 3

### This project implements the table extraction pipeline
Table understanding is divided into 3 sequential steps.

Step 1: Classify all the cells in the table using a pre-trained CRF based model. [cell_classifier]

Step 2: Group all the classified cells into blocks. [block_extractor]

Step 3: Find the relationship between different blocks. [layout_detector]


To simply run a file against the default extractors, use run.py and set the file name.
You can write your own extractors for the 3 steps in the corresponding folder, by inheriting from the corresponding base classes.

Base Class Files:
block_extractor.py, cell_classifier.py, layout_detector.py
