# -*- coding: utf-8 -*-


class ImproperlyConfigured(Exception):
    """
    Improperly configure exception
    """
    def __init__(self, message, errors=None):
        self.errors = errors or []
        self.message = message

    def __repr__(self):
        return self.message
