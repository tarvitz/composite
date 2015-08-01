from __future__ import unicode_literals

import six
import lxml
try:
    import simplejson as json
except ImportError:
    import json

from .fields import MetaField, MetaListField


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
                b'Attribute', (DocumentAttribute, ),
                attribute_class.__dict__
            )
            setattr(new_class, b'Attribute', attribute_composite_class)
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

    @staticmethod
    def iterate(source):
        if isinstance(source, lxml.etree._Element):
            for node in source.getchildren():
                yield (node.tag, node)
        elif isinstance(source, lxml.etree._Attrib):
            for name, item in source.iteritems():
                yield (name, item)
        elif isinstance(source, dict):
            for name, item in source.iteritems():
                yield (name, item)
        else:
            raise NotImplemented(
                "Not implemented iterate operation for `%r` "
                "type instance" % type(source)
            )

    @classmethod
    def get_parse_visitor(cls, fmt='dict'):
        if fmt == 'dict':
            return DictBuildVisitor
        elif fmt == 'xml':
            return XMLParseVisitor
        else:
            raise NotImplemented

    @classmethod
    def get_build_visitor(cls, fmt):
        if fmt == 'dict':
            pass
        elif fmt == 'xml':
            return XMLBuildVisitor
        else:
            raise NotImplemented

    @classmethod
    def build(cls, source, fmt='xml'):
        _fields_mapping = cls._fields_mapping
        _fields = cls._fields

        new_obj = cls()
        visitor_class = cls.get_parse_visitor(fmt)
        visitor = visitor_class(new_obj)

        for field_name, node in cls.iterate(source):
            if field_name not in _fields_mapping:
                continue
            name = _fields_mapping[field_name]
            field = _fields[name]
            field.visit(visitor, node)
        return new_obj

    def init_new_obj_for_format(self, node_name, fmt='xml'):
        new_obj = {}
        if fmt == 'xml':
            if isinstance(self, DocumentAttribute):
                new_obj = lxml.etree._Attrib(lxml.etree.Element(node_name))
            else:
                new_obj = lxml.etree.Element(node_name)
        return new_obj

    def to(self, node_name, fmt='xml'):
        new_obj = self.init_new_obj_for_format(node_name, fmt)
        visitor_class = self.get_build_visitor(fmt)
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
        return self.to(node_name, fmt='xml')

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


class FieldVisitor(object):
    """
    """
    def __init__(self, composite):
        self.composite = composite

    def visit_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_list_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_attribute_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_node(self, node, source):
        """

        :param node:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_list_node(self, node, source):
        """

        :param node:
        :param source:
        :return:
        """
        raise NotImplemented


class DictBuildVisitor(FieldVisitor):
    """

    """


class XMLBuildVisitor(FieldVisitor):
    def visit_node(self, node, source):
        self.composite.append(node.type.to(source, node.name, 'xml'))

    def visit_field(self, field, source):
        element = lxml.etree.Element(field.name)
        element.text = str(source)
        self.composite.append(element)

    def visit_list_field(self, field, source):
        visit_field = self.visit_field
        for value in source:
            visit_field(field, value)

    def visit_list_node(self, node, source):
        """
        visit list node

        :param fields.Node node: node
        :param list[Document] source: source
        :rtype: None
        :return: None
        """
        for value in source:
            element = node.type.to(value,  node.name, 'xml')
            if value.has_attributes():
                attrs = value.get_attributes()
                attrib = attrs.to('attrib', 'xml')
                for name, item in attrib.iteritems():
                    element.attrib[name] = str(item)
            self.composite.append(element)

    def visit_attribute_field(self, field, source):
        self.composite[field.name] = str(source)


class XMLParseVisitor(FieldVisitor):
    """
    XML builder
    """
    def visit_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        obj = self.composite
        name = obj.field_map[field.name]
        setattr(self.composite, name, field.type(source.text))

    def visit_list_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        obj = self.composite
        name = obj.field_map[field.name]
        typ = field.type
        getattr(obj, name).append(typ(source.text))

    def visit_attribute_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        obj = self.composite
        name = obj.field_map[field.name]
        setattr(self.composite, name, field.type(source))

    def visit_node(self, node, source):
        """

        :param node:
        :param source:
        :return:
        """
        obj = self.composite
        name = obj.field_map[node.name]
        setattr(self.composite, name, node.type.build(source, 'xml'))

    def visit_list_node(self, node, source):
        """

        :param node:
        :param source:
        :return:
        """
        obj = self.composite
        name = obj.field_map[node.name]
        element = node.type.build(source, 'xml')
        attrib = source.attrib
        attribute = getattr(node.type, 'Attribute', None)
        #: assign attributes
        if attrib and attribute:
            setattr(
                element, '_attributes', attribute.build(attrib, 'xml')
            )
        getattr(self.composite, name).append(element)
