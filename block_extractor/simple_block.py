from block_extractor.block import Block


class SimpleBlock(Block):
    def __init__(self, block_type, left_col, right_col, upper_row, lower_row):
        self.block_type = block_type
        self.left_col = left_col
        self.right_col = right_col
        self.upper_row = upper_row
        self.lower_row = lower_row

    def get_block_type(self):
        return self.block_type

    def get_left_col(self):
        return self.left_col

    def get_right_col(self):
        return self.right_col

    def get_upper_row(self):
        return self.upper_row

    def get_lower_row(self):
        return self.lower_row

    def __eq__(self, other):  # For testing
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        return "[ {} : ({},{}) to ({},{}) ]".format(self.block_type, self.upper_row, self.left_col, self.lower_row, self.right_col)
