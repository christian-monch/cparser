# -*- encoding: utf-8 -*-
from unittest import TestCase
from c_lexer import CLexer
from character_input import StringCharacterInput
from object_stream import ObjectStream


__author__ = 'Christian Mönch'


class TestCLexer(TestCase):
    def test_get_next_token(self):
        input_stream = ObjectStream(StringCharacterInput("""
abcd

/* This is a block comment */


efg

/* bitmaps (as defined by bitmap.h). Note that size here is the size
 * of the bitmap in bits. The on-the-wire format of a bitmap is 64
 * bit words with the bits in big endian order. The in-memory format
 * is an array of 'unsigned long', which may be either 32 or 64 bits.
 */


/* An empty string */  a = "";


    "This is a \\
continuation line"

    --- -  /* This is another block
              comment. This time with
              many lines.
              */

            // This is a comment that goes to the end of the line.


    ;       if (a == 2) {
                f();
                while (8)

#define werwerøwlkerklj dfsdfsdf

#pragma werwerkljwerlkj


            }
        /*/  */

        /**/

        "One \\000 \\x8a \\010 \\111 more string!\\n"
        'c'

    'e' '\\000' '\\x8a' '\\010' '\\111'

    the last few words
"""))
        lexer = CLexer(input_stream)
        token = lexer.get_next_token()
        while token is not None:
            print token
            token = lexer.get_next_token()

