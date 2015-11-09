# -*- encoding: utf-8 -*-
from unittest import TestCase

__author__ = 'Christian Mönch'


from c_parser import *
from collections import namedtuple
from token_stream import TokenStream


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
    def test_declaration(self):
        import logging

        logging.basicConfig(level=logging.DEBUG)

        ts = TokenStream(TokenProvider([
            Token(Token_INT, 'int'),
            Token(Token_POINTER, '*'),
            Token(Token_ID, 'x')
        ]))
        parser = CParser(ts)
        parser.get_next_token()
        parser.declaration()

        ts = TokenStream(TokenProvider([
            Token(Token_INT, 'int'),
            Token(Token_POINTER, '*'),
            Token(Token_ID, 'x'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_RIGHT_PARENTHESIS, ')')
        ]))
        parser = CParser(ts)
        parser.get_next_token()
        parser.declaration()

        ts = TokenStream(TokenProvider([
            Token(Token_INT, 'int'),
            Token(Token_POINTER, '*'),
            Token(Token_ID, 'x'),
            Token(Token_LEFT_BRACKET, '['),
            Token(Token_RIGHT_BRACKET, ']')
        ]))
        parser = CParser(ts)
        parser.get_next_token()
        parser.declaration()

        ts = TokenStream(TokenProvider([
            Token(Token_INT, 'int'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_POINTER, '*'),
            Token(Token_ID, 'x'),
            Token(Token_RIGHT_PARENTHESIS, ')'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_RIGHT_PARENTHESIS, ')')
        ]))
        parser = CParser(ts)
        parser.get_next_token()
        parser.declaration()

        ts = TokenStream(TokenProvider([
            Token(Token_INT, 'int'),
            Token(Token_POINTER, '*'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_POINTER, '*'),
            Token(Token_ID, 'x'),
            Token(Token_RIGHT_PARENTHESIS, ')'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_RIGHT_PARENTHESIS, ')')
        ]))
        parser = CParser(ts)
        parser.get_next_token()
        parser.declaration()

        # Check: char *(*(**foo[][])())[]
        # Result: foo is an array of an array of a pointer to a pointer to a function returning a pointer to an array of a pointer to char
        ts = TokenStream(TokenProvider([
            Token(Token_INT, 'char'),
            Token(Token_POINTER, '*'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_POINTER, '*'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_POINTER, '*'),
            Token(Token_POINTER, '*'),
            Token(Token_ID, 'foo'),
            Token(Token_LEFT_BRACKET, '['),
            Token(Token_RIGHT_BRACKET, ']'),
            Token(Token_LEFT_BRACKET, '['),
            Token(Token_RIGHT_BRACKET, ']'),
            Token(Token_RIGHT_PARENTHESIS, ')'),
            Token(Token_LEFT_PARENTHESIS, '('),
            Token(Token_RIGHT_PARENTHESIS, ')'),
            Token(Token_RIGHT_PARENTHESIS, ')'),
            Token(Token_LEFT_BRACKET, '['),
            Token(Token_RIGHT_BRACKET, ']')
        ]))
        parser = CParser(ts)
        parser.get_next_token()
        parser.declaration()
