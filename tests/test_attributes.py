from unittest import TestCase

from tests.documents import User
from composite.builders import PythonDocumentBuilder


class TestAttributes(TestCase):
    def setUp(self):
        self.source = {
            '_attributes': {
                'first_name': "User",
                "last_name": "last name",
                'age': 30, 'gender': 'male',
                'phone': '79110001020',
                'email': 'user@example.com'
            },
            'id': 1,
            'sign': 'signature'
        }

    def test_attributes(self):
        user = User.parse(PythonDocumentBuilder, self.source)

        self.assertTrue(user.has_attributes())
        attrs = user.get_attributes()
        self.assertEqual(len(attrs.values()), 6)

        self.assertEqual(attrs.first_name, 'User')
        self.assertEqual(attrs.last_name, 'last name')
        self.assertEqual(attrs.age, 30)
        self.assertEqual(attrs.gender, 'male')
        self.assertEqual(attrs.email, 'user@example.com')
        self.assertEqual(attrs.phone, '79110001020')

    def test_access_to__dict_(self):
        user = User.parse(PythonDocumentBuilder, self.source)
        attrs = user.get_attributes()
        try:
            getattr(attrs, '__dict__')
        except TypeError as err:
            self.fail("accessing __dict__ in attributes causes an error")
