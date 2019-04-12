class EdgeType:
    def __init__(self, edge_type: str, edge_id: int):
        self.edge_type = edge_type
        self.edge_id = edge_id

    def str(self):
        return self.edge_type

    def id(self):
        return self.edge_id


NULL = EdgeType("null", 0)
HEADER = EdgeType("header", 1)
ATTRIBUTE = EdgeType("attribute", 2)
GLOBAL_ATTRIBUTE = EdgeType("global_attribute", 3)
SUPERCATEGORY = EdgeType("supercategory", 4)

# Specify domain and range for each edge.

str_to_edge_type_map = {
    "null": NULL,
    "header": HEADER,
    "attribute": ATTRIBUTE,
    "global_attribute": GLOBAL_ATTRIBUTE,
    "supercategory": SUPERCATEGORY
}