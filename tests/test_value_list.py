import json
from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import ValueList

from composite.builders import LXMLDocumentBuilder, PythonDocumentBuilder


class TestValueList(TestCase):
    def setUp(self):
        with closing(open('documents/value_list.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

        with closing(open('documents/value_list.json', 'r')) as doc:
            self.json_file = doc.read()

    def test_from_xml(self):
        node = etree.XML(self.xml_file)
        value_list = ValueList.parse(LXMLDocumentBuilder, node)
        self.assertEqual(value_list.total, 55)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)
        source = ValueList.parse(LXMLDocumentBuilder, source_node)
        xml_node = ValueList.build(LXMLDocumentBuilder, source)
        value_list = ValueList.parse(LXMLDocumentBuilder, xml_node)
        self.assertEqual(value_list.total, 55)

    def test_from_json(self):
        value_list = ValueList.parse(PythonDocumentBuilder,
                                     json.loads(self.json_file))
        self.assertEqual(value_list.total, 55)

    def test_to_json(self):
        source = ValueList.parse(PythonDocumentBuilder,
                                 json.loads(self.json_file))
        json_raw = ValueList.build(PythonDocumentBuilder, source)
        value_list = ValueList.parse(PythonDocumentBuilder, json_raw)
        self.assertEqual(value_list.total, 55)
