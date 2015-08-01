# -*- coding: utf-8 -*-
"""
.. module:: fields
    :synopsis: Fields
.. moduleauthor:: NickolasFox <tarvitz@blacklibrary.ru>
.. sectionauthor:: NickolasFox <tarvitz@blacklibrary.ru>
"""


class MetaField(object):
    __slots__ = ['name', 'type', 'default']

    def __init__(self, name, type, default=None):
        """
        initiate field object
        """
        self.name = name
        self.type = type
        self.default = default


class MetaListField(MetaField):
    """
    For list fields, list nodes, list etc usage
    """


class Field(MetaField):
    def visit(self, visitor, source):
        visitor.visit_field(self, source)


class ListField(MetaListField):
    def visit(self, visitor, source):
        visitor.visit_list_field(self, source)


class AttributeField(MetaField):
    def visit(self, visitor, source):
        visitor.visit_attribute_field(self, source)


class Node(MetaField):
    def visit(self, visitor, source):
        return visitor.visit_node(self, source)


class ListNode(MetaListField):
    def visit(self, visitor, source):
        return visitor.visit_list_node(self, source)
