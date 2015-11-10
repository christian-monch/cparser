# -*- encoding: utf-8 -*-
__author__ = 'Christian Mönch'


class AST(object):
    def __init__(self, span):
        self.span = span


class Pointer(AST):
    def __init__(self, referred_type, qualifier, span=None):
        super(Pointer, self).__init__(span)
        self.referred_type = referred_type
        self.qualifier = qualifier


class FunctionDeclaration(AST):
    def __init__(self, return_type, parameter, qualifier, span=None):
        super(FunctionDeclaration, self).__init__(span)
        self.return_type = return_type
        self.parameter = parameter
        self.qualifier = qualifier


class FunctionDefinition(AST):
    def __init__(self, return_type, parameter, qualifier, body, span=None):
        super(FunctionDefinition, self).__init__(span)
        self.return_type = return_type
        self.parameter = parameter
        self.qualifier = qualifier
        self.body = body


class ArrayDeclaration(AST):
    def __init__(self, referred_type, qualifier, span=None):
        super(ArrayDeclaration, self).__init__(span)
        self.referred_type = referred_type
        self.qualifier = qualifier


class BasicType(AST):
    def __init__(self, type_name, qualifier, span=None):
        super(BasicType, self).__init__(span)
        self.type_name = type_name
        self.qualifier = qualifier


class Identifier(AST):
    def __init__(self, name, span=None):
        super(Identifier, self).__init__(span)
        self.name = name
