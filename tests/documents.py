# -*- coding: utf-8 -*-

from composite import Document
from composite.fields import Field, AttributeField, ListNode, ListField


class User(Document):
    id = Field(name='id', type=int)
    sign = Field(name='sign', type=str)

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
