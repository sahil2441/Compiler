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
    '''variables : variable
            | variable COMMA variables '''

def p_variable(p):
    '''variable : IDENTIFIER
                | IDENTIFIER variable_array '''

def p_variable_array(p):
    '''variable_array : LSQUARE RSQUARE
                    |  LSQUARE RSQUARE variable_array '''

def p_method_decl(p):
    '''method_decl :  modifier type IDENTIFIER LPAREN RPAREN block
                    | modifier type IDENTIFIER LPAREN formals RPAREN block
                    | modifier VOID IDENTIFIER LPAREN RPAREN block
                    | modifier VOID IDENTIFIER LPAREN formals RPAREN block'''

def p_constructor_decl(p):
    '''constructor_decl : modifier IDENTIFIER LPAREN RPAREN block
                        | modifier IDENTIFIER LPAREN formals RPAREN block'''

def p_formals(p):
    '''formals : formal_param
               | formal_param COMMA formal_param'''

def p_formal_param(p):
    '''formal_param : type variable'''

def p_block(p):
    '''block : LCURLY stmthelper RCURLY
              | LCURLY RCURLY'''

def p_stmthelper(p):
    '''stmthelper : stmt
                    | stmt stmthelper'''

def p_stmt(p):
    '''stmt : IF LPAREN expr RPAREN stmt
             | IF LPAREN expr RPAREN stmt ELSE stmt
             | WHILE LPAREN expr RPAREN stmt
             | FOR LPAREN SEMICOLON SEMICOLON RPAREN stmt
             | FOR LPAREN stmt_expr SEMICOLON SEMICOLON RPAREN stmt
             | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON RPAREN stmt
             | FOR LPAREN stmt_expr SEMICOLON SEMICOLON stmt_expr RPAREN stmt
             | FOR LPAREN stmt_expr SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
             | FOR LPAREN SEMICOLON expr SEMICOLON RPAREN stmt
             | FOR LPAREN SEMICOLON expr SEMICOLON stmt_expr RPAREN stmt
             | FOR LPAREN SEMICOLON SEMICOLON stmt_expr RPAREN stmt
             | RETURN SEMICOLON
             | RETURN expr SEMICOLON
             | stmt_expr SEMICOLON
             | BREAK SEMICOLON
             | CONTINUE SEMICOLON
             | block
             | var_decl
             | SEMICOLON'''

def p_expr(p):
    '''expr : primary
            | assign
            | new_array
            | expr PLUS expr
            | expr MINUS expr
            | expr MULT expr
            | expr DIV expr
            | expr OR expr
            | expr AND expr
            | expr EQUALS expr
            | expr NOTEQUALS expr
            | expr LT expr
            | expr GT expr
            | expr LEQ expr
            | expr GEQ expr
            | PLUS expr
            | MINUS expr
            | NOT expr'''

def p_assign(p):
    '''assign : lhs ASSIGN expr
               | lhs PLUSPLUS
               | PLUSPLUS lhs
               | lhs MINUSMINUS
               | MINUSMINUS lhs'''

def p_new_array(p):
    '''new_array : NEW type expr_array_helper1 expr_array_helper2'''

def p_expr_array_helper1(p):
    '''expr_array_helper1 : LSQUARE expr RSQUARE
                          | LSQUARE expr RSQUARE expr_array_helper1'''

def p_expr_array_helper2(p):
    '''expr_array_helper2 : empty
                           | LSQUARE RSQUARE expr_array_helper2'''

def p_stmt_expr(p):
    '''stmt_expr : empty'''

def p_literal(p):
    ''' literal : INTEGERCONSTANT
                | FLOATCONSTANT
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
            | NEW IDENTIFIER LPAREN arguments RPAREN
            | lhs
            | method_invocation
    '''

def p_arguments(p):
    '''
    arguments : expr
              | COMMA arguments
    '''

def p_lhs(p):
    '''
    lhs : field_access
        | array_access
    '''

def p_method_invocation(p):
    '''
    method_invocation : field_access LPAREN RPAREN
                        | field_access LPAREN expr RPAREN
    '''

def p_field_access(p):
    '''
    field_access : primary DOT IDENTIFIER
                | IDENTIFIER
    '''

def p_array_access(p):
    'array_access : primary LPAREN expr RPAREN'

def p_empty(t):
    'empty : '
    pass

def p_error(t):
    print("Whoa. Error!")

# ROOT_FOLDER = 'F:\\MastersStonyBrook\\SemesterCourses\\Semester2\\CSE504_Compilers\\jsundar-sahjain\\hw2\\'

if __name__ == '__main__':
    file=open('test_case_1.txt')
    data = file.read()
    #data = 'class temp { int x; }'

    parser = yacc.yacc()
    p = parser.parse(data)