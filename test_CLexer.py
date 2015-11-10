# -*- encoding: utf-8 -*-
from unittest import TestCase
from c_lexer import CLexer
from character_input import StringCharacterInput
from object_stream import ObjectStream


__author__ = 'Christian Mönch'


class TestCLexer(TestCase):
    def test_get_next_token(self):
        input_stream = ObjectStream(StringCharacterInput("""
a  b    c d

/* This is a block comment */


e  f   g

    --- -  /* This is another block
              comment. This time with
              many lines.
              */

        /*/  */

        /**/


"""))
        lexer = CLexer(input_stream)
        token = lexer.get_next_token()
        while token is not None:
            print token
            token = lexer.get_next_token()

