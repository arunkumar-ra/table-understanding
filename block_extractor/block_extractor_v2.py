import numpy as np
from block_extractor.block_extractor import BlockExtractor
from type.block.simple_block import SimpleBlock
from typing import List
from type.block.basic_block_type import BasicBlockType

from reader.sheet import Sheet
from type.cell.cell_type_pmf import CellTypePMF
from type.block.block_type_pmf import BlockTypePMF
from type.cell.basic_cell_type import BasicCellType

"""
This block extractor extracts blocks from cell classifications.
Block Types is defined in block_extractor.new_block_types
"""

#TODO: Switch from cell_type.DATA to BasicCellType.DATA
cell_type_to_block_type_map = {
    BasicCellType.DATA: BasicBlockType.VALUE,
    BasicCellType.DATE: BasicBlockType.ATTRIBUTE,
    BasicCellType.EMPTY: BasicBlockType.EMPTY,
    BasicCellType.META: BasicBlockType.ATTRIBUTE
}


class BlockExtractorV2(BlockExtractor):
    def __init__(self):
        pass

    def merge_row_left_to_right(self, row_id, row, tags: List[CellTypePMF]):
        curr_block_start = 0
        row_blocks = []
        for i in range(1, len(row)):
            if tags[i].get_best_type() != tags[i - 1].get_best_type():
                # Appending a tuple (CellType, SimpleBlock), since block type is undetermined at this point
                row_blocks.append((tags[i-1].get_best_type(),
                                   SimpleBlock(None, curr_block_start, i - 1, row_id, row_id)))
                curr_block_start = i

        cols = len(row)
        row_blocks.append((tags[cols-1].get_best_type(),
                          SimpleBlock(None, curr_block_start, cols - 1, row_id, row_id)))
        return row_blocks

    def merge_sheet_left_to_right(self, sheet: Sheet, tags: 'np.array[CellTypePMF]') -> List:
        row_blocks = [self.merge_row_left_to_right(row_id, row, row_tags) for row_id, (row, row_tags) in enumerate(zip(sheet.values, tags))]
        return row_blocks

    def merge_sheet_top_to_bottom(self, row_blocks: List) -> List:
        blocks = []
        up = row_blocks[0]  # Blocks which might be merged with rows below
        for i in range(1, len(row_blocks)):
            down = row_blocks[i]

            j, k = 0, 0
            new_up = []
            while j < len(up) and k < len(down):
                if up[j][1].get_left_col() == down[k][1].get_left_col()\
                        and up[j][1].get_right_col() == down[k][1].get_right_col()\
                        and up[j][0] == down[k][0]:  # Same block type
                    # Merge two blocks
                    new_up.append((
                        up[j][0],
                        SimpleBlock(None, up[j][1].get_left_col(), up[j][1].get_right_col(), up[j][1].get_top_row(),
                                    down[k][1].get_bottom_row())))
                    j += 1
                    k += 1

                elif up[j][1].get_right_col() < down[k][1].get_right_col():
                    blocks.append(up[j])
                    j += 1

                elif down[k][1].get_right_col() < up[j][1].get_right_col():
                    new_up.append(down[k])
                    k += 1

                elif up[j][1].get_right_col() == down[k][1].get_right_col():
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
    def extract_blocks(self, sheet: Sheet, tags: 'np.array[CellTypePMF]') -> List[SimpleBlock]:
        row_blocks = self.merge_sheet_left_to_right(sheet, tags)
        blocks = self.merge_sheet_top_to_bottom(row_blocks)

        new_blocks = []
        # Remove empty blocks
        for _type, block in blocks:
            if _type != "EMPTY":
                new_blocks.append((_type, block))

        blocks = new_blocks

        # Convert old block types to new block types
        new_blocks = []
        for old_type, block in blocks:
            new_type = cell_type_to_block_type_map[old_type]
            if new_type == BasicBlockType.EMPTY:
                continue

            # Attribute can be global, non-global or headers
            if new_type == BasicBlockType.ATTRIBUTE:
                adjacent_block_found = False
                for _, block2 in blocks:
                    if block != block2 and block.is_adjacent(block2):
                        adjacent_block_found = True
                        break
                if not adjacent_block_found:
                    new_type = BasicBlockType.GLOBAL_ATTRIBUTE
                else:
                    # TODO: Block size should not be the only indicator for classifying a block as header
                    block_size = (block.get_right_col() - block.get_left_col() + 1) * (block.get_bottom_row() - block.get_top_row() + 1)
                    if block_size <= 5:
                        new_type = BasicBlockType.HEADER
                    else:
                        new_type = BasicBlockType.ATTRIBUTE ## same as before

            new_blocks.append(SimpleBlock(BlockTypePMF({new_type: 1.0}),
                                          block.get_left_col(), block.get_right_col(),
                                          block.get_top_row(), block.get_bottom_row())
                              )
        return new_blocks
