from lxml import etree
from unittest import TestCase

from contextlib import closing
from .documents import Vector


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
        """
        parse documents/users.xml
        """
        node = etree.XML(self.xml_file)
        vector = Vector.build(node, 'xml')
        self.assert_vector(vector)

    def test_to_xml(self):
        """
        un-parse user object (with documents/users.xml binding)
        """
        source_node = etree.XML(self.xml_file)
        vector = Vector.build(source_node, 'xml')
        xml_node = vector.to_xml()
        source = Vector.from_xml(xml_node)
        self.assert_vector(source)
