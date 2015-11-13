# -*- encoding: utf-8 -*-
from unittest import TestCase

__author__ = 'Christian Mönch'


import logging
from c_parser import *
from object_stream import ObjectStream
from character_input import StringCharacterInput
import c_generator


class TestCParser(TestCase):

    def parser_for(self, source):
        input_stream = ObjectStream(StringCharacterInput(source))
        lexer = CLexer(input_stream)
        return CParser(lexer)

    def test_declaration_list(self):
        # TODO: compare results from parser output directly in order to isolate
        # fault detection.
        logging.basicConfig(level=logging.DEBUG)
        for source_code in ('int x[]',
                            'int x[][]',
                            'int *x[]',
                            'int *x',
                            'int *x()',
                            'int (*x)()',
                            'int *(*x)()',
                            'char **foo[][]',
                            'char (**foo[][])()',
                            'char *(**foo[][])()',
                            # Result: foo is an array of an array of a pointer to a pointer to a function returning a pointer to an array of a pointer to char
                            'char (*(**foo[][])())[]',
                            'int *f(int a, char **b)'):
            parser = self.parser_for(source_code)
            parser.get_next_token()
            a = parser.declaration_list()
            generator = c_generator.CGenerator()
            self.assertEqual(generator.show_declaration_list(a[0], a[1]), source_code)

    def test_parameter_list(self):
        logging.basicConfig(level=logging.DEBUG)

        parser = self.parser_for('()')
        parser.get_next_token()
        pl = parser.parameter_list()
        print pl
        self.assertEqual(pl, [])

        parser = self.parser_for('(int argc)')
        parser.get_next_token()
        pl = parser.parameter_list()
        print pl

        parser = self.parser_for('(int argc, char *argv[])')
        parser.get_next_token()
        pl = parser.parameter_list()
        print pl
