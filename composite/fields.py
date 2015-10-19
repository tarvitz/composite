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
    """
    Field processes simple types of data, for example: int, float, str:

    .. code-block:: python

        age = Field('age', int, 21)
        name = Field('name', str, '')
    """
    def visit(self, visitor, source):
        visitor.visit_field(self, source)


class ListField(MetaListField):
    """
    List of fields combined together:

    .. code-block:: python

        mana_cost = ListField('mana_cost', int, [90, 100, 110, 120])
        player_names = ListField('player_names', str)  # empty list, []
    """
    def visit(self, visitor, source):
        visitor.visit_list_field(self, source)


class AttributeField(MetaField):
    """
    Same as :py:class:`composite.fields.Field` but using only in attributes, as
    they include only simple data.

    .. code-block:: python

        age = AttributeField('age', int)  # int() by default
    """
    def visit(self, visitor, source):
        visitor.visit_attribute_field(self, source)


class Node(MetaField):
    """
    Node field serves to read different data types combined together (ADT).

    .. code-block:: python
        :emphasize-lines: 10-11

        class User(Document):
            age = Field('age', int)
            name = Field('name', str)

        class Company(Document):
            title = Field('title', str)
            address = Field('address', str)

        class Profile(Document):
            user = Node('user', User)
            company = Node('company', Company)
    """
    def visit(self, visitor, source):
        return visitor.visit_node(self, source)


class ListNode(MetaListField):
    """
    List of nodes

    .. code-block:: python
        :emphasize-lines: 6

        class User(Document):
            age = Field('age', int)
            name = Field('name', str)

        class Users(Document):
            users = ListNode('users', User)
    """
    def visit(self, visitor, source):
        return visitor.visit_list_node(self, source)
