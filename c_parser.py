# -*- encoding: utf-8 -*-
"""
 Recursive descent parser for C.

storage_class_specifier ::= AUTO
                        | REGISTER
                        | STATIC
                        | EXTERN
                        | TYPEDEF

expression_statement ::= expression_opt SEMI

selection_statement ::= IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement
                    | SWITCH LPAREN expression RPAREN statement

constant ::= INT_CONST_DEC
         | INT_CONST_OCT
         | INT_CONST_HEX
         | FLOAT_CONST
         | HEX_FLOAT_CONST
         | CHAR_CONST
         | WCHAR_CONST

unary_expression ::= postfix_expression
                 | PLUSPLUS unary_expression
                 | MINUSMINUS unary_expression
                 | unary_operator cast_expression
                 | SIZEOF unary_expression
                 | SIZEOF LPAREN type_name RPAREN

conditional_expression ::= binary_expression
                       | binary_expression CONDOP expression COLON conditional_expression

abstract_declarator ::= pointer
                    | pointer direct_abstract_declarator
                    | direct_abstract_declarator

struct_or_union_specifier ::= struct_or_union ID
                          | struct_or_union TYPEID
                          | struct_or_union brace_open struct_declaration_list brace_close
                          | struct_or_union ID brace_open struct_declaration_list brace_close
                          | struct_or_union TYPEID brace_open struct_declaration_list brace_close

initializer ::= assignment_expression
            | brace_open initializer_list brace_close
            | brace_open initializer_list COMMA brace_close

init_declarator_list ::= init_declarator
                     | init_declarator_list COMMA init_declarator
                     | EQUALS initializer
                     | abstract_declarator

translation_unit_or_empty ::= translation_unit
                          | empty

struct_declaration_list ::= struct_declaration
                        | struct_declaration_list struct_declaration

unified_wstring_literal ::= WSTRING_LITERAL
                        | unified_wstring_literal WSTRING_LITERAL

brace_open ::= LBRACE

enumerator ::= ID
           | ID EQUALS constant_expression

pp_directive ::= PPHASH

function_specifier ::= INLINE

pointer ::= TIMES type_qualifier_list_opt
        | TIMES type_qualifier_list_opt pointer

brace_close ::= RBRACE

external_declaration ::= function_definition
                     | declaration
                     | pp_directive
                     | SEMI

type_specifier ::= VOID
               | _BOOL
               | CHAR
               | SHORT
               | INT
               | LONG
               | FLOAT
               | DOUBLE
               | _COMPLEX
               | SIGNED
               | UNSIGNED
               | typedef_name
               | enum_specifier
               | struct_or_union_specifier

compound_statement ::= brace_open block_item_list_opt brace_close

iteration_statement ::= WHILE LPAREN expression RPAREN statement
                    | DO statement WHILE LPAREN expression RPAREN SEMI
                    | FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
                    | FOR LPAREN declaration expression_opt SEMI expression_opt RPAREN statement

type_name ::= specifier_qualifier_list abstract_declarator_opt

unified_string_literal ::= STRING_LITERAL
                       | unified_string_literal STRING_LITERAL

postfix_expression ::= primary_expression
                   | postfix_expression LBRACKET expression RBRACKET
                   | postfix_expression LPAREN argument_expression_list RPAREN
                   | postfix_expression LPAREN RPAREN
                   | postfix_expression PERIOD ID
                   | postfix_expression PERIOD TYPEID
                   | postfix_expression ARROW ID
                   | postfix_expression ARROW TYPEID
                   | postfix_expression PLUSPLUS
                   | postfix_expression MINUSMINUS
                   | LPAREN type_name RPAREN brace_open initializer_list brace_close
                   | LPAREN type_name RPAREN brace_open initializer_list COMMA brace_close

typedef_name ::= TYPEID

statement ::= labeled_statement
          | expression_statement
          | compound_statement
          | selection_statement
          | iteration_statement
          | jump_statement

unary_operator ::= AND
               | TIMES
               | PLUS
               | MINUS
               | NOT
               | LNOT

cast_expression ::= unary_expression
                | LPAREN type_name RPAREN cast_expression

initializer_list ::= designation_opt initializer
                 | initializer_list COMMA designation_opt initializer

struct_declarator_list ::= struct_declarator
                       | struct_declarator_list COMMA struct_declarator

translation_unit ::= external_declaration
                 | translation_unit external_declaration

struct_or_union ::= STRUCT
                | UNION

type_qualifier_list ::= type_qualifier
                    | type_qualifier_list type_qualifier

struct_declaration ::= specifier_qualifier_list struct_declarator_list_opt SEMI
                   | specifier_qualifier_list abstract_declarator SEMI

assignment_expression ::= conditional_expression
                      | unary_expression assignment_operator assignment_expression

parameter_type_list ::= parameter_list
                    | parameter_list COMMA ELLIPSIS

parameter_declaration ::= declaration_specifiers declarator
                      | declaration_specifiers abstract_declarator_opt

direct_declarator ::= ID
                  | LPAREN declarator RPAREN
                  | direct_declarator LBRACKET type_qualifier_list_opt assignment_expression_opt RBRACKET
                  | direct_declarator LBRACKET STATIC type_qualifier_list_opt assignment_expression RBRACKET
                  | direct_declarator LBRACKET type_qualifier_list STATIC assignment_expression RBRACKET
                  | direct_declarator LBRACKET type_qualifier_list_opt TIMES RBRACKET
                  | direct_declarator LPAREN parameter_type_list RPAREN
                  | direct_declarator LPAREN identifier_list_opt RPAREN

declarator ::= direct_declarator
           | pointer direct_declarator
           | pointer TYPEID

designator ::= LBRACKET constant_expression RBRACKET
           | PERIOD identifier

argument_expression_list ::= assignment_expression
                         | argument_expression_list COMMA assignment_expression

constant_expression ::= conditional_expression

primary_expression ::= identifier
                   | constant
                   | unified_string_literal
                   | unified_wstring_literal
                   | LPAREN expression RPAREN

declaration_specifiers ::= type_qualifier declaration_specifiers_opt
                       | type_specifier declaration_specifiers_opt
                       | storage_class_specifier declaration_specifiers_opt
                       | function_specifier declaration_specifiers_opt

declaration ::= decl_body SEMI

identifier_list ::= identifier
                | identifier_list COMMA identifier

block_item_list ::= block_item
                | block_item_list block_item

binary_expression ::= cast_expression
                  | binary_expression TIMES binary_expression
                  | binary_expression DIVIDE binary_expression
                  | binary_expression MOD binary_expression
                  | binary_expression PLUS binary_expression
                  | binary_expression MINUS binary_expression
                  | binary_expression RSHIFT binary_expression
                  | binary_expression LSHIFT binary_expression
                  | binary_expression LT binary_expression
                  | binary_expression LE binary_expression
                  | binary_expression GE binary_expression
                  | binary_expression GT binary_expression
                  | binary_expression EQ binary_expression
                  | binary_expression NE binary_expression
                  | binary_expression AND binary_expression
                  | binary_expression OR binary_expression
                  | binary_expression XOR binary_expression
                  | binary_expression LAND binary_expression
                  | binary_expression LOR binary_expression

jump_statement ::= GOTO ID SEMI
               | BREAK SEMI
               | CONTINUE SEMI
               | RETURN expression SEMI
               | RETURN SEMI

struct_declarator ::= declarator
                  | declarator COLON constant_expression
                  | COLON constant_expression

function_definition ::= declarator declaration_list_opt compound_statement
                    | declaration_specifiers declarator declaration_list_opt compound_statement

designation ::= designator_list EQUALS

parameter_list ::= parameter_declaration
               | parameter_list COMMA parameter_declaration

enum_specifier ::= ENUM ID
               | ENUM TYPEID
               | ENUM brace_open enumerator_list brace_close
               | ENUM ID brace_open enumerator_list brace_close
               | ENUM TYPEID brace_open enumerator_list brace_close

decl_body ::= declaration_specifiers init_declarator_list_opt

type_qualifier ::= CONST
               | RESTRICT
               | VOLATILE

enumerator_list ::= enumerator
                | enumerator_list COMMA
                | enumerator_list COMMA enumerator

labeled_statement ::= ID COLON statement
                  | CASE constant_expression COLON statement
                  | DEFAULT COLON statement

declaration_list ::= declaration
                 | declaration_list declaration

specifier_qualifier_list ::= type_qualifier specifier_qualifier_list_opt
                         | type_specifier specifier_qualifier_list_opt

block_item ::= declaration
           | statement

empty ::=

assignment_operator ::= EQUALS
                    | XOREQUAL
                    | TIMESEQUAL
                    | DIVEQUAL
                    | MODEQUAL
                    | PLUSEQUAL
                    | MINUSEQUAL
                    | LSHIFTEQUAL
                    | RSHIFTEQUAL
                    | ANDEQUAL
                    | OREQUAL

init_declarator ::= declarator
                | declarator EQUALS initializer

direct_abstract_declarator ::= LPAREN abstract_declarator RPAREN
                           | direct_abstract_declarator LBRACKET assignment_expression_opt RBRACKET
                           | LBRACKET assignment_expression_opt RBRACKET
                           | direct_abstract_declarator LBRACKET TIMES RBRACKET
                           | LBRACKET TIMES RBRACKET
                           | direct_abstract_declarator LPAREN parameter_type_list_opt RPAREN
                           | LPAREN parameter_type_list_opt RPAREN

designator_list ::= designator
                | designator_list designator

identifier ::= ID

expression ::= assignment_expression
           | expression COMMA assignment_expression


"""
__author__ = 'Christian Mönch'


import sys
from c_lexer import *
import ast


class CParserError(object):
    pass


class CParser(object):
    def __init__(self, token_stream):
        self.token_stream = token_stream
        self.current_token = None
        self.error = None
        self.name = ''
        self.first_token = {
            'preprocessor_directive': [TokenEnum.PREPROCESSOR_DIRECTIVE],
            'declaration': [TokenEnum.INT, TokenEnum.LONG, TokenEnum.CHAR, TokenEnum.SHORT],
        }

    def show_message(self, message):
        sys.stderr.write(message + '\n')

    def error(self, number, message, location=None):
        self.show_message('warning: [w-%d]: %s' % (number, message))

    def warning(self, number, message, location=None):
        self.show_message('warning: [w-%d]: %s' % (number, message))

    def get_next_token(self):
        self.current_token = self.token_stream.get_next_token()
        return self.current_token

    def match_token(self, expected_token_type):
        if self.current_token is not None:
            if expected_token_type is None:
                self.error = 'expected end of file, got token %s' % str(self.current_token)
                return False
            else:
                if self.current_token.type == expected_token_type:
                    self.get_next_token()
                    return True
                self.error = 'expected token %s, got: %s' % (str(expected_token_type), str(self.current_token.type))
                return False
        else:
            if expected_token_type is None:
                return True
            else:
                self.error = 'expected token %s, got end of file' % str(expected_token_type)
                return False

    def token_equals(self, compared_type):
        if self.current_token is None:
            return compared_type is None
        else:
            return self.current_token.type == compared_type

    def parse(self):
        self.get_next_token()
        self.translation_unit()

    def translation_unit(self):
        while self.current_token is not None:
            self.external_declaration()

    def external_declaration(self):
        if self.current_token in self.first_token['preprocessor_directive']:
            return self.preprocessor_directive()
        elif self.token_equals(TokenEnum.COMMENT):
            self.get_next_token()
            return None
        elif self.token_equals(TokenEnum.SEMICOLON):
            self.get_next_token()
            return None
        else:
            return self.declaration_or_definition()

    def declaration_or_definition(self):
        pass

    def function_definition(self):
        pass

    def create_modifier(self, list):
        pass

    def build_declaration_ast(self, modifier_spec):
        """
        Converts a list into an AST
        """
        if not modifier_spec:
            return None
        if len(modifier_spec) == 1:
            return modifier_spec[0]
        for index, modifier in enumerate(modifier_spec[:-1]):
            if isinstance(modifier, ast.Pointer):
                modifier.set_modified_type(modifier_spec[index + 1])
            elif isinstance(modifier, ast.ArrayDeclaration):
                modifier.set_modified_type(modifier_spec[index + 1])
            elif isinstance(modifier, ast.Function):
                modifier.set_return_type(modifier_spec[index + 1])
            else:
                raise Exception('unknown modifier %s' % repr(modifier))
        return modifier_spec[0]

    def declaration(self):
        """
        declaration := type_specifier pointer_specifier
        """
        type_spec = self.type_specifier()
        modifier_spec = self.pointer_specifier()
        return type_spec, modifier_spec[0], self.build_declaration_ast(modifier_spec[1:])

    def declaration_list(self):
        """
        declaration_list := type_specifier pointer_specifier { ',' pointer_specifier }
        """
        type_spec = self.type_specifier()
        variable_spec_list = []
        while True:
            modifier_spec = self.pointer_specifier()
            variable_spec_list.append((modifier_spec[0], self.build_declaration_ast(modifier_spec[1:])))
            if self.token_equals(TokenEnum.COMMA):
                self.get_next_token()
                continue
            break
        return type_spec, variable_spec_list

    def type_specifier(self):
        """
        type_specifier := TOKEN_
        """
        result = ''
        while self.current_token.type in (
                TokenEnum.EXTERNAL, TokenEnum.STATIC,
                TokenEnum.CONST,
                TokenEnum.SIGNED, TokenEnum.UNSIGNED,
                TokenEnum.CHAR, TokenEnum.SHORT, TokenEnum.INT, TokenEnum.LONG):
            result += self.current_token.value
            self.get_next_token()
        return ast.BasicType(result, None)

    def pointer_specifier(self):
        if self.token_equals(TokenEnum.TIMES):
            self.get_next_token()
            result = self.pointer_specifier()
            result.append(ast.Pointer(None, None))
        else:
            result = self.variable_specifier()
        return result

    def variable_specifier(self):
        result = self.name_specifier()
        if self.token_equals(TokenEnum.LEFT_PARENTHESIS):
            parameter = self.parameter_list()
            result.append(ast.Function(None, parameter, None, None))
        if self.token_equals(TokenEnum.LEFT_BRACKET):
            while self.token_equals(TokenEnum.LEFT_BRACKET):
                self.match_token(TokenEnum.LEFT_BRACKET)
                result.append(ast.ArrayDeclaration(None, None, None))
                self.match_token(TokenEnum.RIGHT_BRACKET)
        return result

    def name_specifier(self):
        if self.token_equals(TokenEnum.LEFT_PARENTHESIS):
            self.get_next_token()
            result = self.pointer_specifier()
            self.match_token(TokenEnum.RIGHT_PARENTHESIS)
        elif self.token_equals(TokenEnum.ID):
            result = [ast.Identifier(self.current_token.value)]
            self.get_next_token()
        else:
            result = [ast.Identifier(None)]
        return result

    def parameter_list(self):
        """
        parameter_list = '(' [ declaration { ',' declaration } ] ')'
        """
        result = []
        self.match_token(TokenEnum.LEFT_PARENTHESIS)
        if self.token_equals(TokenEnum.RIGHT_PARENTHESIS):
            self.match_token(TokenEnum.RIGHT_PARENTHESIS)
            return result
        result.append(self.declaration())
        while self.token_equals(TokenEnum.COMMA):
            self.get_next_token()
            result.append(self.declaration())
        self.match_token(TokenEnum.RIGHT_PARENTHESIS)
        return result

    def preprocessor_directive(self):
        pass

    def comment(self):
        pass
