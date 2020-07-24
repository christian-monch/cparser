# -*- encoding: utf-8 -*-
"""
A simple lexer for C
"""
import string
from enum import Enum


__author__ = 'Christian Mönch'


EndMarker = '$end'
WordStarter = string.ascii_letters + '_'
WordContinuation = string.ascii_letters + string.digits + '_'


class TokenEnum(Enum):
    UNKNOWN = 'None'
    DIVIDE_ASSIGN = 'Divide_Assign'
    PLUS_ASSIGN = 'Plus_Assign'
    MINUS_ASSIGN = 'Minus_Assign'
    TIMES_ASSIGN = 'Times_Assign'
    MODULE_ASSIGN = 'Module_Assign'
    EQUAL = 'Equal'
    DECREMENT = 'Decrement'
    INCREMENT = 'Increment'
    LOGIC_OR = 'Logic_Or'
    LOGIC_AND = 'Logic_And'
    GREATER_EQUAL = 'Greater_Equal'
    LESS_EQUAL = 'Less_Equal'
    STRUCTURE_DEREFERENCE = 'Structure_Dereference'
    TIMES = 'Times'
    PLUS = 'Plus'
    MINUS = 'Minus'
    DEVIDE = 'Devide'
    MODULE = 'Module'
    ASSIGN = 'Assign'
    LEFT_BRACKET = 'Left_Bracket'
    RIGHT_BRACKET = 'Right_Bracket'
    LEFT_PARENTHESIS = 'Left_Parenthesis'
    RIGHT_PARENTHESIS = 'Right_Parenthesis'
    LEFT_BRACE = 'Left_Brace'
    RIGHT_BRACE = 'Right_Brace'
    OR = 'Or'
    AND = 'And'
    EXOR = 'Exor'
    INVERT = 'Invert'
    NOT = 'Not'
    SEMICOLON = 'Semicolon'
    COLON = 'Colon'
    COMMA = 'Comma'
    DOT = 'Dot'
    LESS = 'Less'
    GREATER = 'Greater'
    QUESTION_MARK = 'Question_Mark'
    BOOL = 'Bool'
    CHAR = 'Char'
    CONST = 'Const'
    INT = 'Int'
    LONG = 'Long'
    FLOAT = 'Float'
    DOUBLE = 'Double'
    SIGNED = 'Signed'
    UNSIGNED = 'Unsigned'
    RESTRICTED = 'Restricted'
    IF = 'If'
    WHILE = 'While'
    DO = 'Do'
    SWITCH = 'Switch'
    BREAK = 'Break'
    GOTO = 'Goto'
    VOID = 'Void'
    TYPEDEF = 'Typedef'
    STRUCT = 'Struct'
    UNION = 'Union'
    VOLATILE = 'Volatile'
    REGISTER = 'Register'
    RETURN = 'Return'
    DEFAULT = 'Default'
    SHORT = 'Short'
    CASE = 'Case'
    INTEGER_CONSTANT = 'Integer_Constant'
    CHARACTER_CONSTANT = 'Character_Constant'
    STRING_CONSTANT = 'String_Constant'
    ID = 'Id'
    PREPROCESSOR_DIRECTIVE = 'Preprocessor_Directive'
    EXTERNAL = 'External'
    STATIC = 'Static'
    COMMENT = 'Comment'
    WHITESPACE = 'Whitespace'
    NUMBER_SIGN = '#'


class Span(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Span(%s, %s)' % (repr(self.start), repr(self.end))


class Token(object):

    def __init__(self, token_type, token_value, span=None):
        self.type = token_type
        self.value = token_value
        self.location = span

    def __repr__(self):
        return 'Token(%s, %s, %s)' % (self.type, repr(self.value), repr(self.location))


class CLexer(object):

    state_plain = 'plain'
    state_comment = 'comment'
    state_line_comment = 'line_comment'

    DoubleToken = {
        '/=': TokenEnum.DIVIDE_ASSIGN,
        '+=': TokenEnum.PLUS_ASSIGN,
        '-=': TokenEnum.MINUS_ASSIGN,
        '*=': TokenEnum.TIMES_ASSIGN,
        '%=': TokenEnum.MODULE_ASSIGN,
        '==': TokenEnum.EQUAL,
        '--': TokenEnum.DECREMENT,
        '++': TokenEnum.INCREMENT,
        '||': TokenEnum.LOGIC_OR,
        '&&': TokenEnum.LOGIC_AND,
        '>=': TokenEnum.GREATER_EQUAL,
        '<=': TokenEnum.LESS_EQUAL,
        '->': TokenEnum.STRUCTURE_DEREFERENCE
    }

    SingleToken = {
        '*': TokenEnum.TIMES,
        '+': TokenEnum.PLUS,
        '-': TokenEnum.MINUS,
        '/': TokenEnum.DEVIDE,
        '%': TokenEnum.MODULE,
        '=': TokenEnum.ASSIGN,
        '[': TokenEnum.LEFT_BRACKET,
        ']': TokenEnum.RIGHT_BRACKET,
        '(': TokenEnum.LEFT_PARENTHESIS,
        ')': TokenEnum.RIGHT_PARENTHESIS,
        '{': TokenEnum.LEFT_BRACE,
        '}': TokenEnum.RIGHT_BRACE,
        '|': TokenEnum.OR,
        '&': TokenEnum.AND,
        '^': TokenEnum.EXOR,
        '~': TokenEnum.INVERT,
        '!': TokenEnum.NOT,
        ';': TokenEnum.SEMICOLON,
        ':': TokenEnum.COLON,
        ',': TokenEnum.COMMA,
        '.': TokenEnum.DOT,
        '<': TokenEnum.LESS,
        '>': TokenEnum.GREATER,
        '?': TokenEnum.QUESTION_MARK
    }

    # "\v\f\n\t\r" == '\x0b\x0c\x0a\x09\x0d'
    EscapeSequences = {
        '\\f':  '\x0c',
        '\\n':  '\x0a',
        '\\t':  '\x09',
        '\\v':  '\x0b',
        '\\r':  '\x0d',
        '\\"':  '"',
        '\\\\':  '\\',
        "\\'":  "'"
    }

    KeyWordTypes = {
        'bool': TokenEnum.BOOL,
        'char': TokenEnum.CHAR,
        'const': TokenEnum.CONST,
        'int': TokenEnum.INT,
        'long': TokenEnum.LONG,
        'float': TokenEnum.FLOAT,
        'double': TokenEnum.DOUBLE,
        'signed': TokenEnum.SIGNED,
        'unsigned': TokenEnum.UNSIGNED,
        'restricted': TokenEnum.RESTRICTED,
        'if': TokenEnum.IF,
        'while': TokenEnum.WHILE,
        'do': TokenEnum.DO,
        'switch': TokenEnum.SWITCH,
        'break': TokenEnum.BREAK,
        'goto': TokenEnum.GOTO,
        'void': TokenEnum.VOID,
        'typedef': TokenEnum.TYPEDEF,
        'struct': TokenEnum.STRUCT,
        'union': TokenEnum.UNION,
        'volatile': TokenEnum.VOLATILE,
        'register': TokenEnum.REGISTER,
        'return': TokenEnum.RETURN,
        'default': TokenEnum.DEFAULT,
        'short': TokenEnum.SHORT,
        'case': TokenEnum.CASE,
        'external': TokenEnum.EXTERNAL,
        'static': TokenEnum.STATIC
    }

    def __init__(self, character_stream):
        self.character_stream = character_stream
        self.current_character = None
        self.current_token_elements = []
        self.ignore_continuation = False
        self.get_next_character()
        self.waiting_tokens = []

    def match_value(self, value):
        if self.current_character:
            if self.current_character.value == value:
                return self.get_next_character()
            raise Exception('unexpected character "%s", expected "%s"' % (self.current_character.value, value))
        raise Exception('unexpected end of file, expected character "%s"' % value)

    def get_next_character(self):
        self.current_character = self.character_stream.get_next_object()
        if not self.ignore_continuation:
            # Check for continuation characters and remove them
            while self.current_character and self.current_character.value == '\\' and self.look_ahead_value(1) == '\n':
                self.current_character = self.character_stream.get_next_object()
                self.current_character = self.character_stream.get_next_object()
        return self.current_character

    def get_next_value(self):
        self.get_next_character()
        return self.current_value()

    def current_value(self):
        if self.current_character is not None:
            return self.current_character.value
        return EndMarker

    def look_ahead(self, count):
        character = self.character_stream.look_ahead(count)
        if character is not None:
            return character.value
        return EndMarker

    def look_ahead_value(self, count):
        character = self.character_stream.look_ahead(count)
        if character is not None:
            return character.value

    def skip_whitespace(self):
        if self.current_value() in string.whitespace:
            self.current_token_elements = []
            while self.current_value() in string.whitespace:
                self.current_token_elements.append(self.current_character)
                self.get_next_character()
            return self.create_token(TokenEnum.WHITESPACE)
        return None

    def skip_inline_whitespace(self):
        if self.current_value() in string.whitespace and self.current_value() != '\n':
            self.current_token_elements = []
            while self.current_value() in string.whitespace and self.current_value() != '\n':
                self.current_token_elements.append(self.current_character)
                self.get_next_character()
            return self.create_token(TokenEnum.WHITESPACE)
        return None

    def create_token(self, token_type, start_coordinate=None, end_coordinate=None):
        if start_coordinate is None:
            start_coordinate = self.current_token_elements[0].coordinate
        if end_coordinate is None:
            end_coordinate = self.current_token_elements[-1].coordinate
        return Token(token_type, ''.join([x.value for x in self.current_token_elements]), Span(
            start_coordinate, end_coordinate))

    def get_next_token(self):
        if self.waiting_tokens:
            return self.waiting_tokens.pop(0)

        # Eat whitespace
        token = self.skip_whitespace()
        if token:
            return token

        # Check preprocessor commands
        if self.current_value() == '#' and self.current_character.coordinate.column == 1:
            return self.read_preprocessor_directive()
        # Check comments
        if self.current_value() == '/' and self.look_ahead_value(1) == '*':
            return self.read_block_comment()
        if self.current_value() == '/' and self.look_ahead_value(1) == '/':
            return self.read_line_comment()

        # Check identifier and keywords
        if self.current_value() in WordStarter:
            self.current_token_elements = [self.current_character]
            while self.get_next_value() in WordContinuation:
                self.current_token_elements.append(self.current_character)
            word = ''.join(x.value for x in self.current_token_elements)
            return self.create_token(self.KeyWordTypes.get(word, TokenEnum.ID))

        # Check numbers
        if self.current_value() in string.digits:
            self.current_token_elements = [self.current_character]
            while self.get_next_value() in string.digits:
                self.current_token_elements.append(self.current_character)
            return self.create_token(TokenEnum.INTEGER_CONSTANT)

        # Check strings
        if self.current_value() == '"':
            return self.read_string_constant()

        # Check chars
        if self.current_value() == '\'':
            return self.read_character_constant()

        # Check double and single character token
        if self.look_ahead_value(1):
            double_value = self.current_value() + self.look_ahead_value(1)
            if double_value in CLexer.DoubleToken:
                self.current_token_elements = [self.current_character, self.get_next_character()]
                self.get_next_character()
                return self.create_token(CLexer.DoubleToken[double_value])
        if self.current_value() in CLexer.SingleToken:
            self.current_token_elements, key = [self.current_character], self.current_value()
            self.get_next_character()
            return self.create_token(CLexer.SingleToken[key])

        # Check for end
        if self.current_value() == EndMarker:
            return None

        # Unknown token
        self.current_token_elements = [self.current_character]
        self.get_next_character()
        return self.create_token(TokenEnum.UNKNOWN)

    def read_word(self):
        """
        read a word: assumes that it is started on the first word character.
        """
        assert self.current_value() in WordStarter
        word_token_elements = [self.current_character]
        while self.get_next_value() in WordContinuation:
            word_token_elements.append(self.current_character)
        return word_token_elements

    def read_preprocessor_directive(self):
        """
        Read a preprocessor directive, assumes we are already on the '#'.
        """
        if self.current_character:
            if self.current_character.value == "#":
                current_token = self.create_token(TokenEnum.NUMBER_SIGN)
            else:
                raise Exception('unexpected character "%s", expected "%s"' % (self.current_character.value, value))
        else:
            raise Exception('unexpected end of file, expected character "%s"' % value)

        self.waiting_tokens.append(self.skip_inline_whitespace())
        self.current_token_elements = self.read_word()
        while self.current_value() != '\n' and self.current_value() != EndMarker:
            self.current_token_elements.append(self.current_character)
            self.get_next_character()
        self.waiting_tokens.append(self.create_token(TokenEnum.PREPROCESSOR_DIRECTIVE))
        return current_token

    def read_block_comment(self):
        self.ignore_continuation = True
        self.current_token_elements = [self.current_character]
        self.current_token_elements.append(self.get_next_character())
        while not (self.get_next_value() == '*' and self.look_ahead_value(1) == '/'):
            if self.current_value() == EndMarker:
                self.ignore_continuation = False
                raise Exception('end of file in block comment')
            self.current_token_elements.append(self.current_character)
        self.current_token_elements.append(self.current_character)
        self.current_token_elements.append(self.get_next_character())
        self.get_next_character()
        self.ignore_continuation = False
        return self.create_token(TokenEnum.COMMENT)

    def read_line_comment(self):
        self.ignore_continuation = True
        self.current_token_elements = [self.current_character]
        self.current_token_elements.append(self.get_next_character())
        while self.get_next_value() != '\n':
            if self.current_value() == EndMarker:
                self.ignore_continuation = False
                raise Exception('end of file in line comment')
            self.current_token_elements.append(self.current_character)
        self.ignore_continuation = False
        return self.create_token(TokenEnum.COMMENT)

    def read_escaped_character(self, next_value):
        escape_sequence = '\\' + next_value
        if escape_sequence not in self.EscapeSequences:
            raise Exception('unknown escape sequence: "%s"' % escape_sequence)
        self.current_character.value = self.EscapeSequences[escape_sequence]
        self.current_token_elements.append(self.current_character)

    def read_escaped_hex_code(self):
        digit_1 = self.current_value()
        digit_2 = self.get_next_value()
        if not digit_2 in string.hexdigits:
            raise Exception('not a hexadecimal digit in escape sequence: %s' % digit_2)
        self.current_character.value = chr(int('%s%s' % (digit_1, digit_2), 16))
        self.current_token_elements.append(self.current_character)

    def read_escaped_octal_code(self):
        digit_1 = self.current_value()
        digit_2 = self.look_ahead(1)
        if not digit_2 in string.octdigits:
            self.current_character.value = chr(int(digit_1, 8))
            self.current_token_elements.append(self.current_character)
            return
        self.get_next_character()
        digit_3 = self.look_ahead(1)
        if not digit_3 in string.octdigits:
            self.current_character.value = chr(int('%s%s' % (digit_1, digit_2), 8))
            self.current_token_elements.append(self.current_character)
            return
        self.get_next_character()
        self.current_character.value = chr(int('%s%s%s' % (digit_1, digit_2, digit_3), 8))
        self.current_token_elements.append(self.current_character)

    def read_escape_sequence(self):
        next_value = self.get_next_value()
        if next_value == EndMarker:
            raise Exception('escape sequence terminated by end of file')
        if next_value == 'x':
            self.get_next_character()
            self.read_escaped_hex_code()
            return
        elif next_value in string.octdigits:
            self.read_escaped_octal_code()
            return
        else:
            self.read_escaped_character(next_value)

    def read_string_constant(self):
        self.current_token_elements = []
        start_coordinate = self.current_character.coordinate
        while self.get_next_value() != '"':
            if self.current_value() in ('\n', EndMarker):
                raise Exception('string terminated by new line or end of file')
            if self.current_value() == '\\':
                self.read_escape_sequence()
            else:
                self.current_token_elements.append(self.current_character)
        end_coordinate = self.current_character.coordinate
        self.get_next_character()
        return self.create_token(TokenEnum.STRING_CONSTANT, start_coordinate, end_coordinate)

    def read_character_constant(self):
        start_coordinate = self.current_character.coordinate
        self.get_next_character()
        self.current_token_elements = []
        if self.current_value() == '\\':
            self.read_escape_sequence()
        else:
            self.current_token_elements.append(self.current_character)
        self.get_next_character()
        if self.current_value() != '\'':
            raise Exception('unterminated string constant:')
        # skip the end tick
        end_coordinate = self.current_character.coordinate
        self.get_next_character()
        return self.create_token(TokenEnum.CHARACTER_CONSTANT, start_coordinate, end_coordinate)


if __name__ == '__main__':
    import sys
    from character_input import FileCharacterInput
    from object_stream import ObjectStream

    input_stream = ObjectStream(FileCharacterInput(sys.stdin, '<stdin>'))
    lexer = CLexer(input_stream)
    token = lexer.get_next_token()
    while token is not None:
        sys.stderr.write(f"{token}\n")
        sys.stdout.write(token.value)
        token = lexer.get_next_token()
