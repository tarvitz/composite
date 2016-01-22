# -*- coding: utf-8 -*-
"""
.. module:: composite.builders.base
    :synopsis: Base builder class
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
from ..const import ATTRIBUTES_META_CLASS


class BaseDocumentBuilder(object):
    """
    Base builder (abstract) class for building/parsing Documents
    """
    parse_visitor_class = None
    build_visitor_class = None

    def __init__(self, document):
        """
        initialize base document builder

        :param composite.documents.Document document: document
        :rtype: None
        :return: None
        """
        self.document = document

    def get_parse_visitor_class(self):
        """
        get parse visitor class

        :rtype: type
        :return: parse visitor class
        """
        return self.parse_visitor_class

    def get_parse_visitor(self):
        """
        get parse visitor

        :rtype: composite.visitors.FieldVisitor
        :return: parse visitor class
        """
        parser_class = self.__class__
        return self.get_parse_visitor_class()(parser_class, self.document)

    def get_build_visitor_class(self):
        """
        get build visitor class

        :rtype: type
        :return: build visitor class
        """
        return self.build_visitor_class

    def get_build_visitor(self, document):
        """
        get build visitor

        :rtype: composite.visitors.FieldVisitor
        :return: build visitor class
        """
        builder_class = self.__class__
        return self.get_build_visitor_class()(builder_class, document)

    def get_document_fields(self):
        """
        get document fields

        :rtype: dict
        :return: document fields
        """
        return self.document._fields

    def get_document_fields_mapping(self):
        """
        get document fields mapping

        :rtype: dict
        :return: mapping
        """
        return self.document._fields_mapping

    def get_attribute_fields(self):
        """
        get document attribute fields

        :rtype: dict
        :return: fields
        """
        return self.document.attributes._fields

    def build_object(self, node_name):
        """
        builds object

        :param str node_name: node name
        :return: object
        :raises NotImplemented:
            - build object should be implemented in real classes
        """
        raise NotImplemented

    def get_attribute_class(self):
        """
        get attribute class

        :rtype: composite.documents.DocumentAttribute
        :return: attribute class
        """
        return getattr(self.document, ATTRIBUTES_META_CLASS, None)

    def build_attributes(self, source_object):
        """
        builds attributes

        :param str source_object: source object
        :return: attribute object
        :raises NotImplemented:
            - build object should be implemented in real classes
        """
        raise NotImplemented

    def init_blank_attributes(self, source_object):
        """
        initiate blank attributes

        :param source_object: source object
        :raises NotImplemented:
            - should be implement in children classes
        """
        raise NotImplemented

    @classmethod
    def iterate(cls, source):
        """
        iterate through source

        :param any source: any source data, for example :py:class:`dict`
        :rtype: generator
        :return: generator with tuple[node name, node content]
        """
        raise NotImplemented

    def parse(self, source):
        """
        parse source data with any format to final document

        :param source: source data (:py:class:`dict`,
            :py:class:`lxml.etree.Element` element, etc)
        :rtype: composite.Document
        :return: document instance
        """
        document = self.document
        fields_mapping = self.get_document_fields_mapping()
        fields = self.get_document_fields()
        visitor = self.get_parse_visitor()

        # #: parse attributes first
        attribute_class = self.get_attribute_class()
        if attribute_class:
            attrs_source = self.build_attributes(source)
            new_attrs = attribute_class.parse(self.__class__, attrs_source)
            setattr(document, '_attributes', new_attrs)

        #: parse nodes
        for field_name, node in self.iterate(source):
            if field_name not in fields_mapping:
                continue
            name = fields_mapping[field_name]
            field = fields[name]
            field.visit(visitor, node)
        return self.document

    def build(self, node_name='document'):
        """
        build instance from python object (document)

        :param str node_name: name of the node to
        :rtype: any
        :return: built instance
        """
        document = self.document
        source_object = self.build_object(node_name)

        visitor = self.get_build_visitor(source_object)
        fields = self.get_document_fields()
        for field_name, field in fields.items():
            field.visit(visitor, getattr(document, field_name))

        if document.has_attributes():
            attribute_fields = self.get_attribute_fields()
            self.init_blank_attributes(source_object)
            for field_name, field in attribute_fields.items():
                field.visit(visitor, getattr(document.attributes, field_name))
        return source_object
