# -*- coding: utf-8 -*-
"""
.. module:: composite.builders.python
    :synopsis: Python (dict) builder class
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""

from .base import BaseDocumentBuilder
from ..visitors import DictBuildVisitor, DictParseVisitor


class PythonDocumentBuilder(BaseDocumentBuilder):
    """
    Python documents builder class for parse documents from raw (dict) format
    and build to them directly. Could help to build json documents
    with json/simplejson/anyjson/etc.
    """
    build_visitor_class = DictBuildVisitor
    parse_visitor_class = DictParseVisitor

    def parse(self, source):
        assert isinstance(source, (dict, ))
        return super(PythonDocumentBuilder, self).parse(source)

    def build(self, node_name='document'):
        assert (not isinstance(self.document, (dict, )))
        return super(PythonDocumentBuilder, self).build(node_name)

    def build_object(self, node_name):
        return {}

    def build_attributes(self, source_object):
        """
        attributes

        :param dict source_object: source element
        :rtype: dict
        :return: attributes
        """
        return source_object.get('_attributes', {})

    @classmethod
    def iterate(cls, source):
        """
        iterate through source document

        :param lxml.etree.Element source: xml document
        :rtype: generator
        :return: tuple[node name, node]
        """
        for name, item in source.items():
            yield (name, item)

    def init_blank_attributes(self, source_object):
        """
        update source object with attributes

        :param dict source_object: source object
        :return: None
        :rtype: None
        """
        source_object.update({'_attributes': {}})
