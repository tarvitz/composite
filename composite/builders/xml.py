# -*- coding: utf-8 -*-
from lxml import etree
from .base import BaseDocumentBuilder
from ..visitors import XMLBuildVisitor, XMLParseVisitor


class XMLAttributeBuilder(BaseDocumentBuilder):
    """
    XML attributes builder
    """
    build_visitor_class = XMLBuildVisitor
    parse_visitor_class = XMLParseVisitor

    def parse(self, source):
        assert isinstance(source, etree._Attrib)
        return super(XMLAttributeBuilder, self).parse(source)

    def iterate(cls, source):
        for name, item in source.items():
            yield (name, item)


class XMLDocumentBuilder(BaseDocumentBuilder):
    """

    """
    build_visitor_class = XMLBuildVisitor
    parse_visitor_class = XMLParseVisitor


    def parse(self, source):
        assert isinstance(source, (etree._Element, etree._Attrib))
        return super(XMLDocumentBuilder, self).parse(source)

    def get_attributes_source(self, source):
        """
        attributes

        :param lxml.etree.Element source: etree element
        :rtype: dict
        :return: attributes
        """
        return source.attrib

    @classmethod
    def iterate(cls, source):
        """
        iterate through source document

        :param lxml.etree.Element source: xml document
        :rtype: generator
        :return: tuple[node name, node]
        """
        # for node in source.getchildren():
        #     yield (node.tag, node)

        if isinstance(source, etree._Element):
            for node in source.getchildren():
                yield (node.tag, node)
        else:
            for name, item in source.items():
                yield (name, item)
