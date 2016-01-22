import json

from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import Company

from composite.builders import LXMLDocumentBuilder, PythonDocumentBuilder


class TestCompany(TestCase):
    maxDiff = None

    def setUp(self):
        with closing(open('documents/company.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

        with closing(open('documents/company.json', 'r')) as doc:
            self.json_file = doc.read()

    def assert_user(self, user):
        """
        make an assertion for user python object

        :param user: user object
        :type user: documents.User
        :raises AssertionError:
            - if user object is non-consistency
        """
        self.assertEqual(user.id, 1)
        self.assertEqual(user.sign, "Pepyako inc.")
        self.assertIn('_attributes', user.__dict__)
        attributes = user.attributes
        self.assertIsInstance(attributes, user.Attributes)
        self.assertEqual(attributes.first_name, "Alexander")
        self.assertEqual(attributes.last_name, "Pepyako")
        self.assertEqual(attributes.age, 23)
        self.assertEqual(attributes.gender, "male")
        self.assertEqual(attributes.phone, "+79110010203")
        self.assertEqual(attributes.email, "com@alexander.pepyako")

    def test_from_xml(self):
        node = etree.XML(self.xml_file)
        company = Company.parse(LXMLDocumentBuilder, node)
        self.assert_user(company.ceo)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)
        company = Company.parse(LXMLDocumentBuilder, source_node)
        xml_node = company.build(LXMLDocumentBuilder, company)
        source = Company.parse(LXMLDocumentBuilder, xml_node)
        self.assert_user(source.ceo)

    def test_from_json(self):
        company = Company.parse(PythonDocumentBuilder,
                                json.loads(self.json_file))
        self.assert_user(company.ceo)

    def test_to_json(self):
        company = Company.parse(PythonDocumentBuilder,
                                json.loads(self.json_file))
        raw_dict = company.build(PythonDocumentBuilder, company)
        raw_json = json.dumps(raw_dict)
        source = Company.parse(PythonDocumentBuilder, json.loads(raw_json))
        self.assert_user(source.ceo)
