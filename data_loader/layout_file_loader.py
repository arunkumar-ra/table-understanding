import json
from util.excel_utils import excel_range2bbox
from block_extractor.simple_block import SimpleBlock
from layout_detector.layout_graph import LayoutGraph
from typing import List


class LayoutFileLoader:
    def __init__(self, layout_file):
        self.layout_file = layout_file
        self.json = None
        try:
            with open(self.layout_file, "r") as infile:
                self.json = json.load(infile)
        except Exception as e:
            print(str(e))

        self.blocks = None

    def get_blocks_and_layout(self):
        blocks_and_layout = []

        if isinstance(self.json, list):
            for sheet in self.json:
                blocks = self.get_blocks(sheet)
                layout = self.get_layout(blocks, sheet)

                blocks_and_layout.append((blocks, layout))
        else:
            blocks = self.get_blocks(self.json)
            layout = self.get_layout(blocks, self.json)

            blocks_and_layout.append((blocks, layout))

        return blocks_and_layout

    def get_blocks(self, sheet) -> List[SimpleBlock]:
        blocks = sheet['blocks']
        blocklist = []

        for block_id in blocks:
            block_range, block_type = blocks[block_id].split("-")
            top_row, left_col, bottom_row, right_col = excel_range2bbox(block_range)
            s = SimpleBlock(block_type, left_col, right_col, top_row, bottom_row)

            blocklist.append(s)

        return blocklist

    def get_layout(self, blocks, sheet) -> LayoutGraph:
        edges = sheet['edges']
        layout = LayoutGraph(blocks)

        for vertex_left in edges:
            edge_list = edges[vertex_left]
            for edge in edge_list:
                edge_type, vertex_right = edge.split(":")
                layout.add_edge(edge_type, int(vertex_left)-1, int(vertex_right)-1)

        return layout