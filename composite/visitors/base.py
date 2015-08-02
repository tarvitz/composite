# -*- coding: utf-8 -*-
"""
.. module:: composite.visitors.base
    :synopsis: Base visitors classes, utils
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""


class FieldVisitor(object):
    """
    """
    def __init__(self, composite):
        self.composite = composite

    def visit_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_list_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_attribute_field(self, field, source):
        """

        :param field:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_node(self, node, source):
        """

        :param node:
        :param source:
        :return:
        """
        raise NotImplemented

    def visit_list_node(self, node, source):
        """

        :param node:
        :param source:
        :return:
        """
        raise NotImplemented
