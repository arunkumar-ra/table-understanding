from cell_classifier.tag import Tag


class SimpleTag(Tag):
    def __init__(self, tags: str):
        self.tags = tags

    def get_tags(self) -> str:
        return self.tags

    def __eq__(self, other):  # For testing
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        return self.tags
