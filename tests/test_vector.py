from lxml import etree
from unittest import TestCase

from contextlib import closing
from tests.documents import Vector

from composite.builders import LXMLDocumentBuilder


class TestVector(TestCase):
    def setUp(self):
        with closing(open('documents/vector.xml', 'r')) as doc:
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
        vector = Vector.parse(LXMLDocumentBuilder, node)
        self.assert_vector(vector)

    def test_build_from_xml(self):
        node = etree.fromstring(self.xml_file)
        vector = Vector.parse(LXMLDocumentBuilder, node)
        self.assert_vector(vector)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)
        vector = Vector.parse(LXMLDocumentBuilder, source_node)
        xml_node = Vector.build(LXMLDocumentBuilder, vector)
        source = Vector.parse(LXMLDocumentBuilder, xml_node)
        self.assert_vector(source)
