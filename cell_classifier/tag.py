import abc


class Tag(abc.ABC):
    @abc.abstractmethod
    def get_tags(self):
        pass
