import abc


class Block(abc.ABC):
    @abc.abstractmethod
    def get_block_type(self):
        pass

    @abc.abstractmethod
    def get_left_col(self):
        pass

    @abc.abstractmethod
    def get_right_col(self):
        pass

    @abc.abstractmethod
    def get_upper_row(self):
        pass

    @abc.abstractmethod
    def get_lower_row(self):
        pass
