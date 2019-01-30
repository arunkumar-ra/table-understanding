import abc


class LayoutDetector(abc.ABC):
    @abc.abstractmethod
    def detect_layout(self, sheet, tags, blocks):
        pass
