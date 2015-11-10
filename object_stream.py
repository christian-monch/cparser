# -*- encoding: utf-8 -*-
__author__ = 'Christian Mönch'


class ObjectStream(object):
    def __init__(self, object_stream):
        self.object_stream = object_stream
        self.object_queue = []

    def get_current_object(self):
        if len(self.object_queue) == 0:
            return None
        return self.object_queue[0]

    def get_next_object(self):
        if self.object_queue:
            del self.object_queue[0]
        if len(self.object_queue) == 0:
            new_object = self.object_stream.get_next_object()
            if new_object is None:
                return None
            self.object_queue.append(new_object)
        return self.object_queue[0]

    def look_ahead(self, count):
        while len(self.object_queue) < count + 1:
            next_object = self.object_stream.get_next_object()
            if next_object is None:
                return None
            self.object_queue.append(next_object)
        return self.object_queue[count]

    def push_object(self, an_object):
        self.object_queue.insert(0, an_object)
