import numpy as np
from block_extractor.block_extractor import BlockExtractor
from block_extractor.simple_block import SimpleBlock
from typing import List
from block_extractor import new_block_types

"""
This block extractor extracts blocks from cell classifications.
Block Types is defined in block_extractor.new_block_types
"""

old_type_to_new_type_map = {
    "_DATA_": new_block_types.VALUE,
    "DATE": new_block_types.ATTRIBUTE,
    "EMPTY": new_block_types.EMPTY,
    "META": new_block_types.ATTRIBUTE
}

class BlockExtractorV2(BlockExtractor):
    def merge_row_left_to_right(self, row_id, row, tags):
        curr_block_start = 0
        row_blocks = []
        for i in range(1, len(row)):
            if tags[i] != tags[i-1]:
                row_blocks.append(SimpleBlock(tags[i-1].get_tags(), curr_block_start, i-1, row_id, row_id))
                curr_block_start = i

        cols = len(row)
        row_blocks.append(SimpleBlock(tags[cols-1].get_tags(), curr_block_start, cols-1, row_id, row_id))
        return row_blocks

    def merge_sheet_left_to_right(self, sheet, tags) -> List:
        row_blocks = [self.merge_row_left_to_right(row_id, row, row_tags) for row_id, (row, row_tags) in enumerate(zip(sheet, tags))]
        return row_blocks

    def merge_sheet_top_to_bottom(self, row_blocks: List) -> List:
        blocks = []
        up = row_blocks[0]  # Blocks which might be merged with rows below
        for i in range(1, len(row_blocks)):
            down = row_blocks[i]

            j, k = 0, 0
            new_up = []
            while j < len(up) and k < len(down):
                if up[j].get_left_col() == down[k].get_left_col() and up[j].get_right_col() == down[k].get_right_col()\
                        and up[j].get_block_type() == down[k].get_block_type():
                    # Merge two blocks
                    new_up.append(SimpleBlock(up[j].get_block_type(), up[j].get_left_col(), up[j].get_right_col(),
                                              up[j].get_upper_row(), down[k].get_lower_row()))
                    j += 1
                    k += 1

                elif up[j].get_right_col() < down[k].get_right_col():
                    blocks.append(up[j])
                    j += 1

                elif down[k].get_right_col() < up[j].get_right_col():
                    new_up.append(down[k])
                    k += 1

                elif up[j].get_right_col() == down[k].get_right_col():
                    blocks.append(up[j])
                    new_up.append(down[k])
                    j += 1
                    k += 1
            up = new_up

        blocks.extend(up)  # Add whatevers left
        return blocks

    """
    Hard coded logic
    """
    def extract_blocks(self, sheet: np.array, tags: np.array) -> List[SimpleBlock]:
        row_blocks = self.merge_sheet_left_to_right(sheet, tags)
        blocks = self.merge_sheet_top_to_bottom(row_blocks)

        new_blocks = []
        # Remove empty blocks
        for block in blocks:
            if block.get_block_type() != "EMPTY":
                new_blocks.append(block)

        blocks = new_blocks

        # Convert old block types to new block types
        new_blocks = []
        for block in blocks:
            old_type = block.get_block_type()
            new_type = old_type_to_new_type_map[old_type]

            if new_type == new_block_types.EMPTY:
                continue

            # Attribute can be global, non-global or headers
            if new_type == new_block_types.ATTRIBUTE:
                adjacent_block_found = False
                for block2 in blocks:
                    if block != block2 and block.is_adjacent(block2):
                        adjacent_block_found = True
                        break
                if not adjacent_block_found:
                    new_type = new_block_types.GLOBAL_ATTRIBUTE
                else:
                    # TODO: Block size should not be the only indicator for classifying a block as header
                    block_size = (block.get_right_col() - block.get_left_col() + 1) * (block.get_lower_row() - block.get_upper_row() + 1)
                    if block_size <= 5:
                        new_type = new_block_types.HEADER
                    else:
                        new_type = new_block_types.ATTRIBUTE ## same as before

            new_blocks.append(SimpleBlock(new_type,
                                          block.get_left_col(), block.get_right_col(),
                                          block.get_upper_row(), block.get_lower_row())
                              )
        return new_blocks