from __future__ import unicode_literals

import warnings
import six
from lxml import etree
try:
    import simplejson as json
except ImportError:
    import json

from .exceptions import ImproperlyConfigured
from .fields import MetaField, MetaListField, AttributeField
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

    def __init__(cls, name, bases, attrs):
        #: reserved for attributes only
        if cls.__name__ == 'Attribute':
            _errors = []
            for field_name, field in attrs.items():
                if (isinstance(field, MetaField) and not
                        isinstance(field, AttributeField)):
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
    def get_attribute_class(cls):
        """
        get Attribute composite (document) class or None

        :return: self attribute class or None
        """
        return getattr(cls, 'Attribute', None)

    @staticmethod
    def iterate(source):
        if isinstance(source, etree._Element):
            for node in source.getchildren():
                yield (node.tag, node)
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
    def get_source_attributes(cls, source):
        if isinstance(source, dict):
            return source.get('_attributes', {})
        elif isinstance(source, etree._Element):
            return dict(source.attrib)
        else:
            raise NotImplemented

    @classmethod
    def build(cls, source, fmt='dict'):
        _fields_mapping = cls._fields_mapping
        _fields = cls._fields

        new_obj = cls()
        visitor_class = cls.get_parse_visitor_class(fmt)
        visitor = visitor_class(new_obj)

        #: build attributes first
        attrs_source = cls.get_source_attributes(source)
        attribute_class = cls.get_attribute_class()
        if attrs_source and attribute_class:
            new_attrs = attribute_class.build(attrs_source, fmt)
            setattr(new_obj, '_attributes', new_attrs)

        for field_name, node in cls.iterate(source):
            if field_name not in _fields_mapping:
                continue
            name = _fields_mapping[field_name]
            field = _fields[name]
            field.visit(visitor, node)
        return new_obj

    @classmethod
    def parse(cls, builder_class, source):
        """
        build instance withing build_class and source

        :param builder_class:
        :param source:
        :rtype: Document
        :return: document instance
        """
        new_obj = cls()
        builder = builder_class(new_obj)
        return builder.parse(source)

    def init_new_obj_for_format(self, fmt='dict', node_name='DocumentRoot'):
        new_obj = {}
        if fmt == 'xml':
            new_obj = etree.Element(node_name)
        return new_obj

    @staticmethod
    def bind_blank_attributes(new_obj):
        """
        there're two several ways for attributes initialization:

        - build it in schema permanently but blank if they (attributes)
            didn't define,
            would not be nice as end document would have unnecessary blank
            field
        - build it within build visitor but every visit run should perform
            safe check if attribute field exists inside its object.
            Some document classes have already attribute field which could be
            visit safely without any checks, some have not. Lots of checks
            would be cpu time wasting.
        - build attributes before visit operations would perform.
            This way garantee that visitor would run safely without any checks,
            but you should maintain this each new format (that demands it)
            you want to add. For example lxml XML document already has attrib
            field inside new Element, so there's no need to make blank
            attribute instance here.

        :return: None
        :rtype: None
        """
        if isinstance(new_obj, dict):
            new_obj['_attributes'] = {}

    def to(self, fmt='dict', node_name=''):
        warnings.warn('deprecated')
        new_obj = self.init_new_obj_for_format(fmt, node_name)
        visitor_class = self.get_build_visitor_class(fmt)
        visitor = visitor_class(new_obj)
        for field_name, field in self._fields.items():
            field.visit(visitor, getattr(self, field_name))

        if self.has_attributes():
            self.bind_blank_attributes(new_obj)
            for field_name, field in self.attributes._fields.items():
                field.visit(visitor, getattr(self.attributes, field_name))
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
