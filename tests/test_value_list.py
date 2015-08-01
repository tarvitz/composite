from lxml import etree
from unittest import TestCase
from contextlib import closing

from .documents import ValueList


class TestVector(TestCase):
    def setUp(self):
        with closing(open('documents/value_list.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

    def test_from_xml(self):
        """
        parse documents/users.xml
        """
        node = etree.XML(self.xml_file)
        value_list = ValueList.build(node, 'xml')
        self.assertEqual(value_list.total, 55)

    def test_to_xml(self):
        """
        un-parse user object (with documents/users.xml binding)
        """
        source_node = etree.XML(self.xml_file)
        source = ValueList.build(source_node, 'xml')
        xml_node = source.to_xml()
        value_list = ValueList.from_xml(xml_node)
        self.assertEqual(value_list.total, 55)
