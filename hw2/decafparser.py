# -*- coding: utf-8 -*-
''' PLY/yacc parser specification file '''
import traceback

from pip.utils import logging

from ply import *
import decaflexer

tokens = decaflexer.tokens
errors_list=""

precedence = (
    ('left', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOTEQUALS'),    
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'NOT'),
    ('right', 'UMINUS'),
    ('right', 'UPLUS'),
    ('right', 'ELSE'),
)

def p_classdecl(p):
    '''classdecl :  CLASS IDENTIFIER LCURLY RCURLY
                |   CLASS IDENTIFIER LCURLY field_decl class_body_decl RCURLY
                |   CLASS IDENTIFIER LCURLY method_decl class_body_decl RCURLY
                |   CLASS IDENTIFIER LCURLY constructor_decl class_body_decl RCURLY
                |   CLASS IDENTIFIER EXTENDS IDENTIFIER LCURLY field_decl class_body_decl RCURLY
                |   CLASS IDENTIFIER EXTENDS IDENTIFIER LCURLY constructor_decl class_body_decl RCURLY
                |   CLASS IDENTIFIER EXTENDS IDENTIFIER LCURLY method_decl class_body_decl RCURLY'''

def p_class_body_decl(p):
   '''class_body_decl : field_decl class_body_decl
                    | method_decl class_body_decl
                    | constructor_decl class_body_decl
                    | empty'''


def p_field_decl(p):
    'field_decl : modifier var_decl'

def p_modifier(p):
    ''' modifier : PUBLIC
                | PRIVATE
                | STATIC
                | PUBLIC STATIC
                | PRIVATE STATIC
                | empty'''

def p_var_decl(p):
    'var_decl : type variables SEMICOLON'

def p_type(p):
    '''type : INT
            | FLOAT
            | BOOLEAN
            | IDENTIFIER '''

def p_variables(p):
    '''variables : IDENTIFIER brackets
                |  variables COMMA IDENTIFIER brackets'''

def p_brackets(p):
    '''brackets : LSQUARE RSQUARE brackets
                | empty'''

def p_method_decl(p):
    '''method_decl :  modifier type IDENTIFIER LPAREN RPAREN block
                    | modifier VOID IDENTIFIER LPAREN RPAREN block
                    | modifier VOID IDENTIFIER LPAREN formals RPAREN block
                    | modifier type IDENTIFIER LPAREN formals RPAREN block '''

def p_constructor_decl(p):
    '''constructor_decl : modifier IDENTIFIER LPAREN RPAREN block
                        | modifier IDENTIFIER LPAREN formals RPAREN block'''

def p_formals(p):
    '''formals : type variables
                | type variables COMMA formals'''
#TODO
def p_block(p):
    '''block : LCURLY empty RCURLY
              | LCURLY stmthelper RCURLY'''

def p_stmthelper(p):
    '''stmthelper : stmt
                  | stmthelper stmt'''

def p_stmt(p):
    '''stmt : IF LPAREN expr RPAREN stmt ELSE stmt
              | IF LPAREN expr RPAREN stmt
              | WHILE LPAREN expr RPAREN stmt
              | FOR LPAREN SEMICOLON SEMICOLON RPAREN stmt
              | FOR LPAREN stmt_expr SEMICOLON SEMICOLON RPAREN stmt
              | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON RPAREN stmt
              | FOR LPAREN stmt_expr SEMICOLON SEMICOLON stmt_expr RPAREN stmt
              | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
              | FOR LPAREN SEMICOLON expr SEMICOLON RPAREN stmt
              | FOR LPAREN SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
              | FOR LPAREN SEMICOLON SEMICOLON stmt_expr RPAREN stmt
              | block
              | var_decl
              | stmt_expr SEMICOLON
              | RETURN expr SEMICOLON
              | RETURN SEMICOLON
              | BREAK SEMICOLON
              | CONTINUE SEMICOLON
              | SEMICOLON'''

def p_expr(p):
    '''expr : primary
            | assign
            | new_array
            | expr OR expr
            | expr AND expr
            | expr EQUALS expr
            | expr NOTEQUALS expr
            | expr LT expr
            | expr GT expr
            | expr LEQ expr
            | expr GEQ expr
            | expr PLUS expr
            | expr MINUS expr
            | expr MULT expr
            | expr DIV expr
            | NOT expr'''

def p_expr_uminus(p):
    'expr : MINUS expr %prec UMINUS'
    p[0] = -p[2]

def p_expr_uplus(p):
    'expr : PLUS expr %prec UPLUS'
    p[0] = -p[2]


def p_assign(p):
    '''assign : lhs ASSIGN expr
               | lhs PLUSPLUS
               | PLUSPLUS lhs
               | lhs MINUSMINUS
               | MINUSMINUS lhs'''

def p_new_array(p):
    '''new_array : NEW type expr_array_helper'''

def p_expr_array_helper(p):
    '''expr_array_helper : LSQUARE expr RSQUARE
                          | LSQUARE expr RSQUARE expr_array_helper
                          | LSQUARE expr RSQUARE expr_array_helper2'''

def p_expr_array_helper2(p):
    '''expr_array_helper2 : LSQUARE RSQUARE
                           | LSQUARE RSQUARE expr_array_helper2'''

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''

def p_literal(p):
    ''' literal : INTEGERCONSTANT
                | FLOATCONSTANT
                | STRINGCONSTANT
                | NULL
                | TRUE
                | FALSE
    '''

def p_primary(p):
    '''
    primary : literal
            | THIS
            | SUPER
            | LPAREN expr RPAREN
            | NEW IDENTIFIER LPAREN RPAREN
            | NEW IDENTIFIER LPAREN arguments RPAREN
            | lhs
            | method_invocation
    '''

def p_arguments(p):
    '''
    arguments : expr
              | arguments COMMA expr
    '''

def p_lhs(p):
    '''
    lhs : field_access
        | array_access
    '''

def p_field_access(p):
    '''
    field_access : primary DOT IDENTIFIER
                | IDENTIFIER
    '''

def p_array_access(p):
    'array_access : primary LSQUARE expr RSQUARE'

def p_method_invocation(p):
    '''
    method_invocation : field_access LPAREN RPAREN
                        | field_access LPAREN arguments RPAREN
    '''

def p_empty(t):
    'empty : '
    pass

def p_error(p):
    '''
    An alternative error recovery scheme is to enter a panic mode recovery in which tokens are discarded to a point
    where the parser might be able to recover in some sensible manner.
    Panic mode recovery is implemented entirely in the p_error() function. For example, this function starts discarding
    tokens until it reaches a closing '}'. Then, it restarts the parser in its initial state.
    '''
    # logging.exception("Something awful happened!")

    parser=yacc.yacc()

    if p is not None:
        print 'Error due to token :'
        print p
        error=('Line number: ')
        error+=str(p.lineno)
        error+=(', Lex position: ')
        error+=str(p.lexpos)
        print error
        parser.errok()
    else:
        print("Unexpected end of input")

def parse(data):
    '''
    As an optional feature, yacc.py can automatically track line numbers and positions for all of the grammar symbols
    as well. However, this extra tracking requires extra processing and can significantly slow down parsing.
    Therefore, it must be enabled by passing the tracking=True option to yacc.parse().
    '''
    yacc.yacc();
    # yacc.parse(data)
    yacc.parse(data)

if __name__ == '__main__':
    file=open('test_case_1.txt')
    data = file.read()
    #data = 'class temp { int x; }'
    parse(data)
