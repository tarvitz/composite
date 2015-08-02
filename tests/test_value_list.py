from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import ValueList


class TestValueList(TestCase):
    def setUp(self):
        with closing(open('documents/value_list.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

        with closing(open('documents/value_list.json', 'r')) as doc:
            self.json_file = doc.read()

    def test_from_xml(self):
        node = etree.XML(self.xml_file)
        value_list = ValueList.build(node, 'xml')
        self.assertEqual(value_list.total, 55)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)
        source = ValueList.build(source_node, 'xml')
        xml_node = source.to_xml()
        value_list = ValueList.from_xml(xml_node)
        self.assertEqual(value_list.total, 55)

    def test_from_json(self):
        value_list = ValueList.from_json(self.json_file)
        self.assertEqual(value_list.total, 55)

    def test_to_json(self):
        source = ValueList.from_json(self.json_file)
        json_raw = source.to_json()
        value_list = ValueList.from_json(json_raw)
        self.assertEqual(value_list.total, 55)
