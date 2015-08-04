from unittest import TestCase

from composite.fields import Field
from composite.documents import Document
from composite.exceptions import ImproperlyConfigured


class TestAttributes(TestCase):
    def setup_failure_attribute_class(self):
        """
        document class

        :rtype: T <= Document
        :return: document class
        """
        attribute_attrs = {
            'z': Field('z', int)
        }
        attrs = {
            'x': Field('x', int),
            'y': Field('y', int),
            'Attribute': type('Attribute', (), attribute_attrs)
        }
        return type('Vector', (Document, ), attrs)

    def test_attribute_class_failure(self):
        with self.assertRaises(ImproperlyConfigured):
            vector_class = self.setup_failure_attribute_class()
            vector = vector_class.build({'x': 1, 'y': 10})
            self.assertEqual(vector.x, 1)
            self.assertEqual(vector.y, 10)
