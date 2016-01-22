# -*- coding: utf-8 -*-
"""
.. module:: documents
    :synopsis: Documents
.. moduleauthor:: NickolasFox <tarvitz@blacklibrary.ru>
.. sectionauthor:: NickolasFox <tarvitz@blacklibrary.ru>
"""

from __future__ import unicode_literals

import six
from .exceptions import ImproperlyConfigured
from .fields import BaseField, MetaListField, AttributeField
from .const import ATTRIBUTES_META_CLASS


class DocumentMeta(type):
    """
    Document Meta class for building documents
    """
    def __new__(cls, name, bases, attrs):
        _fields = {}
        _fields_mapping = {}

        attribute_class = attrs.pop(ATTRIBUTES_META_CLASS, None)
        for field_name, item in attrs.items():
            if isinstance(item, BaseField):
                _fields[field_name] = item
                _fields_mapping[item.name] = field_name
        attrs.update({
            '_fields': _fields,
            '_fields_mapping': _fields_mapping
        })
        new_class = super(DocumentMeta, cls).__new__(cls, name, bases, attrs)
        if attribute_class:
            attribute_composite_class = type(
                str(ATTRIBUTES_META_CLASS), (DocumentAttribute, ),
                dict(attribute_class.__dict__)
            )
            setattr(new_class, str(ATTRIBUTES_META_CLASS),
                    attribute_composite_class)
        return new_class

    def __init__(cls, name, bases, attrs):
        #: reserved for attributes only
        if cls.__name__ == ATTRIBUTES_META_CLASS:
            _errors = []
            for field_name, field in attrs.items():
                if (isinstance(field, BaseField) and
                        not isinstance(field, AttributeField)):
                    _errors.append({
                        'msg': (
                            "Field `%s` has type `%r`" % (field_name,
                                                          type(field))
                        )
                    })
            if _errors:
                raise ImproperlyConfigured(
                    "Attribute class should be configured with "
                    "`AttributeField` only", _errors
                )

        super(DocumentMeta, cls).__init__(name, bases, attrs)


class Document(six.with_metaclass(DocumentMeta)):
    """
    Document (some call them schema) example usage:

    .. code-block:: python

        from composite import Document, fields, builders

        class User(Document):
            name = fields.Field('name', str)
            age = fields.Field('age', int)
            address = fields.Field('address', str)

        user = User.parse(builders.PythonDocumentBuilder,
            {'name': 'Alice', 'age': 10, 'address': 'Wonderland'})
        user.name  # Alice
        User.build(builders.PythonDocumentBuilder, user)
        {'name': 'Alice', 'age': 10, 'address': 'Wonderland'}

    """
    _fields_mapping = {}
    _fields = {}

    def __init__(self):
        for name, item in self._fields.items():
            if isinstance(item, MetaListField):
                setattr(self, name, [])
            else:
                setattr(self, name, item.type())

    def __str__(self):  #: pragma: no cover
        return '0x%08x' % id(self)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())

    @classmethod
    def parse(cls, builder_class, source):
        """
        parse to python-object instance with ``build_class`` ``source`` data

        :param builder_class: builder class
            (:py:class:`composite.builders.BaseDocumentBuilder`)
        :param source: any data to process
        :rtype: composite.Document
        :return: document instance
        """
        new_obj = cls()
        builder = builder_class(new_obj)
        builder.parse(source)
        return new_obj

    @classmethod
    def build(cls, builder_class, document, node_name='Document'):
        """
        build (build composite according to its build class business logic)

        :param builder_class: builder class
            (:py:class:`composite.builders.BaseDocumentBuilder`)
        :param composite.Document document: python instance
            (:py:class:`composite.Document`)
        :rtype: any
        :return: any object, for example lxml.etree.Element if build process
            had been managed with lxml builder class
        """
        builder = builder_class(document)
        return builder.build(node_name)

    def has_attributes(self):
        """
        if document has attributes

        :rtype: bool
        :return: check if given document has attributes
        """
        return hasattr(self, '_attributes')

    def get_attributes(self):
        """
        get attributes node

        :rtype: DocumentAttribute or None
        :return: attributes
        """
        return getattr(self, '_attributes', None)

    @property
    def attributes(self):
        return self.get_attributes()

    @property
    def field_map(self):
        return self._fields_mapping


class DocumentAttribute(Document):
    """
    Base class for building attributes inside
    :py:class:`composite.documents.Document` instances example:

    .. code-block:: python

        from composite import Document, fields, builders

        class User(Document):
            name = fields.Field('name', str)

            class Attribute:
                age = fields.AttributeField('age', int)
                gender = fields.AttributeField('gender', str)

        user = User.parse(builders.PythonDocumentBuilder,
            {'name': 'Alice', '_attributes': {'age': 10, 'gender': 'female'}})
        user.attributes.gender  # female
        User.build(builders.PythonDocumentBuilder, user)
        {'name': 'Alice', '_attributes': {'age': 10, 'gender': 'female'}}
    """
    def get_attribute_fields(self):
        """
        get attribute fields

        :rtype: dict
        :return: fields
        """
        return self._fields

    def values(self):
        """
        attribute values bind

        :rtype: list
        :return: attribute values
        """
        return [
            getattr(self, name, None)
            for name in self.get_attribute_fields()
        ]
