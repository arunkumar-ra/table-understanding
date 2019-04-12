from type.layout import edge_type

# TODO: NEED tight coupling from labels to inverse dict
inv_edge_labels = {
    0: edge_type.NULL,
    1: edge_type.HEADER,
    2: edge_type.ATTRIBUTE,
    3: edge_type.GLOBAL_ATTRIBUTE,
    4: edge_type.SUPERCATEGORY
}

label_keys = [
    0, 1, 2, 3, 4
]
