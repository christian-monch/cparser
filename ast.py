# -*- encoding: utf-8 -*-
__author__ = 'Christian Mönch'


class AST(object):
    def __init__(self, span):
        self.span = span


# Objects of this class modify other types
class BaseTypeModifier(AST):
    def __init__(self, span):
        super(BaseTypeModifier, self).__init__(span)
        self.modified_type = None

    def set_modified_type(self, modified_type):
        self.modified_type = modified_type


class Pointer(BaseTypeModifier):
    def __init__(self, modified_type, qualifier, span=None):
        super(Pointer, self).__init__(span)
        self.qualifier = qualifier
        self.set_modified_type(modified_type)


class Function(AST):
    def __init__(self, return_type, parameter, body, qualifier, span=None):
        super(Function, self).__init__(span)
        self.return_type = return_type
        self.parameter = parameter
        self.body = body
        self.qualifier = qualifier

    def set_return_type(self, return_type):
        self.return_type = return_type


class ArrayDeclaration(BaseTypeModifier):
    def __init__(self, modified_type, size, qualifier, span=None):
        super(ArrayDeclaration, self).__init__(span)
        self.size = size
        self.qualifier = qualifier
        self.set_modified_type(modified_type)


class BasicType(AST):
    def __init__(self, type_name, qualifier, span=None):
        super(BasicType, self).__init__(span)
        self.type_name = type_name
        self.qualifier = qualifier


class Identifier(AST):
    def __init__(self, name, span=None):
        super(Identifier, self).__init__(span)
        self.name = name


class TypeModifier(AST):
    def __init__(self, modifier, identifier, span=None):
        super(TypeModifier, self).__init__(span)
        self.modifier = modifier
        self.identifier = identifier


class Declaration(AST):
    def __init__(self, basic_type, modifier, span=None):
        super(Declaration, self).__init__(span)
        self.basic_type = basic_type
        self.modifier = modifier
        self.identifier = modifier.identifier


class DeclarationList(AST):
    def __init__(self, basic_type, modifier_list, span=None):
        super(DeclarationList, self).__init__(span)
        self.basic_type = basic_type
        self.modifier_list = modifier_list
