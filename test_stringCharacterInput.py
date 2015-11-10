# -*- encoding: utf-8 -*-
from unittest import TestCase
from character_input import StringCharacterInput, Character


__author__ = 'Christian Mönch'


class TestStringCharacterInput(TestCase):
    def compare_value(self, character_object, character):
        return character_object.value == character

    def compare_coordinates(self, character_object, line, column):
        return (character_object.coordinate.line, character_object.coordinate.column) == (line, column)

    def test_basic(self):
        ci = StringCharacterInput('')
        self.assertIsNone(ci.get_next_object())

        ci = StringCharacterInput('abc')
        self.assertTrue(self.compare_value(ci.get_next_object(), 'a'))
        self.assertTrue(self.compare_value(ci.get_next_object(), 'b'))
        self.assertTrue(self.compare_value(ci.get_next_object(), 'c'))
        self.assertIsNone(ci.get_next_object())

        ci = StringCharacterInput('ab\ncd')
        self.assertTrue(self.compare_coordinates(ci.get_next_object(), 1, 1))
        self.assertTrue(self.compare_coordinates(ci.get_next_object(), 1, 2))
        self.assertTrue(self.compare_coordinates(ci.get_next_object(), 1, 3))
        self.assertTrue(self.compare_coordinates(ci.get_next_object(), 2, 1))
        self.assertTrue(self.compare_coordinates(ci.get_next_object(), 2, 2))
