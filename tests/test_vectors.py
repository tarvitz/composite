from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import Vectors
from composite.builders.xml import LXMLDocumentBuilder


class TestVectors(TestCase):
    def setUp(self):
        with closing(open('documents/vectors.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

    def assert_vector(self, vector):
        """
        make an assertion for user python object

        :param vector: vector object
        :type vector: documents.Vector
        :raises AssertionError:
            - if vector object is non-consistency
        """
        self.assertEqual(vector.x, 1.2)
        self.assertEqual(vector.y, 3.2)

    def test_from_xml(self):
        node = etree.XML(self.xml_file)
        vectors = Vectors.parse(LXMLDocumentBuilder, node)
        self.assertEqual(len(vectors), 3)
        vector = vectors[0]
        self.assert_vector(vector)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)

        vectors = Vectors.parse(LXMLDocumentBuilder, source_node)
        xml_node = Vectors.build(LXMLDocumentBuilder, vectors)
        self.assertIsNotNone(xml_node)
        vectors = Vectors.parse(LXMLDocumentBuilder, xml_node)
        self.assertEqual(len(vectors), 3)
        vector = vectors[0]
        self.assert_vector(vector)
