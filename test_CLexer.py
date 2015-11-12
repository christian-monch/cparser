# -*- encoding: utf-8 -*-
from unittest import TestCase
from c_lexer import CLexer
from character_input import StringCharacterInput
from object_stream import ObjectStream


__author__ = 'Christian Mönch'


class TestCLexer(TestCase):
    def x_test_get_next_token(self):
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

    def process_block_comment(self, block_comment):
        input_stream = ObjectStream(StringCharacterInput(block_comment))
        lexer = CLexer(input_stream)
        return lexer.read_block_comment()

    def process_line_comment(self, block_comment):
        input_stream = ObjectStream(StringCharacterInput(block_comment))
        lexer = CLexer(input_stream)
        return lexer.read_line_comment()

    def process_preprocessor_directive(self, directive):
        input_stream = ObjectStream(StringCharacterInput(directive))
        lexer = CLexer(input_stream)
        return lexer.read_preprocessor_directive()

    def test_read_block_comment(self):
        comment = "/* one line block comment */"
        token = self.process_block_comment(comment)
        self.assertEqual(comment, token.value)

        comment = "/**/"
        token = self.process_block_comment(comment)
        self.assertEqual(comment, token.value)

        comment = "/*/*/"
        token = self.process_block_comment(comment)
        self.assertEqual(comment, token.value)

        # Check muli line
        comment = r"""/*
                      * multi line block comment
                      * 2nd line
                      */"""
        token = self.process_block_comment(comment)
        self.assertEqual(comment, token.value)

        # Check muli line with continuation (which should be preserved
        comment = r"""/*
                       * multi line block comment\
                       * 2nd line
                       */"""
        token = self.process_block_comment(comment)
        self.assertEqual(comment, token.value)

        comment = '/**'
        self.assertRaises(Exception, self.process_block_comment, (comment,))

    def test_read_line_comment(self):
        comment = '// line comment\n'
        token = self.process_line_comment(comment)
        self.assertEqual(comment[:-1], token.value)

        comment = '// line comment     \n'
        token = self.process_line_comment(comment)
        self.assertEqual(comment[:-1], token.value)

        comment = '//\n'
        token = self.process_line_comment(comment)
        self.assertEqual(comment[:-1], token.value)

        comment = '//\\\nx'
        token = self.process_line_comment(comment)
        self.assertEqual(comment[:-2], token.value)

        comment = '//'
        self.assertRaises(Exception, self.process_line_comment, (comment,))

    def test_read_preprocessor_directive(self):
        directive = '#pragma abc\n'
        token = self.process_preprocessor_directive(directive)
        self.assertEqual(directive[1:-1], token.value)

        directive = '#pragma abc'
        token = self.process_preprocessor_directive(directive)
        self.assertEqual(directive[1:], token.value)

        # Check proper continuation handling
        directive = '#pragma a\\\nb'
        token = self.process_preprocessor_directive(directive)
        self.assertEqual('pragma ab', token.value)

        directive = '#pragma abc'
        self.assertRaises(Exception, self.process_preprocessor_directive, (directive,))

    def process_string_constant(self, constant):
        input_stream = ObjectStream(StringCharacterInput(constant))
        lexer = CLexer(input_stream)
        return lexer.read_string_constant()

    def test_string_constant_reading(self):
        constant = '"abc\\n"'
        token = self.process_string_constant(constant)
        self.assertEqual('abc\n', token.value)

        constant = '"abc\\\\"'
        token = self.process_string_constant(constant)
        self.assertEqual('abc\\', token.value)

        constant = '"abc\\\ndef"'
        token = self.process_string_constant(constant)
        self.assertEqual('abcdef', token.value)

        constant = '"abc'
        self.assertRaises(Exception, self.process_string_constant, (constant,))

        constant = '"abc\\"'
        self.assertRaises(Exception, self.process_string_constant, (constant,))

        for sequence, result in ((r'"a\""', 'a"'),
                                 (r'"a\'"', "a'"),
                                 (r'"a\n"', "a\n"),
                                 (r'"a\t"', "a\t"),
                                 (r'"a\v"', "a\v"),
                                 (r'"a\f"', "a\f"),
                                 (r'"a\2"', "a\x02"),
                                 (r'"a\23"', "a\x13"),
                                 (r'"a\234"', "a\x9c")):
            token = self.process_string_constant(sequence)
            self.assertEqual(token.value, result)
