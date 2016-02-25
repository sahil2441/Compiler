# -*- coding: utf-8 -*-
''' PLY/yacc parser specification file '''
from ply import *
import decaflexer

tokens = decaflexer.tokens

precedence = (
    ('left', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOTEQUALS'),    
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', 'PLUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'NOT'),
)

# start = 'program'
#
# def p_program(p):
#     'classdecl*'

def p_classdecl(p):
    '''classdecl : CLASS IDENTIFIER LCURLY class_body_decl_helper RCURLY
                  | CLASS IDENTIFIER EXTENDS IDENTIFIER LCURLY class_body_decl_helper RCURLY'''

def p_class_body_decl_helper(p):
    ''' class_body_decl_helper : class_body_decl
                                | class_body_decl class_body_decl_helper '''
    
def p_class_body_decl(p):
   '''class_body_decl : field_decl
                       | method_decl
                       | constructor_decl'''
    
def p_field_decl(p):
    'field_decl : modifier var_decl'

def p_modifier(p):
    ''' modifier : PUBLIC
                | PRIVATE
                | STATIC
                | PUBLIC STATIC
                | PRIVATE STATIC '''

def p_var_decl(p):
    'var_decl : type variables SEMICOLON'

def p_type(p):
    '''type : INT
        | FLOAT
        | BOOLEAN
        | IDENTIFIER '''

def p_variables(p):
    '''variables : variable
            | variable COMMA variables '''

def p_variable(p):
    '''variable : IDENTIFIER
                | IDENTIFIER variable_array '''

def p_variable_array(p):
    '''variable_array : LSQUARE RSQUARE
                    |  LSQUARE RSQUARE variable_array '''

def p_error(t):
    print("Whoa. Error!")

ROOT_FOLDER = 'F:\\MastersStonyBrook\\SemesterCourses\\Semester2\\CSE504_Compilers\\jsundar-sahjain\\hw2\\'

if __name__ == '__main__':
    #file=open(ROOT_FOLDER+'test_case_1.txt')
    #data = file.read()
    data = 'class temp { int x; }'
    parser = yacc.yacc()
    p = parser.parse(data)