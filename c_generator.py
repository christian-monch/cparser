# -*- encoding: utf-8 -*-
__author__ = 'Christian Mönch'


import ast


class CGenerator(object):
    def __init__(self):
        pass

    # Case function:
    # The difficult case is the function. E.g. <t> is function returning <r>:
    # This should yield: <r><t>(). E.g. <variable x> is a function return a <pointer to>
    # <pointer to><variable x>() =>  *x()
    # At the point where we see the function, we have already read <t>. So we have to store
    # it and use it correctly.
    #
    # Case: array:
    # E.g. we have an array of ... So the array is built from what we will read.
    # x is a pointer to an array of pointer:  *(*x)[]
    # <t> is an array of: <t>[]
    def show_type(self, type_string, current_type):
        if current_type is None:
            return type_string
        if isinstance(current_type, ast.Function):
            return self.show_type(type_string + '(' + self.show_parameter(current_type.parameter) + ')', current_type.return_type)
        elif isinstance(current_type, ast.ArrayDeclaration):
            return self.show_type(type_string + '[]', current_type.modified_type)
        elif isinstance(current_type, ast.Pointer):
            if isinstance(current_type.modified_type, (ast.ArrayDeclaration, ast.Function)):
                return self.show_type('(*' + type_string + ')', current_type.modified_type)
            return self.show_type('*' + type_string, current_type.modified_type)
        else:
            raise Exception('unexpected type node: %s' % str(current_type))

    def show_declaration_list(self, basic_type, identifier_modifier_list):
        result = ''
        for identifier, modifier in identifier_modifier_list:
            if result != '':
                result += ', '
            result += self.show_type(identifier.name if identifier.name is not None else '', modifier)
        return basic_type.type_name + ' ' + result

    def show_declaration(self, basic_type, identifier, modifier):
        return basic_type.type_name + ' ' + self.show_type(identifier.name if identifier.name is not None else '', modifier)

    def show_parameter(self, parameter_list):
        result = ''
        return ', '.join([self.show_declaration(p[0], p[1], p[2]) for p in parameter_list])
