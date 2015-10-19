# -*- coding: utf-8 -*-
"""
.. module:: composite.builders.base
    :synopsis: Base builder class
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""


class BaseDocumentBuilder(object):
    """
    Base builder class for Documents
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

        :rtype: class
        :return: visitor class
        """
        return self.parse_visitor_class

    def get_parse_visitor(self):
        parser_class = self.__class__
        return self.get_parse_visitor_class()(parser_class, self.document)

    def get_build_visitor_class(self):
        """

        :rtype: callable
        :return: callable object
        """
        return self.build_visitor_class

    def get_build_visitor(self, document):
        builder_class = self.__class__
        return self.get_build_visitor_class()(builder_class, document)

    def get_document_fields(self):
        return self.document._fields

    def get_document_fields_mapping(self):
        return self.document._fields_mapping

    def get_attribute_fields(self):
        return self.document.attributes._fields

    def get_source_object(self, node_name):
        """
        get source object

        :param str node_name: node name
        :return: source object
        """
        raise NotImplemented

    def get_attribute_class(self):
        return getattr(self.document, 'Attribute', None)

    def get_attributes_source(self, source):
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

        :param source: lxml element, dict, etc
        :rtype: generator
        :return: generator with tuple[node name, node content]
        """
        raise NotImplemented

    def parse(self, source):
        """
        build instance withing given source

        :param source: source data (dict, lxml element, etc)
        :return:
        """
        document = self.document
        fields_mapping = self.get_document_fields_mapping()
        fields = self.get_document_fields()
        visitor = self.get_parse_visitor()

        # #: parse attributes first
        attribute_class = self.get_attribute_class()
        if attribute_class:
            attrs_source = self.get_attributes_source(source)
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
        build xml instance from python object (document)

        :rtype: lxml.etree._Element
        :return: xml document
        """
        document = self.document
        source_object = self.get_source_object(node_name)

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
