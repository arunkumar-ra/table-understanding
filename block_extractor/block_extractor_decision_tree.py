import numpy as np
from block_extractor.block_extractor import BlockExtractor
from block_extractor.block_extractor_v2 import BlockExtractorV2
from type.block.simple_block import SimpleBlock
from typing import List
from queue import Queue
from reader.sheet import Sheet
from type.cell.cell_class import CellClass
from type.cell.cell_type import CellType
from typing import Tuple

"""
Use a decision tree based approach to split the group of cells in to different groups.
At each step, a split is chosen (horizontal or vertical) which minimizes the total entropy.
We keep splitting until we reach a point where the entropy loss (or information gain) is lower than a preset threshold. 
"""
class BlockExtractorDecisionTree(BlockExtractor):

    def __init__(self, threshold=0.20):
        self.threshold = threshold

    """
    List of possible hypothesis lines in x-axis and y-axis for splitting the table
    """
    def get_hypotheses(self, blocks):
        row_h = set()
        col_h = set()

        for _, block in blocks:
            row_h.add(block.get_top_row() - 1)
            row_h.add(block.get_bottom_row())
            col_h.add(block.get_left_col()-1)
            col_h.add(block.get_right_col())

        return row_h, col_h

    # TODO: Test this function
    def get_cell_distribution_of_split(self, split_block, maximal_blocks: List[Tuple[CellType, SimpleBlock]]) -> dict:
        block_dist = dict()
        for _type, block in maximal_blocks:
            intersection = split_block.get_intersecting_area(block)
            if intersection != 0:
                if _type not in block_dist:
                    block_dist[_type] = 0

                block_dist[_type] += intersection

        return block_dist

    def get_block_size(self, block):
        block_size = (block.get_right_col() - block.get_left_col() + 1) * \
                     (block.get_bottom_row() - block.get_top_row() + 1)

        return block_size

    def get_entropy(self, block: SimpleBlock, block_dist) -> float:
        entropy = 0.0
        block_size = self.get_block_size(block)

        for cell_type in block_dist:
            if block_dist[cell_type] != 0:
                p = block_dist[cell_type] / block_size

                entropy -= p * np.log2(p)
        return entropy

    def get_best_split(self, block: SimpleBlock, maximal_blocks: List[Tuple[CellType, SimpleBlock]], row_h, col_h):

        best_split = None, None
        best_split_entropy = 100

        base_entropy = self.get_entropy(block, self.get_cell_distribution_of_split(block, maximal_blocks))

        for b1, b2 in self.get_splits(block, row_h, col_h):
            entropy1 = self.get_entropy(b1, self.get_cell_distribution_of_split(b1, maximal_blocks))
            entropy2 = self.get_entropy(b2, self.get_cell_distribution_of_split(b2, maximal_blocks))
            b1_size = self.get_block_size(b1)
            b2_size = self.get_block_size(b2)

            p1 = b1_size / (b1_size + b2_size)

            entropy_after_split = p1 * entropy1 + (1 - p1) * entropy2
            print(base_entropy - entropy_after_split)

            if entropy_after_split < best_split_entropy:
                best_split = b1, b2
                best_split_entropy = entropy_after_split

        information_gain = base_entropy - best_split_entropy

        return best_split, information_gain

    def get_splits(self, block: SimpleBlock, row_h, col_h):

        for row in row_h:
            if row-1 < block.get_top_row() or row > block.get_bottom_row():
                continue
            b1 = SimpleBlock(None, block.get_left_col(), block.get_right_col(), block.get_top_row(), row)
            b2 = SimpleBlock(None, block.get_left_col(), block.get_right_col(), row + 1, block.get_bottom_row())

            yield b1, b2

        for col in col_h:
            if col-1 < block.get_left_col() or col > block.get_right_col():
                continue
            b1 = SimpleBlock(None, block.get_left_col(), col, block.get_top_row(), block.get_bottom_row())
            b2 = SimpleBlock(None, col + 1, block.get_right_col(), block.get_top_row(), block.get_bottom_row())

            yield b1, b2


    # TODO: How to return a tree instead of a list
    def extract_blocks(self, sheet: Sheet, tags: 'np.array[CellClass]') -> List[SimpleBlock]:
        # Get simple set of blocks from block extractor v2
        bev2 = BlockExtractorV2()
        row_blocks = bev2.merge_sheet_left_to_right(sheet, tags)
        maximal_blocks = bev2.merge_sheet_top_to_bottom(row_blocks)

        print("Maximal blocks extracted.")
        for block in maximal_blocks:
            print(block)

        row_h, col_h = self.get_hypotheses(maximal_blocks)

        max_row, max_col = sheet.values.shape
        start_block = SimpleBlock(None, 0, max_col - 1, 0, max_row - 1)  # TODO: Check if -1 is correct
        blocks = []

        q = Queue()
        q.put(start_block)

        while not q.empty():
            next_block = q.get()
            split_blocks, gain = self.get_best_split(next_block, maximal_blocks, row_h, col_h)

            b1, b2 = split_blocks
            if (b1 and b2) and gain >= self.threshold:  # Block was split into 2 blocks
                q.put(b1)
                q.put(b2)
                # print("Splitting {} into {} and {}".format(next_block, b1, b2))
                # print("Information gain: {}".format(gain))
            else:  # Block could not be split
                blocks.append(next_block)
                # print("Not splitting block {}".format(next_block))

        return blocks
