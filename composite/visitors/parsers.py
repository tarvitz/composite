# -*- coding: utf-8 -*-
"""
.. module:: composite.visitors.parsers
    :synopsis: Parsers
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
from .base import FieldVisitor


class DictParseVisitor(FieldVisitor):
    """
    """
    def visit_field(self, field, source):
        name = self.composite.field_map[field.name]
        setattr(self.composite, name, field.type(source))

    def visit_list_field(self, field, source):
        name = self.composite.field_map[field.name]
        typ = field.type
        component_list = [typ(x) for x in source]
        setattr(self.composite, name, component_list)

    def visit_node(self, node, source):
        obj = self.composite
        name = obj.field_map[node.name]
        element = node.type.build(source)
        setattr(obj, name, element)

    def visit_list_node(self, node, source):
        obj = self.composite
        name = obj.field_map[node.name]
        append_field = getattr(obj, name)

        for value in source:
            element = node.type.build(value)
            append_field.append(element)

    def visit_attribute_field(self, field, source):
        obj = self.composite
        name = obj.field_map[field.name]
        setattr(obj, name, field.type(source))


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
        getattr(self.composite, name).append(element)
