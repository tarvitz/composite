# -*- coding: utf-8 -*-
"""
.. module:: composite.visitors
    :synopsis: Visitors
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""
import lxml


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


class DictParseVisitor(FieldVisitor):
    """
    """

    def visit_field(self, field, source):
        name = self.composite.field_map[field.name]
        setattr(self.composite, name, field.type(source))

    def visit_list_field(self, field, source):
        visit_field = self.visit_field
        name = self.composite.field_map[field.name]
        for value in source:
            getattr(self.composite, name).append(visit_field(field, value))

    def visit_node(self, node, source):
        obj = self.composite
        name = obj.field_map[node.name]
        setattr(obj, name, node.type.build(source))

    def visit_list_node(self, node, source):
        obj = self.composite
        name = obj.field_map[node.name]
        append_field = getattr(obj, name)
        for value in source:
            element = node.type.build(value)
            attrib = value.get('_attributes', {})
            attribute_class = node.type.get_attribute_class()
            if attrib and attribute_class:
                setattr(element, '_attributes', attribute_class.build(attrib))
            append_field.append(element)

    def visit_attribute_field(self, field, source):
        obj = self.composite
        name = obj.field_map[field.name]
        setattr(obj, name, field.type(source))


class DictBuildVisitor(FieldVisitor):
    def visit_node(self, node, source):
        element = node.type.to(source, node.name)
        if element.has_attributes():
            element['_attributes'] = element.attributes.to('_attributes')
        self.composite.append(element)

    def visit_field(self, field, source):
        self.composite[field.name] = field.type(source)

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
        self.composite[node.name] = []
        component = self.composite[node.name]

        for value in source:
            element = value.to()
            if value.has_attributes():
                attrs = value.get_attributes()
                element['_attributes'] = attrs.to()
            component.append(element)

    def visit_attribute_field(self, field, source):
        self.composite[field.name] = field.type(source)


class XMLBuildVisitor(FieldVisitor):
    def visit_node(self, node, source):
        self.composite.append(node.type.to(source, node.name, 'xml'))

    def visit_field(self, field, source):
        element = lxml.etree.Element(field.name)
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
            # element = node.type.to('xml', value, node.name, 'xml')
            element = value.to('xml', node.name)
            if value.has_attributes():
                attrs = value.get_attributes()
                attrib = attrs.to('xml', 'attrib')
                for name, item in attrib.iteritems():
                    element.attrib[name] = str(item)
            self.composite.append(element)

    def visit_attribute_field(self, field, source):
        self.composite[field.name] = str(source)


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
        attrib = source.attrib
        attribute = getattr(node.type, 'Attribute', None)
        #: assign attributes
        if attrib and attribute:
            setattr(
                element, '_attributes', attribute.build(attrib, 'xml')
            )
        getattr(self.composite, name).append(element)
