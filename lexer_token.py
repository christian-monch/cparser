# -*- encoding: utf-8 -*-
__author__ = 'Christian Mönch'


from collections import namedtuple


Coordinate = namedtuple('Coordinate', ['file', 'line', 'column'])


class Span(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Token(object):
    def __init__(self, token_type, token_value, span=None):
        self.type = token_type
        self.value = token_value
        self.location = span
