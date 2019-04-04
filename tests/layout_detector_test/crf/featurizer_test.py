import unittest
import numpy as np
from cell_classifier.simple_tag import SimpleTag
from block_extractor.simple_block import SimpleBlock
from layout_detector.crf.featurizer import Featurize
from layout_detector.layout_graph import LayoutGraph


class TestFeaturizer(unittest.TestCase):
    def testFeaturizerForSimpleTableWithTwoColumns(self):

        sheet = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('DATE'), SimpleTag('_DATA_')],
                                  [SimpleTag('DATE'), SimpleTag('_DATA_')], [SimpleTag('DATE'), SimpleTag('_DATA_')]])

        b1 = SimpleBlock("META", 0, 1, 0, 0)
        b2 = SimpleBlock("DATE", 0, 0, 1, 3)
        b3 = SimpleBlock("_DATA_", 1, 1, 1, 3)

        blocks = [b1, b2, b3]

        featurizer = Featurize([sheet], [tags], [blocks])
        input_features, _ = featurizer.get_input_features()

        print(input_features)

        # assert input_features == [([[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False]], [[0, 1], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1, 3], [1, 5], [2, 1], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 3], [4, 5], [5, 0], [5, 1], [5, 2], [5, 4]])]
        assert input_features == [([[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False]], [[0, 1], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1, 3], [1, 5], [2, 1], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 3], [4, 5], [5, 0], [5, 1], [5, 2], [5, 4]], [[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False]])]

        layoutGraph = LayoutGraph(blocks)
        layoutGraph.add_edge("header", 0, 1)
        layoutGraph.add_edge("header", 0, 2)
        layoutGraph.add_edge("meta", 1, 2)

        labels = featurizer.get_label_map([layoutGraph])

        assert np.array_equal(labels, [[1, 1, 0, 2, 0, 0]])

    def testFeaturizerForMultiplesTables(self):

        # Table 1
        sheet1 = np.array([['date', 'value'], ['2001', '10.0'], ['2002', '11.0'], ['2003', '12.0']])
        tags1 = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('DATE'), SimpleTag('_DATA_')],
                                  [SimpleTag('DATE'), SimpleTag('_DATA_')], [SimpleTag('DATE'), SimpleTag('_DATA_')]])
        b1_1 = SimpleBlock("META", 0, 1, 0, 0)
        b1_2 = SimpleBlock("DATE", 0, 0, 1, 3)
        b1_3 = SimpleBlock("_DATA_", 1, 1, 1, 3)
        blocks1 = [b1_1, b1_2, b1_3]

        # Table 2
        sheet2 = np.array([['date', 'value'], ['10.0', '2001'], ['11.0', '2002'], ['12.0', '2003']])
        tags2 = np.array([[SimpleTag('META'), SimpleTag('META')], [SimpleTag('_DATA_'), SimpleTag('DATE')],
                          [SimpleTag('_DATA_'), SimpleTag('DATE')], [SimpleTag('_DATA_'), SimpleTag('DATE')]])
        b2_1 = SimpleBlock("META", 0, 1, 0, 0)
        b2_2 = SimpleBlock("_DATA_", 0, 0, 1, 3)
        b2_3 = SimpleBlock("DATE", 1, 1, 1, 3)
        blocks2 = [b2_1, b2_2, b2_3]

        featurizer = Featurize([sheet1, sheet2], [tags1, tags2], [blocks1, blocks2])
        input_features, _ = featurizer.get_input_features()

        print(input_features)

        # assert input_features == [([[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False]], [[0, 1], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1, 3], [1, 5], [2, 1], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 3], [4, 5], [5, 0], [5, 1], [5, 2], [5, 4]]), ([[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False]], [[0, 1], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1, 3], [1, 5], [2, 1], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 3], [4, 5], [5, 0], [5, 1], [5, 2], [5, 4]])]
        assert input_features == [([[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False]], [[0, 1], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1, 3], [1, 5], [2, 1], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 3], [4, 5], [5, 0], [5, 1], [5, 2], [5, 4]], [[0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False]]), ([[0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False]], [[0, 1], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1, 3], [1, 5], [2, 1], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 4], [4, 0], [4, 2], [4, 3], [4, 5], [5, 0], [5, 1], [5, 2], [5, 4]], [[0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 1, 0, 0, 0, 0, 1, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False, 0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 1, 0, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 0, 1, 0, 0, 1, 0, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 1, 0, 0, 0, 0, 0, 1, True, True, True, False, False], [0, 0, 1, 0, 0, 1, 0, 0, True, True, True, True, False, 0, 0, 1, 0, 0, 0, 0, 1, True, True, True, False, False]])]

        layoutGraph1 = LayoutGraph(blocks1)
        layoutGraph1.add_edge("header", 0, 1)
        layoutGraph1.add_edge("header", 0, 2)
        layoutGraph1.add_edge("meta", 1, 2)

        layoutGraph2 = LayoutGraph(blocks1)
        layoutGraph2.add_edge("header", 0, 1)
        layoutGraph2.add_edge("header", 0, 2)
        layoutGraph2.add_edge("meta", 2, 1)

        labels = featurizer.get_label_map([layoutGraph1, layoutGraph2])

        assert np.array_equal(labels, [[1, 1, 0, 2, 0, 0], [1, 1, 0, 0, 0, 2]])

