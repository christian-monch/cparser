# -*- encoding: utf-8 -*-
from unittest import TestCase

__author__ = 'Christian Mönch'


from c_parser import *
from collections import namedtuple
from object_stream import ObjectStream
from character_input import StringCharacterInput

Token = namedtuple('Token', ['type', 'value'])


class TokenProvider(object):
    def __init__(self, token_list):
        self.token_list = token_list

    def get_next_token(self):
        if self.token_list:
            token = self.token_list[0]
            del self.token_list[0]
            return token
        return None


class TestCParser(TestCase):

    def parser_for(self, source):
        input_stream = ObjectStream(StringCharacterInput(source))
        lexer = CLexer(input_stream)
        return CParser(lexer)

    def test_declaration(self):
        import logging

        logging.basicConfig(level=logging.DEBUG)

        parser = self.parser_for('int *x')
        parser.get_next_token()
        parser.declaration()

        parser = self.parser_for('int *x()')
        parser.get_next_token()
        parser.declaration()

        parser = self.parser_for('int *x[]')
        parser.get_next_token()
        parser.declaration()

        parser = self.parser_for('int (*x)()')
        parser.get_next_token()
        parser.declaration()

        parser = self.parser_for('int *(*x)()')
        parser.get_next_token()
        parser.declaration()

        # Check: char *(*(**foo[][])())[]
        # Result: foo is an array of an array of a pointer to a pointer to a function returning a pointer to an array of a pointer to char
        parser = self.parser_for('char *(*(**foo[][])())[]')
        parser.get_next_token()
        parser.declaration()

    def test_declaration_2(self):
        import logging

        logging.basicConfig(level=logging.DEBUG)

        parser = self.parser_for('int *x')
        parser.get_next_token()
        parser.declaration()
