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
    Field visitor, helps to parse and build documents. There are 5 types of
    fields:

    - ``attribute field``, field attribute:

        .. code-block:: xml

            <font size="12em" color="black" weight="bold">

        ``size``, ``color`` and ``weight`` are attributes

    - ``field``, simple data field:

        .. code-block:: xml
            :emphasize-lines: 2-4

            <Document>
                <x>0</x>
                <name>Jim</name>
                <pi>3.14</pi>
            </Document>

    - ``list field``, simple data fields combined in array/list:

        .. code-block:: xml
            :emphasize-lines: 2-4

            <Document>
                <name>Jim</name>
                <name>Jill</name>
                <name>Jerry</name>
            </Document>
    - ``node``, block with several data in it:

        .. code-block:: xml
            :emphasize-lines: 2-6

            <User>
                <name>Alexander</name>
                <last_name>Pepyako</last_name>
                <age>32</age>
                <email>com@alexander.pepyako</email>
            </User>

    - ``list node``, several nodes combined in array/list:

        .. code-block:: xml
            :emphasize-lines: 2-7

            <Clients>
                <user>
                    <name>Alexander</name>
                    <last_name>Pepyako</last_name>
                    <age>32</age>
                    <email>com@alexander.pepyako</email>
                </user>
                <user>
                    <name>Mary</name>
                    <last_name>Noname</last_name>
                    <age>27</age>
                    <email>mary@noname.nozone</email>
                </user>
            </Clients>
    """
    def __init__(self, builder_class, composite):
        self.builder_class = builder_class
        self.composite = composite

    def visit_attribute_field(self, field, source):
        """
        visit attribute field

        :param field: field to visit
        :type field: composite.fields.AttributeField
        :param source: any source of data
        :rtype: None
        :return: None
        """
        raise NotImplemented

    def visit_field(self, field, source):
        """
        visit field

        :param field: field to visit
        :type field: composite.fields.Field
        :param source: any source of data
        :rtype: None
        :return: None
        """
        raise NotImplemented

    def visit_list_field(self, field, source):
        """
        visit list field

        :param field: field to visit
        :type field: composite.fields.ListField
        :param source: any source of data
        :rtype: None
        :return: None
        """
        raise NotImplemented

    def visit_node(self, node, source):
        """
        visit node

        :param node: node field to visit
        :type node: composite.fields.Node
        :param source: any source of data
        :rtype: None
        :return: None
        """
        raise NotImplemented

    def visit_list_node(self, node, source):
        """
        visit list node

        :param field: field to visit
        :type field: composite.fields.ListNode
        :param source: any source of data
        :rtype: None
        :return: None
        """
        raise NotImplemented
