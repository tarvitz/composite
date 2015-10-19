# -*- coding: utf-8 -*-
"""
.. module:: composite.visitors.builders
    :synopsis: Builtin builders:
        - dict (python dict)
        - lxml (libxml bindings)
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
from lxml import etree
from .base import FieldVisitor


class DictBuildVisitor(FieldVisitor):
    def visit_node(self, node, source):
        self.composite[node.name] = source.build(self.builder_class, source,
                                                 node.name)

    def visit_field(self, field, source):
        self.composite[field.name] = field.type(source)

    def visit_list_field(self, field, source):
        self.composite[field.name] = source

    def visit_list_node(self, node, source):
        self.composite[node.name] = []
        component_list = self.composite[node.name]
        build_class = self.builder_class
        component_list_append = component_list.append
        for element in source:
            build = element.build
            result = build(build_class, element, node.name)
            component_list_append(result)

    def visit_attribute_field(self, field, source):
        self.composite['_attributes'].update({
            field.name: field.type(source)
        })


class LXMLBuildVisitor(FieldVisitor):
    def visit_node(self, node, source_node):
        self.composite.append(source_node.build(self.builder_class,
                                                source_node, node.name))

    def visit_field(self, field, source_node):
        element = etree.Element(field.name)
        element.text = str(source_node)
        self.composite.append(element)

    def visit_list_field(self, field, source_node):
        visit_field = self.visit_field
        for value in source_node:
            visit_field(field, value)

    def visit_list_node(self, node, source_node):
        builder_class = self.builder_class
        for item in source_node:
            element = item.build(builder_class, item, node.name)
            self.composite.append(element)

    def visit_attribute_field(self, field, source_node):
        self.composite.attrib[field.name] = str(source_node)
