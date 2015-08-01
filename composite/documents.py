from __future__ import unicode_literals

import six
import lxml
try:
    import simplejson as json
except ImportError:
    import json

from .fields import MetaField, MetaListField
from .visitors import (
    DictParseVisitor, DictBuildVisitor, XMLBuildVisitor, XMLParseVisitor
)


class DocumentMeta(type):
    def __new__(cls, name, bases, attrs):
        _fields = {}
        _fields_mapping = {}

        attribute_class = attrs.pop('Attribute', None)
        for field_name, item in attrs.items():
            if isinstance(item, MetaField):
                _fields[field_name] = item
                _fields_mapping[item.name] = field_name
        attrs.update({
            '_fields': _fields,
            '_fields_mapping': _fields_mapping
        })
        new_class = super(DocumentMeta, cls).__new__(cls, name, bases, attrs)
        if attribute_class:
            attribute_composite_class = type(
                str('Attribute'), (DocumentAttribute, ),
                dict(attribute_class.__dict__)
            )
            setattr(new_class, str('Attribute'), attribute_composite_class)
        return new_class


class Document(six.with_metaclass(DocumentMeta)):
    _fields_mapping = {}
    _fields = {}

    def __init__(self):
        for name, item in self._fields.items():
            if isinstance(item, MetaListField):
                setattr(self, name, [])
            else:
                setattr(self, name, item.type())

    def __str__(self):
        return '0x%08x' % id(self)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())

    @classmethod
    def get_attribute_class(cls):
        """
        get Attribute composite (document) class or None

        :return: self attribute class or None
        """
        return getattr(cls, 'Attribute', None)

    @staticmethod
    def iterate(source):
        if isinstance(source, lxml.etree._Element):
            for node in source.getchildren():
                yield (node.tag, node)
        elif isinstance(source, lxml.etree._Attrib):
            for name, item in source.iteritems():
                yield (name, item)
        elif isinstance(source, dict):
            for name, item in six.iteritems(source):
                yield (name, item)
        else:
            raise NotImplemented(
                "Not implemented iterate operation for `%r` "
                "type instance" % type(source)
            )

    @classmethod
    def get_parse_visitor_class(cls, fmt='dict'):
        if fmt == 'dict':
            return DictParseVisitor
        elif fmt == 'xml':
            return XMLParseVisitor
        else:
            raise NotImplemented

    @classmethod
    def get_build_visitor_class(cls, fmt):
        if fmt == 'dict':
            return DictBuildVisitor
        elif fmt == 'xml':
            return XMLBuildVisitor
        else:
            raise NotImplemented

    @classmethod
    def build(cls, source, fmt='dict'):
        _fields_mapping = cls._fields_mapping
        _fields = cls._fields

        new_obj = cls()
        visitor_class = cls.get_parse_visitor_class(fmt)
        visitor = visitor_class(new_obj)

        for field_name, node in cls.iterate(source):
            if field_name not in _fields_mapping:
                continue
            name = _fields_mapping[field_name]
            field = _fields[name]
            field.visit(visitor, node)
        return new_obj

    def init_new_obj_for_format(self, fmt='dict', node_name='DocumentRoot'):
        new_obj = {}
        if fmt == 'xml':
            if isinstance(self, DocumentAttribute):
                new_obj = lxml.etree._Attrib(lxml.etree.Element(node_name))
            else:
                new_obj = lxml.etree.Element(node_name)
        elif fmt == 'dict':
            new_obj = {}
        return new_obj

    def to(self, fmt='dict', node_name=''):
        new_obj = self.init_new_obj_for_format(fmt, node_name)
        visitor_class = self.get_build_visitor_class(fmt)
        visitor = visitor_class(new_obj)
        for field_name, field in self._fields.items():
            field.visit(visitor, getattr(self, field_name))
        return new_obj

    @classmethod
    def from_dict(cls, source):
        return cls.build(source)

    @classmethod
    def from_json(cls, source):
        return cls.build(json.loads(source))

    @classmethod
    def from_xml(cls, source):
        return cls.build(source, 'xml')

    def to_xml(self, node_name='DocumentRoot'):
        return self.to('xml', node_name=node_name)

    def to_json(self):
        return json.dumps(self.to())

    def to_dict(self):
        return self.to()

    def has_attributes(self):
        return hasattr(self, '_attributes')

    def get_attributes(self):
        """
        get attributes node

        :rtype: DocumentAttribute or None
        :return: attributes
        """
        return getattr(self, '_attributes')

    @property
    def attributes(self):
        return self.get_attributes()

    @property
    def field_map(self):
        return self._fields_mapping


class DocumentAttribute(Document):
    """
    For XML attributes
    """
    def iteritems(self):
        for name in self._fields.iterkeys():
            yield (name, getattr(self, name, None))

    def items(self):
        return [
            (name, getattr(self, name, None))
            for name in self._fields.keys()
        ]

    def keys(self):
        return self._fields.keys()

    def values(self):
        return [
            getattr(self, name, None) for name in self._fields.keys()
        ]
