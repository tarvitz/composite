# -*- coding: utf-8 -*-
"""
.. module:: composite.builers.xml
    :synopsis: XML (lxml) builder
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
from lxml import etree
from .base import BaseDocumentBuilder
from ..visitors import LXMLBuildVisitor, LXMLParseVisitor


class LXMLDocumentBuilder(BaseDocumentBuilder):
    """
    XML documents builder class for parse documents from raw format
    (via lxml) and build to them directly.
    """
    build_visitor_class = LXMLBuildVisitor
    parse_visitor_class = LXMLParseVisitor

    def parse(self, source):
        assert isinstance(source, (etree._Element, etree._Attrib))
        return super(LXMLDocumentBuilder, self).parse(source)

    def build(self, node_name='document'):
        assert (not isinstance(self.document, (etree._Element, etree._Attrib)))
        return super(LXMLDocumentBuilder, self).build(node_name)

    def build_object(self, node_name):
        """
        returns blank lxml.etree.Element object

        :param str node_name: document node name
        :rtype: lxml.etree.Element
        :return: lxml Element instance
        """
        return etree.Element(node_name)

    def build_attributes(self, source_object):
        """
        attributes

        :param lxml.etree.Element source_object: etree element
        :rtype: dict
        :return: attributes
        """
        return source_object.attrib

    def init_blank_attributes(self, source_object):
        """
        lxml etree Element objects already has blank initiated attribute
        children object

        :param lxml._etree.Element source_object: source element
        :return: None
        :rtype: None
        """

    @classmethod
    def iterate(cls, source):
        """
        iterate through source document

        :param source: xml document or
            its attribute
        :type source: lxml.etree.Element | lxml.etree._Attrib
        :rtype: generator
        :return: tuple[node name, node]
        """
        if isinstance(source, etree._Element):
            for node in source.iterchildren():
                yield (node.tag, node)
        else:
            for name, item in source.iteritems():
                yield (name, item)
