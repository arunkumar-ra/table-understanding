import abc
from typing import List


class BlockExtractor(abc.ABC):
    @abc.abstractmethod
    def extract_blocks(self, sheet, tags) -> List:
        pass
