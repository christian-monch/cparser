# -*- encoding: utf-8 -*-
__author__ = 'Christian Mönch'


class TokenStream(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_queue = []

    def get_current_token(self):
        if len(self.token_queue) == 0:
            return None
        return self.token_queue[0]

    def get_next_token(self):
        if self.token_queue:
            del self.token_queue[0]
        if len(self.token_queue) == 0:
            token = self.lexer.get_next_token()
            if token is None:
                return None
            self.token_queue.append(token)
            return self.token_queue[0]
        else:
            return self.token_queue[0]

    def look_ahead(self, count):
        while len(self.token_queue) < count + 1:
            token = self.lexer.get_next_token()
            if token is None:
                return None
            self.token_queue.append(token)
        return self.token_queue[count]

    def push_token(self, token):
        self.token_queue.insert(0, token)
