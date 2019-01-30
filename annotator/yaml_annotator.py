from annotator.abstract_annotator import AbstractAnnotator
from block_extractor.block import Block
from layout_detector.layout_graph import LayoutGraph
import yaml
from typing import List


class YAMLAnnotator(AbstractAnnotator):
    def __init__(self, version=1):
        self.annotation = dict()
        self.annotation['version'] = str(version)
        # self.annotation['components'] = dict()
        self.annotation['transformation'] = dict()
        self.annotation['layout'] = dict()

        self.annotation['relationships'] = dict()
        self.annotation['relationships']['mappings'] = []
        self.annotation['relationships']['semantic_relations'] = dict()

        self.annotation['ontology_prefixes'] = dict()
        self.annotation['ontology_prefixes']['schema'] = 'http://schema.org/'


    def add_layout(self, label, block):
        layout = dict()

        layout['location'] = "{}..{}:{}..{}".format(block.get_upper_row(), block.get_lower_row(),
                                                    block.get_left_col(), block.get_right_col())
        layout['semantic_type'] = "schema:unknown"

        self.annotation['layout'][label] = layout  # TODO: What if two blocks have the same label?

    def add_mapping(self, type, label1, block1, label2, block2):
        # If the two blocks are aligned perfectly, then it should be a one to one mapping.
        mapping_type = "one2one"

        mapping = dict()
        mapping['type'] = type
        mapping[mapping_type] = label1 + ":0 <-> " + label2 + ":0"  # What do the :0s mean here

        self.annotation['relationships']['mappings'].append(mapping)

    def write_yaml(self, annotation: dict, outfile):
        with open(outfile, 'w') as out:
            yaml.dump(annotation, out, default_flow_style=False)
            print("Successfully written yaml output")  # TODO: Use logging module

    def add_layouts(self, layout: LayoutGraph):
        pass

    def add_mappings(self, layout: LayoutGraph):
        for vertex_1 in range(len(layout.nodes)):
            for edge_num in range(len(layout.outEdges[vertex_1])):
                label, vertex_2 = layout.outEdges[vertex_1][edge_num]
                if label == "meta":
                    print ("adding mapping from", vertex_1, "to ", vertex_2)
                    self.add_mapping("dimension_mapping", str(vertex_1), layout.nodes[vertex_1],
                                     str(vertex_2), layout.nodes[vertex_2])

    def get_annotation(self, sheet_index, sheet, tags, blocks: List[Block], layout: LayoutGraph) -> dict:
        # self.write_yaml(self.annotation, "test.yaml")

        label_count = 0
        if blocks:
            for block in blocks:
                self.add_layout("label" + str(label_count), block)
                label_count += 1

        self.add_layouts(layout)
        self.add_mappings(layout)

        return self.annotation
