# -*- coding: utf-8 -*-
"""
.. module:: composite.visitors.parsers
    :synopsis: Builtin parsers
        - dict (python dict)
        - lxml (libxml bindings)
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
from .base import FieldVisitor


class DictParseVisitor(FieldVisitor):
    def visit_attribute_field(self, field, raw_node):
        document = self.composite
        name = document.field_map[field.name]
        setattr(document, name, field.type(raw_node))

    def visit_field(self, field, raw_node):
        name = self.composite.field_map[field.name]
        setattr(self.composite, name, field.type(raw_node))

    def visit_list_field(self, field, raw_node):
        name = self.composite.field_map[field.name]
        typ = field.type
        component_list = [typ(x) for x in raw_node]
        setattr(self.composite, name, component_list)

    def visit_node(self, node, raw_node):
        document = self.composite
        name = document.field_map[node.name]
        element = node.type.parse(self.builder_class, raw_node)
        setattr(document, name, element)

    def visit_list_node(self, node, raw_node):
        document = self.composite
        name = document.field_map[node.name]
        append_field = getattr(document, name)
        builder_class = self.builder_class
        for value in raw_node:
            element = node.type.parse(builder_class, value)
            append_field.append(element)


class LXMLParseVisitor(FieldVisitor):
    def visit_attribute_field(self, field, raw_node):
        document = self.composite
        name = document.field_map[field.name]
        setattr(self.composite, name, field.type(raw_node))

    def visit_field(self, field, raw_node):
        document = self.composite
        name = document.field_map[field.name]
        setattr(self.composite, name, field.type(raw_node.text))

    def visit_list_field(self, field, raw_node):
        document = self.composite
        name = document.field_map[field.name]
        typ = field.type
        getattr(document, name).append(typ(raw_node.text))

    def visit_node(self, node, raw_node):
        document = self.composite
        name = document.field_map[node.name]
        element = node.type.parse(self.builder_class, raw_node)
        setattr(self.composite, name, element)

    def visit_list_node(self, node, raw_node):
        document = self.composite
        name = document.field_map[node.name]
        element = node.type.parse(self.builder_class, raw_node)
        getattr(self.composite, name).append(element)
