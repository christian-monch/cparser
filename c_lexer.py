# -*- encoding: utf-8 -*-
"""
A simple lexer for C
"""
__author__ = 'Christian Mönch'


import string


EndMarker = '$end'

WordStarter = string.ascii_letters + '_'
WordContinuation = string.ascii_letters + string.digits + '_'


class Span(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Span(%s, %s)' % (repr(self.start), repr(self.end))


class Token(object):

    Type_None               = 'None'
    Type_Id                 = 'Id'
    Type_Left_Parenthesis   = 'Left_Parenthesis'
    Type_Right_Parenthesis  = 'Right_Parenthesis'
    Type_Left_Bracket       = 'Left_Bracket'
    Type_Right_Bracket      = 'Right_Bracket'
    Type_Left_Brace         = 'Left_Brace'
    Type_Right_Brace        = 'Right_Brace'
    Type_Integer            = 'Integer'
    Type_Unsigned_Integer   = 'Unsigned_Integer'
    Type_Long               = 'Long'
    Type_Unsigned_Long      = 'Unsigned_Long'
    Type_Float              = 'Float'
    Type_Comment            = 'Comment'
    Type_Divide_Assign      = 'Divide_Assign'    # /=
    Type_Plus_Assign        = 'Plus_Assign'      # +=
    Type_Character          = 'Character'
    Type_String             = 'String'

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
        '/=': Token.Type_Divide_Assign,
        '+=': Token.Type_Plus_Assign,
        '-=': 'Minus_Assign',
        '*=': 'Times_Assign',
        '%=': 'Module_Assign',
        '==': 'Equal',
        '--': 'Decrement',
        '++': 'Increment',
        '||': 'Logic_Or',
        '&&': 'Logic_And',
        '>=': 'Greater_Equal',
        '<=': 'Less_Equal'
    }

    SingleToken = {
        '*': 'Times',
        '+': 'Plus',
        '-': 'Minus',
        '/': 'Devide',
        '%': 'Module',
        '=': 'Assign',
        '[': 'Left_Bracket',
        ']': 'Right_Bracket',
        '(': 'Left_Parenthesis',
        ')': 'Right_Parenthesis',
        '{': 'Left_Brace',
        '}': 'Right_Brace',
        '|': 'Or',
        '&': 'And',
        '^': 'Exor',
        '~': 'Invert',
        '!': 'Not',
        ';': 'Semicolon',
        ':': 'Colon',
        ',': 'Comma',
        '.': 'Dot',
        '<': 'Less',
        '>': 'Greater',
        '?': 'Question_Mark',
    }

    # "\v\f\n\t\r" == '\x0b\x0c\x0a\x09\x0d'
    EscapeSequences = {
        '\\f':  '\x0c',
        '\\n':  '\x0a',
        '\\t':  '\x09',
        '\\v':  '\x0b',
        '\\r':  '\x0d',
    }

    KeyWordTypes = {
        'char': 'Char',
        'const': 'Const',
        'int': 'Int',
        'long': 'Long',
        'float': 'Float',
        'double': 'Double',
        'signed': 'Signed',
        'unsigned': 'Unsigned',
        'restricted': 'Restricted',
        'if': 'If',
        'while': 'While',
        'do': 'Do',
        'switch': 'Switch',
        'break': 'Break',
        'goto': 'Goto',
        'void': 'Void',
        'typedef': 'Typedef',
        'struct': 'Struct',
        'union': 'Union',
        'volatile': 'Volatile',
        'register': 'Register'
    }

    def __init__(self, character_stream):
        self.character_stream = character_stream
        self.current_character = None
        self.current_token_elements = []
        self.state = CLexer.state_plain
        self.get_next_character()

    def get_next_character(self):
        self.current_character = self.character_stream.get_next_object()
        while self.current_character and self.current_character.value == '\\' and self.look_ahead_value(1) == '\n':
            # Eat the continuation characters, first the backslash then the newline
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
        while self.current_character and self.current_character.value in string.whitespace:
            self.get_next_character()

    def create_token(self, token_type):
        return Token(token_type, ''.join([x.value for x in self.current_token_elements]), Span(
            self.current_token_elements[0].coordinate, self.current_token_elements[-1].coordinate))

    def get_next_token(self):
        if self.current_character is None:
            return None
        while self.current_character:
            handler = getattr(self, 'handle_' + self.state)
            result = handler()
            if result:
                return result
        return None

    def handle_plain(self):
        # Eat whitespace
        while self.current_value() in string.whitespace:
            self.get_next_character()

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
            # TODO: check for keyword
            word = ''.join(x.value for x in self.current_token_elements)
            return self.create_token(self.KeyWordTypes.get(word, Token.Type_Id))

        # Check numbers
        if self.current_value() in string.digits:
            self.current_token_elements = [self.current_character]
            while self.get_next_value() in string.digits:
                self.current_token_elements.append(self.current_character)
            return self.create_token(Token.Type_Integer)

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
        return self.create_token(Token.Type_None)

    def read_block_comment(self):
        self.current_token_elements = [self.current_character]
        self.current_token_elements.append(self.get_next_character())
        while not (self.get_next_value() == '*' and self.look_ahead_value(1) == '/'):
            if self.current_value() == EndMarker:
                raise Exception('end of file in comment')
            self.current_token_elements.append(self.current_character)
        self.current_token_elements.append(self.current_character)
        self.current_token_elements.append(self.get_next_character())
        self.get_next_character()
        return self.create_token(Token.Type_Comment)

    def read_line_comment(self):
        self.current_token_elements = [self.current_character]
        self.current_token_elements.append(self.get_next_character())
        while self.get_next_value() not in ('\n', EndMarker):
            self.current_token_elements.append(self.current_character)
        return self.create_token(Token.Type_Comment)

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
        digit_2 = self.get_next_value()
        if not digit_2 in string.octdigits:
            raise Exception('not an octal digit in escape sequence: %s' % digit_2)
        digit_3 = self.get_next_value()
        if not digit_3 in string.octdigits:
            raise Exception('not an octal digit in escape sequence: %s' % digit_3)
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
        self.current_token_elements = [self.current_character]
        while self.get_next_value() != '"':
            if self.current_value() in ('\n', EndMarker):
                raise Exception('string terminated by new line or end of file')
            if self.current_value() == '\\':
                self.read_escape_sequence()
            else:
                self.current_token_elements.append(self.current_character)
        self.current_token_elements.append(self.current_character)
        self.get_next_character()
        return self.create_token(Token.Type_String)

    def read_character_constant(self):
        self.current_token_elements = [self.current_character]
        self.get_next_character()
        if self.current_value() == '\\':
            self.read_escape_sequence()
        else:
            self.current_token_elements.append(self.current_character)
        self.get_next_character()
        if self.current_value() != '\'':
            raise Exception('unterminated string constant:')
        self.current_token_elements.append(self.current_character)
        self.get_next_character()
        return self.create_token(Token.Type_Character)


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
