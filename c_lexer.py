# -*- encoding: utf-8 -*-
"""
A simple lexer for C
"""
__author__ = 'Christian Mönch'


import string
from character_input import Coordinate


class Span(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return 'Span(%s, %s)' % (repr(self.start), repr(self.end))


class Token(object):

    Type_None               = 0
    Type_Id                 = 1
    Type_Left_Parenthesis   = 2
    Type_Right_Parenthesis  = 3
    Type_Left_Bracket       = 4
    Type_Right_Bracket      = 5
    Type_Left_Brace         = 6
    Type_Right_Brace        = 7
    Type_Integer            = 8
    Type_Unsigned_Integer   = 9
    Type_Long               = 10
    Type_Unsigned_Long      = 11
    Type_Float              = 12
    Type_Comment            = 13
    Type_Divide_Assign      = 14    # /=

    def __init__(self, token_type, token_value, span=None):
        self.type = token_type
        self.value = token_value
        self.location = span

    def __repr__(self):
        return 'Token(%d, %s, %s)' % (self.type, repr(self.value), repr(self.location))


class CLexer(object):

    state_plain = 'plain'
    state_comment = 'comment'
    state_line_comment = 'line_comment'

    def __init__(self, character_stream):
        self.character_stream = character_stream
        self.current_character = None
        self.current_token_elements = []
        self.state = CLexer.state_plain
        self.get_next_character()

    def get_next_character(self):
        self.current_character = self.character_stream.get_next_object()
        return self.current_character

    def look_ahead(self, count):
        return self.character_stream.look_ahead(count)

    def skip_whitespace(self):
        while self.current_character and self.current_character.value in string.whitespace:
            self.current_character = self.character_stream.get_next_object()

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
        if self.current_character.value == '/' and self.look_ahead(1).value == '*':
            return self.read_block_comment()
        token = Token(Token.Type_None, self.current_character.value, Span(
            self.current_character.coordinate, self.current_character.coordinate))
        self.get_next_character()
        return token

    def read_block_comment(self):
        self.current_token_elements = [self.current_character]
        self.current_token_elements.append(self.get_next_character())
        self.get_next_character()
        while self.current_character.value != '*' and self.look_ahead(1).value != '/':
            self.current_token_elements.append(self.current_character)
            self.get_next_character()
        self.current_token_elements.append(self.current_character)
        self.current_token_elements.append(self.get_next_character())
        self.get_next_character()
        token = Token(Token.Type_Comment, ''.join([x.value for x in self.current_token_elements]), Span(
            self.current_token_elements[0].coordinate, self.current_token_elements[-1].coordinate))
        self.current_token_elements = []
        return token

x = """
class CLexer(object):

    state_plain = 'plain'
    state_word = 'word'
    state_number = 'number'
    state_start_comment = 'start_comment'
    state_block_comment = 'block_comment'
    state_line_comment = 'line_comment'

    def __init__(self, byte_stream, name='<unknown>', max_push_back=1):
        self.byte_stream = byte_stream
        self.file_name = name
        self.max_push_back = max_push_back
        self.end_of_stream = False
        self.current_line = 1
        self.current_column = 0
        self.current_byte = None
        self.token_value = ''
        self.token_type = 0
        self.token_start = None
        self.token_end = None
        self.wrap_line = False
        self.state = CLexer.state_plain
        self.pushed_bytes = []
        self.byte_track = []

    def get_next_byte(self):
        if self.pushed_bytes:
            self.byte_track.append(self.pushed_bytes[0])
            self.current_byte, self.current_line, self.current_column = self.pushed_bytes[0]
            del self.pushed_bytes[0]
            return self.current_byte
        if self.end_of_stream is True:
            self.current_byte = None
            return None
        self.byte_track.append((self.current_byte, self.current_column, self.current_line))
        if self.wrap_line is True:
            self.current_line += 1
            self.current_column = 0
        self.current_byte = self.byte_stream.read(1)
        if self.current_byte == '':
            self.end_of_stream = True
            self.current_byte = None
        else:
            if self.current_byte == '\n':
                self.wrap_line = True
            self.current_column += 1
        return self.current_byte

    def push_back_byte(self):
        if len(self.pushed_bytes) >= self.max_push_back:
            raise Exception('Maximum push back reached (%d bytes)' % self.max_push_back)
        if self.byte_track:
            self.current_byte, self.current_line, self.current_column = self.byte_track[0]
            del self.byte_track[0]
        else:
            self.current_byte, self.current_line, self.current_column = (None, 1, 0)

    def get_next_token(self):
        # Make sure to read a character if this is the first call
        if not self.end_of_stream and self.current_byte is None:
            self.get_next_byte()
        while not self.end_of_stream:
            handler = getattr(self, 'handle_' + self.state)
            result = handler(self)
            if result:
                return result
        return None

    def skip_white_space(self):
        while not self.end_of_stream and self.current_byte in string.whitespace:
            self.get_next_byte()

    def record_token_start(self):
        self.token_start = Coordinate(self.file_name, self.current_line, self.current_column)

    def record_token_end(self):
        self.token_end = Coordinate(self.file_name, self.current_line, self.current_column)

    def create_token(self, token_type, token_value):
        return Token(token_type, token_value, Span(self.token_start, self.token_end))

    def handle_plain(self):
        self.skip_white_space()
        if self.current_byte == '_' or self.current_byte in string.ascii_letters:
            self.record_token_start()
            self.token_value = self.current_byte
            return self.read_word()
        if self.current_byte == '/':
            self.record_token_start()
            self.get_next_byte()
            if self.current_byte == '*':
                self.read_block_comment()
            elif self.current_byte == '/':
                self.read_line_comment()
            elif self.current_byte == '=':
                self.record_token_end()
                return self.create_token(Token.Type_Divide_Assign, '/=')

            return None


    def handle_start_comment(self):
        if self.current_byte == '/':
            self.state = CLexer.state_line_comment
"""