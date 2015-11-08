# -*- encoding: utf-8 -*-
from unittest import TestCase
from token_stream import TokenStream


__author__ = 'Christian Mönch'


class TestTokenStream(TestCase):
    class TokenProvider(object):
        def __init__(self, token_list):
            self.token_list = token_list

        def get_next_token(self):
            if self.token_list:
                token = self.token_list[0]
                del self.token_list[0]
                return token
            return None

    def test_get_current_token(self):
        ts = TokenStream(self.TokenProvider(None))
        self.assertEqual(ts.get_current_token(), None)
        ts = TokenStream(self.TokenProvider([0]))
        self.assertEqual(ts.get_current_token(), None)
        self.assertEqual(ts.get_next_token(), 0)
        self.assertEqual(ts.get_current_token(), 0)
        self.assertEqual(ts.get_next_token(), None)
        self.assertEqual(ts.get_current_token(), None)

    def test_get_next_token(self):
        ts = TokenStream(self.TokenProvider([x for x in xrange(4)]))
        for i in xrange(4):
            self.assertEqual(ts.get_next_token(), i)
        self.assertEqual(ts.get_next_token(), None)
        self.assertEqual(ts.get_next_token(), None)

        ts = TokenStream(self.TokenProvider([]))
        self.assertEqual(ts.get_next_token(), None)
        self.assertEqual(ts.get_next_token(), None)

        ts = TokenStream(self.TokenProvider(['a']))
        self.assertEqual(ts.get_next_token(), 'a')
        self.assertEqual(ts.get_next_token(), None)
        self.assertEqual(ts.get_next_token(), None)

    def test_look_ahead(self):
        ts = TokenStream(self.TokenProvider([x for x in xrange(4)]))
        self.assertEqual(ts.get_next_token(), 0)
        for i in xrange(4):
            self.assertEqual(ts.look_ahead(i), i)
        self.assertEqual(ts.look_ahead(4), None)
        self.assertEqual(ts.look_ahead(5), None)
        self.assertEqual(ts.get_next_token(), 1)
        self.assertEqual(ts.get_next_token(), 2)
        self.assertEqual(ts.look_ahead(0), 2)
        self.assertEqual(ts.look_ahead(1), 3)
        self.assertEqual(ts.look_ahead(2), None)
        self.assertEqual(ts.look_ahead(3), None)
        self.assertEqual(ts.get_next_token(), 3)
        self.assertEqual(ts.get_next_token(), None)
        self.assertEqual(ts.get_next_token(), None)

    def test_push_token(self):
        ts = TokenStream(self.TokenProvider([0]))
        self.assertEqual(ts.get_current_token(), None)
        ts.push_token(-1)
        self.assertEqual(ts.get_current_token(), -1)
        self.assertEqual(ts.get_next_token(), 0)
        self.assertEqual(ts.get_current_token(), 0)
        self.assertEqual(ts.get_next_token(), None)
