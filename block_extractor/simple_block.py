from block_extractor.block import Block


class SimpleBlock(Block):
    def __init__(self, block_type, left_col, right_col, upper_row, lower_row):
        self.block_type = block_type
        self.left_col = left_col
        self.right_col = right_col
        self.upper_row = upper_row
        self.lower_row = lower_row

    def __hash__(self):
        return hash(str(self))

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

    def is_adjacent(self, otherBlock):
        assert isinstance(otherBlock, self.__class__)

        # left, right
        if self.get_right_col() + 1 == otherBlock.get_left_col():
            if max(self.get_upper_row(), otherBlock.get_upper_row()) <= min(self.get_lower_row(), otherBlock.get_lower_row()):
                return True

        # right, left
        if self.get_left_col() - 1 == otherBlock.get_right_col():
            if max(self.get_upper_row(), otherBlock.get_upper_row()) <= min(self.get_lower_row(), otherBlock.get_lower_row()):
                return True

        # up, down
        if self.get_lower_row() + 1 == otherBlock.get_upper_row():
            if max(self.get_left_col(), otherBlock.get_left_col()) <= min(self.get_right_col(), otherBlock.get_right_col()):
                return True

        # down, up
        if self.get_upper_row() - 1 == otherBlock.get_lower_row():
            if max(self.get_left_col(), otherBlock.get_left_col()) <= min(self.get_right_col(), otherBlock.get_right_col()):
                return True

        return False

    def are_blocks_within_x_row_or_column(self, max_dist, otherBlock):
        assert isinstance(otherBlock, self.__class__)

        # left, right
        if otherBlock.get_left_col() >= self.get_right_col() + 1 and otherBlock.get_left_col() <= self.get_right_col() + max_dist:
            return True

        # right, left
        if otherBlock.get_right_col() >= self.get_left_col() - max_dist and otherBlock.get_right_col() <= self.get_left_col() - 1:
            return True

        # up, down
        if otherBlock.get_upper_row() >= self.get_lower_row() + 1 and otherBlock.get_upper_row() <= self.get_lower_row() + max_dist:
            return True

        # down, up
        if otherBlock.get_lower_row() >= self.get_upper_row() - max_dist and otherBlock.get_lower_row() <= self.get_upper_row() - 1:
            return True

        return False

    def are_blocks_horizontal(self, otherBlock):
        assert isinstance(otherBlock, self.__class__)

        if otherBlock.get_upper_row() != self.get_upper_row():
            return False
        if otherBlock.get_lower_row() != self.get_lower_row():
            return False

        return True

    def are_blocks_vertical(self, otherBlock):
        assert isinstance(otherBlock, self.__class__)

        if otherBlock.get_left_col() != self.get_left_col():
            return False
        if otherBlock.get_right_col() != self.get_right_col():
            return False

        return True

    def __eq__(self, other):  # For testing
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        return "[ {} : ({},{}) to ({},{}) ]".format(self.block_type, self.upper_row, self.left_col, self.lower_row, self.right_col)
