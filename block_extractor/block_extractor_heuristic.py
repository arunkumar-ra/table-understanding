from block_extractor.block_extractor import BlockExtractor
from type.block.basic_block_type import BasicBlockType2
from type.block.block_type_pmf import BlockTypePMF
from type.block.simple_block import SimpleBlock
from typing import List
from reader.sheet import Sheet

"""
This block extractor extracts blocks based on the heuristics defined
for one dimenstion and two dimension tables.
Block Types is defined in block_extractor.new_block_types
"""

class BlockExtractorHeuristic(BlockExtractor):
    def __init__(self):
        pass

    def is1d(self, sheet):        
        columnValues = {}        

        for i, row in enumerate(sheet):            
            for j, col in enumerate(row):
                if i > 0 and j == 0:                    
                    if col in columnValues:
                        return True
                    columnValues[col] = True
        return False

    def extract_blocks(self, sheet: Sheet, tags: 'np.array[CellTypePMF]') -> List[SimpleBlock]:        
        allBlocks = []
        sheet = sheet.values.tolist()

        if (self.is1d(sheet)):            
            columnBlocks = {}
            column_header = []
            columns = []

            for i, row in enumerate(sheet):
                for j, col in enumerate(row):
                        if i==0:
                            column_header.append((i,j))
                            columnBlocks[col] = []
                            columns.append(col)
                        else:                            
                            columnBlocks[columns[j]].append((i,j))
            
            allBlocks.append(SimpleBlock(BlockTypePMF({BasicBlockType2.COLUMN_HEAD: 1.0}),
                                          column_header[0][1], column_header[-1][1],
                                          column_header[0][0], column_header[-1][0])
                              )
            
            for blockName in columnBlocks:                
                allBlocks.append(SimpleBlock(BlockTypePMF({BasicBlockType2.DATA: 1.0}),
                                          columnBlocks[blockName][0][1], columnBlocks[blockName][-1][1],
                                          columnBlocks[blockName][0][0], columnBlocks[blockName][-1][0])
                              )

        else:
            metadata = []
            data = []
            column_header = []
            row_header = []

            for i, row in enumerate(sheet):
                for j, col in enumerate(row):

                    if col.strip() != '':
                        if i == 0 and j == 0:
                            metadata.append((i, j))
                        elif i == 0:
                            column_header.append((i, j))
                        elif j == 0:
                            row_header.append((i, j))
                        else:
                            data.append((i, j))
            allBlocks.append(SimpleBlock(BlockTypePMF({BasicBlockType2.METADATA: 1.0}),
                                              metadata[0][1], metadata[-1][1],
                                              metadata[0][0], metadata[-1][0])
                            )
            
            allBlocks.append(SimpleBlock(BlockTypePMF({BasicBlockType2.DATA: 1.0}),
                                              data[0][1], data[-1][1],
                                              data[0][0], data[-1][0])
                            )
            
            allBlocks.append(SimpleBlock(BlockTypePMF({BasicBlockType2.COLUMN_HEAD: 1.0}),
                                              column_header[0][1], column_header[-1][1],
                                              column_header[0][0], column_header[-1][0])
                            )
            
            allBlocks.append(SimpleBlock(BlockTypePMF({BasicBlockType2.ROW_HEAD: 1.0}),
                                              row_header[0][1], row_header[-1][1],
                                              row_header[0][0], row_header[-1][0])
                            )
        return allBlocks