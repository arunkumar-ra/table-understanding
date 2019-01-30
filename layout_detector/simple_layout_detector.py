from layout_detector.layout_detector import LayoutDetector
from block_extractor import block_types

# """
# Assigns each DATA block to nearest META and DATE blocks as long as they are aligned.
# Assigns each DATE block and META block to nearest DATA block as long as they are aligned.
# """

"""
Creates an edge between each DATA block and all META and DATE blocks.
"""
class SimpleLayoutDetector(LayoutDetector):
    def neighbors(self, idx, blocks) -> set:
        n = set()
        vertex = blocks[idx]

        if vertex.get_block_type() == block_types.DATA:
            for idx, block in enumerate(blocks):
                if block.get_block_type() == block_types.DATE or block.get_block_type() == block_types.META:
                    n.add(idx)

        return n

    """
    Returns an adjacency list with block_idx as vertex
    """
    def detect_layout(self, sheet, tags, blocks):
        layout_graph = [self.neighbors(i, blocks) for i in range(len(blocks))]

        # Make edges bidirectional
        for vertex_num, neighbor_set in enumerate(layout_graph):
            for other_vertex in neighbor_set:
                layout_graph[other_vertex].add(vertex_num)

        return layout_graph
