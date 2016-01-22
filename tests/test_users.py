import json
from lxml import etree
from unittest import TestCase
from contextlib import closing

from tests.documents import Users

from composite.builders import LXMLDocumentBuilder, PythonDocumentBuilder


class TestUsers(TestCase):
    maxDiff = None

    def setUp(self):
        with closing(open('documents/users.xml', 'r')) as doc:
            self.xml_file = doc.read().encode('utf-8')

        with closing(open('documents/users.json', 'r')) as doc:
            self.json_raw = str(doc.read())

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
        """
        parse documents/users.xml
        """
        node = etree.XML(self.xml_file)
        users = Users.parse(LXMLDocumentBuilder, node)
        self.assertEqual(len(users), 2)
        user = users[0]
        self.assert_user(user)

    def test_to_xml(self):
        """
        un-parse user object (with documents/users.xml binding)
        """
        source_node = etree.XML(self.xml_file)
        users = Users.parse(LXMLDocumentBuilder, source_node)
        xml_node = Users.build(LXMLDocumentBuilder, users)
        source = Users.parse(LXMLDocumentBuilder, xml_node)
        self.assertEqual(len(source), 2)
        user = source[0]
        self.assert_user(user)

    def test_from_json(self):
        users = Users.parse(PythonDocumentBuilder, json.loads(self.json_raw))
        self.assertEqual(len(users), 2)
        user = users[0]
        self.assert_user(user)

    def test_to_json(self):
        users = Users.parse(PythonDocumentBuilder, json.loads(self.json_raw))
        self.assertEqual(len(users), 2)

        raw_object = Users.build(PythonDocumentBuilder, users)
        self.assertIsInstance(raw_object, dict)
        self.assertIn('profile', raw_object)
        self.assertEqual(len(raw_object['profile']), 2)
        user = raw_object['profile'][0]

        self.assertEqual(
            user, {
                '_attributes': {
                    "gender": "male",
                    "first_name": "Alexander",
                    "last_name": "Pepyako",
                    "age": 23,
                    "phone": "+79110010203",
                    "email": "com@alexander.pepyako"
                },
                'id': 1,
                'sign': "Pepyako inc."
            }
        )
