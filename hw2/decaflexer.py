''' PLY/lex scanner specification file '''
import sys
sys.path.insert(0,"../..")

import ply.lex as lex

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
         ['IDENTIFIER', 'INTEGERCONSTANT','FLOATCONSTANT','STRINGCONSTANT', 'COMMENT',
          'GEQ', 'LEQ', 'GT', 'LT', 'EQUALS', 'PLUS', 'MINUS', 'MULT', 'DIV', 'SEMICOLON','COLON',
          'COMMA', 'ASSIGN','SPACE']

t_INTEGERCONSTANT = r'(\+|-)?[0-9]+$'
    
t_FLOATCONSTANT = r'[0-9]+(\.[0-9]+|((.)?[0-9]+)?(e|E)(\-|\+)?[0-9]+)$'
    
t_ignore_COMMENT = r'(//.*|\/\*.*\*\/)'
    
t_STRINGCONSTANT = r'\"\"$' #TODO

t_GEQ = r'>='
t_LEQ = r'<='
t_GT = r'>'
t_LT = r'<'
t_EQUALS = r'=='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_ASSIGN = r'='


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

if __name__ == '__main__':
     lex.runmain()

# Test it out
data = '''class nrfib{
public static void main() {
int n, i, fn, fn_prev;
n = In.scan_int();
fn = 1;
fn_1 = 0;
for(i=1; i<n; i=i+1) {
fn = fn_prev + fn;
fn_prev = fn - fn_prev;
}
Out.print("Fib = ");
Out.print(fn);
Out.print("\n");
}
}'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
    
  