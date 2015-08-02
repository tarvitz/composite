from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import Company


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
        self.assertIsInstance(attributes, user.Attribute)
        self.assertEqual(attributes.first_name, "Alexander")
        self.assertEqual(attributes.last_name, "Pepyako")
        self.assertEqual(attributes.age, 23)
        self.assertEqual(attributes.gender, "male")
        self.assertEqual(attributes.phone, "+79110010203")
        self.assertEqual(attributes.email, "com@alexander.pepyako")

    def test_from_xml(self):
        node = etree.XML(self.xml_file)
        company = Company.build(node, 'xml')
        self.assert_user(company.ceo)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)
        company = Company.build(source_node, 'xml')
        xml_node = company.to_xml()
        source = Company.from_xml(xml_node)
        self.assert_user(source.ceo)

    def test_from_json(self):
        company = Company.from_json(self.json_file)
        self.assert_user(company.ceo)

    def test_to_json(self):
        company = Company.from_json(self.json_file)
        raw_json = company.to_json()
        source = Company.from_json(raw_json)
        self.assert_user(source.ceo)
