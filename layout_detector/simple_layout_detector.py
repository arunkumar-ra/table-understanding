from layout_detector.layout_detector import LayoutDetector
from type.layout.layout_graph import LayoutGraph
from type.cell import cell_type

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

        if vertex.get_block_type() == cell_type.DATA:
            for idx, block in enumerate(blocks):
                if block.get_block_type() == cell_type.DATE or block.get_block_type() == cell_type.META:
                    n.add(idx)

        return n

    """
    Returns an adjacency list with block_idx as vertex
    """
    def detect_layout(self, sheet, tags, blocks):
        layout_graph = LayoutGraph(blocks)

        for i in range(len(blocks)):
            neighbor_set = self.neighbors(i, blocks)
            for vertex in neighbor_set:
                print (vertex, i, "HI")
                layout_graph.add_edge("meta", vertex, i)

        return layout_graph
