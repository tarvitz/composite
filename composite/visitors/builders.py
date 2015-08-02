# -*- coding: utf-8 -*-
"""
.. module:: composite.visitors.builders
    :synopsis: Builders
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
from lxml import etree
from .base import FieldVisitor


class DictBuildVisitor(FieldVisitor):
    def visit_node(self, node, source):
        self.composite[node.name] = source.to()

    def visit_field(self, field, source):
        self.composite[field.name] = field.type(source)

    def visit_list_field(self, field, source):
        self.composite[field.name] = source

    def visit_list_node(self, node, source):
        """
        visit list node

        :param fields.Node node: node
        :param list[Document] source: source
        :rtype: None
        :return: None
        """
        self.composite[node.name] = []
        component_list = self.composite[node.name]

        for element in source:
            component_list.append(element.to())

    def visit_attribute_field(self, field, source):
        self.composite['_attributes'].update({
            field.name: field.type(source)
        })


class XMLBuildVisitor(FieldVisitor):
    def visit_node(self, node, source):
        self.composite.append(source.to('xml', node.name))

    def visit_field(self, field, source):
        element = etree.Element(field.name)
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
            element = value.to('xml', node.name)
            self.composite.append(element)

    def visit_attribute_field(self, field, source):
        self.composite.attrib[field.name] = str(source)
