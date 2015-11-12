# -*- encoding: utf-8 -*-
"""
A simple lexer for C
"""
__author__ = 'Christian Mönch'


import string


EndMarker = '$end'
WordStarter = string.ascii_letters + '_'
WordContinuation = string.ascii_letters + string.digits + '_'


Token_NONE = 'None'
Token_DIVIDE_ASSIGN = 'Divide_Assign'
Token_PLUS_ASSIGN = 'Plus_Assign'
Token_MINUS_ASSIGN = 'Minus_Assign'
Token_TIMES_ASSIGN = 'Times_Assign'
Token_MODULE_ASSIGN = 'Module_Assign'
Token_EQUAL = 'Equal'
Token_DECREMENT = 'Decrement'
Token_INCREMENT = 'Increment'
Token_LOGIC_OR = 'Logic_Or'
Token_LOGIC_AND = 'Logic_And'
Token_GREATER_EQUAL = 'Greater_Equal'
Token_LESS_EQUAL = 'Less_Equal'
Token_STRUCTURE_DEREFERENCE = 'Structure_Dereference'
Token_TIMES = 'Times'
Token_PLUS = 'Plus'
Token_MINUS = 'Minus'
Token_DEVIDE = 'Devide'
Token_MODULE = 'Module'
Token_ASSIGN = 'Assign'
Token_LEFT_BRACKET = 'Left_Bracket'
Token_RIGHT_BRACKET = 'Right_Bracket'
Token_LEFT_PARENTHESIS = 'Left_Parenthesis'
Token_RIGHT_PARENTHESIS = 'Right_Parenthesis'
Token_LEFT_BRACE = 'Left_Brace'
Token_RIGHT_BRACE = 'Right_Brace'
Token_OR = 'Or'
Token_AND = 'And'
Token_EXOR = 'Exor'
Token_INVERT = 'Invert'
Token_NOT = 'Not'
Token_SEMICOLON = 'Semicolon'
Token_COLON = 'Colon'
Token_COMMA = 'Comma'
Token_DOT = 'Dot'
Token_LESS = 'Less'
Token_GREATER = 'Greater'
Token_QUESTION_MARK = 'Question_Mark'
Token_BOOL = 'Bool'
Token_CHAR = 'Char'
Token_CONST = 'Const'
Token_INT = 'Int'
Token_LONG = 'Long'
Token_FLOAT = 'Float'
Token_DOUBLE = 'Double'
Token_SIGNED = 'Signed'
Token_UNSIGNED = 'Unsigned'
Token_RESTRICTED = 'Restricted'
Token_IF = 'If'
Token_WHILE = 'While'
Token_DO = 'Do'
Token_SWITCH = 'Switch'
Token_BREAK = 'Break'
Token_GOTO = 'Goto'
Token_VOID = 'Void'
Token_TYPEDEF = 'Typedef'
Token_STRUCT = 'Struct'
Token_UNION = 'Union'
Token_VOLATILE = 'Volatile'
Token_REGISTER = 'Register'
Token_RETURN = 'Return'
Token_DEFAULT = 'Default'
Token_SHORT = 'Short'
Token_CASE = 'Case'
Token_INTEGER_CONSTANT = 'Integer_Constant'
Token_CHARACTER_CONSTANT = 'Character_Constant'
Token_STRING_CONSTANT = 'String_Constant'
Token_ID = 'Id'
Token_COMMENT = 'Comment'
Token_PREPROCESSOR_DIRECTIVE = 'Preprocessor_Directive'
Token_EXTERNAL = 'Extternal'
Token_STATIC = 'Static'


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
        '/=': Token_DIVIDE_ASSIGN,
        '+=': Token_PLUS_ASSIGN,
        '-=': Token_MINUS_ASSIGN,
        '*=': Token_TIMES_ASSIGN,
        '%=': Token_MODULE_ASSIGN,
        '==': Token_EQUAL,
        '--': Token_DECREMENT,
        '++': Token_INCREMENT,
        '||': Token_LOGIC_OR,
        '&&': Token_LOGIC_AND,
        '>=': Token_GREATER_EQUAL,
        '<=': Token_LESS_EQUAL,
        '->': Token_STRUCTURE_DEREFERENCE
    }

    SingleToken = {
        '*': Token_TIMES,
        '+': Token_PLUS,
        '-': Token_MINUS,
        '/': Token_DEVIDE,
        '%': Token_MODULE,
        '=': Token_ASSIGN,
        '[': Token_LEFT_BRACKET,
        ']': Token_RIGHT_BRACKET,
        '(': Token_LEFT_PARENTHESIS,
        ')': Token_RIGHT_PARENTHESIS,
        '{': Token_LEFT_BRACE,
        '}': Token_RIGHT_BRACE,
        '|': Token_OR,
        '&': Token_AND,
        '^': Token_EXOR,
        '~': Token_INVERT,
        '!': Token_NOT,
        ';': Token_SEMICOLON,
        ':': Token_COLON,
        ',': Token_COMMA,
        '.': Token_DOT,
        '<': Token_LESS,
        '>': Token_GREATER,
        '?': Token_QUESTION_MARK
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
        'bool': Token_BOOL,
        'char': Token_CHAR,
        'const': Token_CONST,
        'int': Token_INT,
        'long': Token_LONG,
        'float': Token_FLOAT,
        'double': Token_DOUBLE,
        'signed': Token_SIGNED,
        'unsigned': Token_UNSIGNED,
        'restricted': Token_RESTRICTED,
        'if': Token_IF,
        'while': Token_WHILE,
        'do': Token_DO,
        'switch': Token_SWITCH,
        'break': Token_BREAK,
        'goto': Token_GOTO,
        'void': Token_VOID,
        'typedef': Token_TYPEDEF,
        'struct': Token_STRUCT,
        'union': Token_UNION,
        'volatile': Token_VOLATILE,
        'register': Token_REGISTER,
        'return': Token_RETURN,
        'default': Token_DEFAULT,
        'short': Token_SHORT,
        'case': Token_CASE,
        'external': Token_EXTERNAL,
        'static': Token_STATIC
    }

    def __init__(self, character_stream):
        self.character_stream = character_stream
        self.current_character = None
        self.current_token_elements = []
        self.ignore_continuation = False
        self.get_next_character()

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
        while self.current_value() in string.whitespace:
            self.get_next_character()

    def skip_inline_whitespace(self):
        while self.current_value() in string.whitespace and self.current_value() != '\n':
            self.get_next_character()

    def create_token(self, token_type, start_coordinate=None, end_coordinate=None):
        if start_coordinate is None:
            start_coordinate = self.current_token_elements[0].coordinate
        if end_coordinate is None:
            end_coordinate = self.current_token_elements[-1].coordinate
        return Token(token_type, ''.join([x.value for x in self.current_token_elements]), Span(
            start_coordinate, end_coordinate))

    def get_next_token(self):
        # Eat whitespace
        self.skip_whitespace()

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
            return self.create_token(self.KeyWordTypes.get(word, Token_ID))

        # Check numbers
        if self.current_value() in string.digits:
            self.current_token_elements = [self.current_character]
            while self.get_next_value() in string.digits:
                self.current_token_elements.append(self.current_character)
            return self.create_token(Token_INTEGER_CONSTANT)

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
        return self.create_token(Token_NONE)

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
        self.match_value('#')
        self.skip_inline_whitespace()
        self.current_token_elements = self.read_word()
        while self.current_value() != '\n' and self.current_value() != EndMarker:
            self.current_token_elements.append(self.current_character)
            self.get_next_character()
        return self.create_token(Token_PREPROCESSOR_DIRECTIVE)

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
        return self.create_token(Token_COMMENT)

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
        return self.create_token(Token_COMMENT)

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
        return self.create_token(Token_STRING_CONSTANT, start_coordinate, end_coordinate)

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
        return self.create_token(Token_CHARACTER_CONSTANT, start_coordinate, end_coordinate)


if __name__ == '__main__':
    import sys
    from character_input import FileCharacterInput
    from object_stream import ObjectStream

    input_stream = ObjectStream(FileCharacterInput(sys.stdin, '<stdin>'))
    lexer = CLexer(input_stream)
    token = lexer.get_next_token()
    while token is not None:
        print token
        token = lexer.get_next_token()
