import yaml
from block_extractor.simple_block import SimpleBlock
from typing import List
from layout_detector.layout_graph import LayoutGraph
from cell_classifier.simple_tag import SimpleTag

from block_extractor import new_block_types
from layout_detector import edge_types

import numpy as np

"""
Parse Binhs Layout Files into required format 
Look at data/sample.yaml for sample input
### TODO: Should change the class name to something more meaningful
"""
class BinhsLayoutFileLoader:
    def __init__(self, layout_file):
        self.layout_file = layout_file
        self.layout = None

        with open(self.layout_file, "r") as infile:
            self.layout = yaml.load(infile)

        print(self.layout)
        self.block_idx = dict()
        self.blocks = None

    # This method only works for simple tables where data cells have the label 'value'
    # There are no date cells
    # Only metadata cells and data cells
    def get_cell_tags(self):
        # Find the minimum bounding box for the sheet
        max_row, max_col = 0, 0

        for block_name in self.layout['layout']:
            location = self.layout['layout'][block_name]['location']

            row_range, col_range = location.split(":")
            _, bottom_row = row_range.split("..")
            _, right_col = col_range.split("..")

            max_row = max(max_row, int(bottom_row))
            max_col = max(max_col, int(right_col))

        print("Bounding box is (0, {}, 0, {})".format(max_row, max_col))

        tags = np.empty((max_row+1, max_col+1), dtype=SimpleTag)

        for block_name in self.layout['layout']:
            location = self.layout['layout'][block_name]['location']

            row_range, col_range = location.split(":")
            top_row, bottom_row = row_range.split("..")
            top_row, bottom_row = int(top_row), int(bottom_row)
            left_col, right_col = col_range.split("..")
            left_col, right_col = int(left_col), int(right_col)

            if block_name == "year" or block_name == "month" or block_name == "day" or block_name == "date":
                cell_tag = "DATE"
            elif block_name == "value":  # Might need to add more block names here from chiraag and apoorva's annotations
                cell_tag = "_DATA_"
            else:
                cell_tag = "META"

            for i in range(bottom_row - top_row + 1):
                for j in range(right_col - left_col + 1):
                    tags[top_row + i][left_col + j] = SimpleTag(cell_tag)

        for i in range(max_row + 1):
            for j in range(max_col + 1):
                if not tags[i][j]:
                    tags[i][j] = SimpleTag("EMPTY")

        return tags

    # This method tries to be general but might fail for complex layout structure
    # Block types are assigned based on label
    # 'value' - is assigned data block
    # all others are assigned metadata block
    # No empty blocks will be returned
    def get_blocks(self) -> List[SimpleBlock]:
        block_list = []
        block_id = 0
        for block_name in self.layout['layout']:
            if block_name == "value":
                block_type = new_block_types.VALUE
            elif block_name == "title" or block_name == "comments":
                block_type = new_block_types.GLOBAL_ATTRIBUTE
            elif block_name == "header":
                block_type = new_block_types.HEADER
            else:
                block_type = new_block_types.ATTRIBUTE

            block = self.layout['layout'][block_name]
            location = block['location']

            row_range, col_range = location.split(":")
            top_row, bottom_row = row_range.split("..")
            left_col, right_col = col_range.split("..")

            block_list.append(SimpleBlock(block_type, int(left_col), int(right_col), int(top_row), int(bottom_row)))
            self.block_idx[block_name] = block_id
            block_id += 1

        self.blocks = block_list
        return block_list


    # Layout information is extracted from the relationships property
    # Not 100% sure on the syntax of these in the yaml files. So there might be some bugs here
    def get_layout(self):
        relations = self.layout['relationships']['mappings']
        layout = LayoutGraph(self.blocks)
        for relation in relations:
            mapping = relation['value']

            _from, _to = mapping.split("<->")
            _from = _from.split(":")[0].strip()
            _to = _to.split(":")[0].strip()

            if _from == "header":
                edge_type = edge_types.HEADER
            elif _from == "title" or _from == "comments":
                edge_type = edge_types.GLOBAL_ATTRIBUTE
            else:
                edge_type = edge_types.ATTRIBUTE

            layout.add_edge(edge_type, self.block_idx[_from], self.block_idx[_to])

        return layout

    def get_cell_tags_blocks_and_layout(self):
        return self.get_cell_tags(), self.get_blocks(), self.get_layout()