from layout_detector.layout_detector import LayoutDetector
from layout_detector.crf.featurizer import Featurize


class CRFLayoutDetector(LayoutDetector):
    def detect_layout(self, sheet, tags, blocks):
        # TODO: Read model from file
        ssvm = None

        featurizer = Featurize([sheet], [tags], [blocks])
        X_graph = featurizer.get_input_features()

        predictions = [x for x in ssvm.predict(X_graph)]

        print(predictions)
