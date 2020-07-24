# -*- encoding: utf-8 -*-
from collections import namedtuple


__author__ = 'Christian Mönch'


Coordinate = namedtuple('Coordinate', ['name', 'line', 'column'])


class Character(object):
    def __init__(self, value, representation=None, encoding=None, coordinate=None):
        self.value = value
        self.representation = representation
        self.encoding = encoding
        self.coordinate = coordinate

    def __repr__(self):
        return 'Character(%s [%s:%d:%d])' % (
            repr(self.value), self.coordinate.name, self.coordinate.line, self.coordinate.column)


class BaseCharacterInput(object):
    def __init__(self, input_name):
        self.input_name = input_name
        self.line = 1
        self.column = 1
        self.end_of_input = False

    def is_newline(self, character):
        return character == '\n'

    def read_character(self):
        raise Exception('subclass responsibility')

    def get_next_object(self):
        if self.end_of_input is True:
            return None
        character = self.read_character()
        if character is None:
            self.end_of_input = True
            return None
        result = Character(character, coordinate=Coordinate(self.input_name, self.line, self.column))
        if self.is_newline(character):
            self.column = 1
            self.line += 1
        else:
            self.column += 1
        return result


class FileCharacterInput(BaseCharacterInput):
    def __init__(self, input_file, file_name='<unknown>'):
        super(FileCharacterInput, self).__init__(file_name)
        self.input_file = input_file
        self.file_name = file_name
        self.waiting_characters = ""

    def read_character(self):
        if self.waiting_characters:
            result, self.waiting_characters = self.waiting_characters[0], self.waiting_characters[1:]
            return result
        self.waiting_characters = self.input_file.read(1)
        if self.waiting_characters == '':
            return None
        result, self.waiting_characters = self.waiting_characters[0], self.waiting_characters[1:]
        return result


class StringCharacterInput(BaseCharacterInput):
    def __init__(self, input_string):
        super(StringCharacterInput, self).__init__('<memory string>')
        self.input_string = input_string
        self.position = 0

    def read_character(self):
        if self.position == len(self.input_string):
            return None
        character = self.input_string[self.position]
        self.position += 1
        return character
