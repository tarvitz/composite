# -*- coding: utf-8 -*-


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
        return self.parse_visitor_class

    def get_parse_visitor(self):
        return self.get_parse_visitor_class()(self.document)

    def get_build_visitor_class(self):
        return self.build_visitor_class

    def get_build_visitor(self):
        return self.get_build_visitor_class()(self.document)

    def get_document_fields(self):
        return self.document._fields

    def get_document_fields_mapping(self):
        return self.document._fields_mapping

    @classmethod
    def iterate(cls, source):
        """
        iterate through source

        :param source: lxml element, dict, etc
        :rtype: generator
        :return: generator with tuple[node name, node content]
        """
        raise NotImplemented

    def get_attribute_class(self):
        return getattr(self.document, 'Attribute', None)

    def get_attributes_source(self, source):
        return {}

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
