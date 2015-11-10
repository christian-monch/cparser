# -*- encoding: utf-8 -*-
from unittest import TestCase
from object_stream import ObjectStream
from character_input import StringCharacterInput


__author__ = 'Christian Mönch'


class TestObjectStream(TestCase):

    class ObjectProvider(object):
        def __init__(self, object_list):
            self.object_list = object_list

        def get_next_object(self):
            if self.object_list:
                next_object = self.object_list[0]
                del self.object_list[0]
                return next_object
            return None

    def test_get_current_object(self):
        os = ObjectStream(self.ObjectProvider(None))
        self.assertEqual(os.get_current_object(), None)
        os = ObjectStream(self.ObjectProvider([0]))
        self.assertEqual(os.get_current_object(), None)
        self.assertEqual(os.get_next_object(), 0)
        self.assertEqual(os.get_current_object(), 0)
        self.assertEqual(os.get_next_object(), None)
        self.assertEqual(os.get_current_object(), None)

    def test_get_next_object(self):
        os = ObjectStream(self.ObjectProvider([x for x in xrange(4)]))
        for i in xrange(4):
            self.assertEqual(os.get_next_object(), i)
        self.assertEqual(os.get_next_object(), None)
        self.assertEqual(os.get_next_object(), None)

        os = ObjectStream(self.ObjectProvider([]))
        self.assertEqual(os.get_next_object(), None)
        self.assertEqual(os.get_next_object(), None)

        os = ObjectStream(self.ObjectProvider(['a']))
        self.assertEqual(os.get_next_object(), 'a')
        self.assertEqual(os.get_next_object(), None)
        self.assertEqual(os.get_next_object(), None)

    def test_look_ahead(self):
        os = ObjectStream(self.ObjectProvider([x for x in xrange(4)]))
        self.assertEqual(os.get_next_object(), 0)
        for i in xrange(4):
            self.assertEqual(os.look_ahead(i), i)
        self.assertEqual(os.look_ahead(4), None)
        self.assertEqual(os.look_ahead(5), None)
        self.assertEqual(os.get_next_object(), 1)
        self.assertEqual(os.get_next_object(), 2)
        self.assertEqual(os.look_ahead(0), 2)
        self.assertEqual(os.look_ahead(1), 3)
        self.assertEqual(os.look_ahead(2), None)
        self.assertEqual(os.look_ahead(3), None)
        self.assertEqual(os.get_next_object(), 3)
        self.assertEqual(os.get_next_object(), None)
        self.assertEqual(os.get_next_object(), None)

    def test_push_object(self):
        os = ObjectStream(self.ObjectProvider([0]))
        self.assertEqual(os.get_current_object(), None)
        os.push_object(-1)
        self.assertEqual(os.get_current_object(), -1)
        self.assertEqual(os.get_next_object(), 0)
        self.assertEqual(os.get_current_object(), 0)
        self.assertEqual(os.get_next_object(), None)
