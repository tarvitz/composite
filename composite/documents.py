from __future__ import unicode_literals

import six
from .exceptions import ImproperlyConfigured
from .fields import MetaField, MetaListField, AttributeField


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
                if (isinstance(field, MetaField)
                        and not isinstance(field, AttributeField)):
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
    def parse(cls, builder_class, source):
        """
        build instance withing build_class and source

        :param builder_class:
        :param source:
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
        :type builder_class:
        :param document:
        :rtype:
        :return: instance
        """
        builder = builder_class(document)
        return builder.build(node_name)

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
    def get_attribute_fields(self):
        return self._fields

    def values(self):
        return [
            getattr(self, name, None)
            for name in self.get_attribute_fields()
        ]
