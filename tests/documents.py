# -*- coding: utf-8 -*-

from composite import Document
from composite.fields import Field, AttributeField, ListNode, ListField, Node


class User(Document):
    id = Field(name='id', type=int)
    sign = Field(name='sign', type=str)

    def get_user_name(self):
        if self.get_attributes():
            return '%s %s' % (self.attributes.first_name,
                              self.attributes.last_name)
        return self.id

    def __str__(self):
        return '%s' % self.attributes.first_name

    class Attribute:
        first_name = AttributeField(name='first_name', type=str)
        last_name = AttributeField(name='last_name', type=str)
        age = AttributeField(name='age', type=int)
        gender = AttributeField(name='gender', type=str)
        phone = AttributeField(name='phone', type=str)
        email = AttributeField(name='email', type=str)


class Users(Document):
    """
    users

    :param list[User] users: user list
    """
    users = ListNode(name='profile', type=User)

    def __len__(self):
        return len(self.users)

    def __getitem__(self, item):
        return self.users[item]

    def __iter__(self):
        for user in self.users:
            yield user


class Vector(Document):
    """
    Vector document

    :param float x: x
    :param float y: y
    """
    x = Field('x', type=float)
    y = Field('y', type=float)

    def __str__(self):
        return '(%.2f, %.2f)' % (self.x, self.y)


class Vectors(Document):
    """
    Vectors document

    :param list[Vector] vectors: vector list
    """
    vectors = ListNode('vector', type=Vector)

    def __len__(self):
        return len(self.vectors)

    def __getitem__(self, item):
        return self.vectors[item]


class ValueList(Document):
    """
    Value list

    :param list[int] values: values
    """
    values = ListField('values', int)

    @property
    def total(self):
        return sum(self.values)


class Company(Document):
    """
    Company document

    :param str title: title
    :param str address: address
    :param str company_type: company type
    :param User ceo: company CEO user profile
    """
    title = Field('title', str)
    address = Field('address', str)
    company_type = Field('company_type', str)
    ceo = Node('ceo', type=User)

    def __str__(self):
        return self.ceo.get_user_name()
