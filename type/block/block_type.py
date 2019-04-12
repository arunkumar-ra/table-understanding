class BlockType:

    def __init__(self, block_type: str, block_id: int):
        self.block_type = block_type
        self.block_id = block_id

    def str(self):
        return self.block_type

    def id(self):
        return self.block_id

    @classmethod
    def max_id(cls):
        # [EMPTY, VALUE, ATTRIBUTE, GLOBAL_ATTRIBUTE, HEADER]
        # TODO: Need some way to return this automatically
        return 5


EMPTY = BlockType("empty_block", 0)
VALUE = BlockType("value_block", 1)
ATTRIBUTE = BlockType("attribute_block", 2)
GLOBAL_ATTRIBUTE = BlockType("global_attribute_block", 3)
HEADER = BlockType("header_block", 4)


str_to_block_type_map = {
    "empty_block": EMPTY,
    "value_block": VALUE,
    "attribute_block": ATTRIBUTE,
    "global_attribute_block": GLOBAL_ATTRIBUTE,
    "header_block": HEADER
}