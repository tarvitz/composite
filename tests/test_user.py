from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import User

from composite.builders import LXMLDocumentBuilder, PythonDocumentBuilder


class TestUser(TestCase):
    maxDiff = None

    def setUp(self):
        with closing(open('documents/user.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

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
        user = User.parse(LXMLDocumentBuilder, node)
        self.assert_user(user)

    def test_build_from_xml(self):
        node = etree.fromstring(self.xml_file)
        user = User.parse(LXMLDocumentBuilder, node)
        self.assert_user(user)

    def test_to_xml(self):
        source_node = etree.XML(self.xml_file)
        user = User.parse(LXMLDocumentBuilder, source_node)
        xml_node = User.build(LXMLDocumentBuilder, user)
        source = User.parse(LXMLDocumentBuilder, xml_node)
        self.assert_user(source)

    def test_to_dict(self):
        source_node = etree.XML(self.xml_file)
        user = User.parse(LXMLDocumentBuilder, source_node)
        self.assertEqual(
            User.build(PythonDocumentBuilder, user),
            {
                '_attributes': {
                    'first_name': 'Alexander',
                    'last_name': 'Pepyako',
                    'age': 23,
                    'gender': 'male',
                    'phone': '+79110010203',
                    'email': 'com@alexander.pepyako'
                },
                'id': 1,
                'sign': 'Pepyako inc.'
            }
        )
