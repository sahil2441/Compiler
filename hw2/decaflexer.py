''' PLY/lex scanner specification file '''
import sys
#sys.path.insert(0,"../..")
import ply.lex as lex

ROOT_FOLDER = 'F:\\MastersStonyBrook\\SemesterCourses\\Semester2\\CSE504_Compilers\\jsundar-sahjain\\hw2\\'

reserved = {
    'boolean' : 'BOOLEAN', 
    'break' : 'BREAK', 
    'continue' : 'CONTINUE',
    'class' : 'CLASS',
    'do' : 'DO', 
    'else' : 'ELSE',
    'extends' : 'EXTENDS', 
    'false' : 'FALSE', 
    'float' : 'FLOAT', 
    'for' : 'FOR', 
    'if' : 'IF',
    'int' : 'INT',
    'new' : 'NEW',
    'null' : 'NULL',
    'private' : 'PRIVATE',
    'public' : 'PUBLIC',
    'return' : 'RETURN',
    'static' : 'STATIC',
    'super' : 'SUPER',
    'this' : 'THIS',
    'true' : 'TRUE',
    'void' : 'VOID',
    'while' : 'WHILE'} 

tokens = list(reserved.values()) + \
         ['IDENTIFIER', 'INTEGERCONSTANT','FLOATCONSTANTFIRST','FLOATCONSTANTSECOND','STRINGCONSTANT', 'COMMENT',
          'GEQ', 'LEQ', 'GT', 'LT', 'EQUALS', 'NOTEQUALS', 'OR', 'AND', 'NOT', 'PLUS', 'MINUS', 'MULT', 'DIV', 'SEMICOLON','COLON',
          'COMMA', 'ASSIGN','SPACE','LPAREN','RPAREN','LCURLY','RCURLY','DOT', 'LSQUARE','RSQUARE', 'PLUSPLUS', 'MINUSMINUS']

t_INTEGERCONSTANT = r'(\+|-)?[0-9]+$'
t_FLOATCONSTANTFIRST=r'(\-\+)?([0-9]+[.][0-9]+)'
t_FLOATCONSTANTSECOND = r'(\+|\-)?[0-9]+(\.[0-9]+|((.)?[0-9]+)?(e|E)(\-|\+)?[0-9]+)$'
t_ignore_COMMENT = r'(//.*|\/\*.*\*\/)'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

"""
String constants begin and end with a double quote ("). If the string itself contains a double
quote, it is \escaped" with a backslash (\) as in the example string: "\"What?\" she exclaimed.".
Escape sequences, such as \n and \t are used to place special characters such as newlines and tabs
in a string. If the string contains a backslash, that is escaped too (e.g., "The computer simply
responded with \"A:\\>\""). Strings must be contained within a single line.
"""

#TODO
t_STRINGCONSTANT = r'\".*\"$'

t_GEQ = r'>='
t_LEQ = r'<='
t_GT = r'>'
t_LT = r'<'
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_OR = r'\|\|'
t_AND  = r'&&'
t_NOT = r'!'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_ASSIGN = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCURLY  = r'\{'
t_RCURLY  = r'\}'
t_DOT= r'\.'
t_LSQUARE=R'\['
t_RSQUARE=R'\]'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'


def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

def feedInput():
    file=open(ROOT_FOLDER+'test_case_1.txt')
    data = file.read()
    file.close()
    # Give the lexer some input
    lexer.input(data)


def print_token():
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)

if __name__ == '__main__':
    feedInput()
    lex.lex()
    # lex.runmain()
    print_token()
  