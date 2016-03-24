import ply.yacc as yacc
import decaflexer
from decaflexer import tokens
#from decaflexer import errorflag
from decaflexer import lex
from AST import *

import sys
import logging
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', 'LEQ', 'GEQ', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
    ('right', 'ELSE'),
    ('right', 'RPAREN'),
)


def init():
    decaflexer.errorflag = False

classes = list()
classesMap = dict()
currentClass = "";
fieldMap = dict()
counter = 0
constructorMap = dict()
constructorCounter = 0
methodMap = dict()
methodCounter = 0
scopeList = []
debug = False;
def push_scope(f):
    scopeList.append(f);

def pop_scope():
    scopeList.pop()

def fetchScope():
    return scopeList[-1]

def __alreadyExistsInScope(var):
    '''
    This method checks if the variable is valid in the current scope.
    :param var:
    :return:
    '''
    scope = fetchScope();
    if (isinstance(scope, Method) or isinstance(scope, Constructor)):
        for param in scope.parameters:
            if (param.name == var):
                return True;
        for param in scope.variables:
            if (param.name == var):
                return True;
    return False;

def _scopedVariable(pstr):
    '''
    This method creates the alias for the variable name based on the variable ID in the scope
    :param pstr:
    :return:
    '''
    varstr = pstr
    if 'Array-Access' in pstr:
       return varstr;
    scope = fetchScope();
    for param in scope.parameters:
        if param.name == pstr:
            varstr = "Variable("+ str(param.id)+")"
            return varstr;
    for variable in scope.variables:
        if variable.name == pstr:
            varstr = "Variable("+ str(variable.id)+")"
            return varstr;
    if (not 'Field-access' in varstr):
        varstr = 'Field-access(This, '+varstr+')'
    return varstr

### DECAF Grammar

# Top-level
def p_pgm(p):
    'pgm : class_decl_list'
    if (debug): print 's0'
    pass

def p_class_decl_list_nonempty(p):
    'class_decl_list : class_decl class_decl_list'
    if (debug): print 's1'
    pass
def p_class_decl_list_empty(p):
    'class_decl_list : '
    if (debug): print 's2'
    pass

def p_class_decl(p):
    'class_decl : CLASS ID extends LBRACE newscope class_body_decl_list RBRACE'
    if (debug): print 's3.1'
    pop_scope()
    pass

def p_newscope(p):
    'newscope : '
    if (debug): print 's3.2'
    if (p[-2]):
        newclass = DecafClass(p[-3], p[-2])
    else:
        newclass = DecafClass(p[-3])
    if (classesMap.has_key(newclass.name)):
        print "Error! Class "+str(newclass.name)+" is already defined!"
        decaflexer.errorflag = True
    classesMap[newclass.name] = newclass;
    classes.append(newclass)
    push_scope(newclass)

def p_class_decl_error(p):
    'class_decl : CLASS ID extends LBRACE error RBRACE'
    # error in class declaration; skip to next class decl.
    pass

def p_extends_id(p):
    'extends : EXTENDS ID '
    p[0] = p[2]
    if (debug): print 's4'
    pass
def p_extends_empty(p):
    ' extends : '
    if (debug): print 's5'
    pass

def p_class_body_decl_list_plus(p):
    'class_body_decl_list : class_body_decl_list class_body_decl'
    p[0] = p[1]
    if (debug): print 's6'
    pass
def p_class_body_decl_list_single(p):
    'class_body_decl_list : class_body_decl'
    p[0] = p[1]
    if (debug): print 's7'
    pass

def p_class_body_decl_field(p):
    'class_body_decl : field_decl'
    p[0] = p[1]
    if (debug): print 's8'
    pass
def p_class_body_decl_method(p):
    'class_body_decl : method_decl'
    p[0] = p[1]
    if (debug): print 's9'
    pass
def p_class_body_decl_constructor(p):
    'class_body_decl : constructor_decl'
    p[0] = p[1]
    if (debug): print 's10'
    pass


# Field/Method/Constructor Declarations

def p_field_decl(p):
    'field_decl : mod var_decl'
    visibility =  p[1][0]
    modifier = p[1][1]
    scope = fetchScope()
    type=p[2][0]
    if (classesMap.has_key(type)):
        type = 'user('+type+')'
    variables = p[2][1].split(",")
    for variable in variables:
        localtype = type
        varcomponents = variable.split("(")
        var = varcomponents[-1]
        if (len(varcomponents) > 0):
            varcomponents = varcomponents[0:-1]
            for comp in varcomponents:
                localtype = comp+"(" + localtype + ")"
        global counter
        counter = counter + 1
        fieldMap[counter] = Field(var, counter, scope.name,type=localtype)
        if (isinstance(scope, DecafClass)):
            for field in  classesMap[scope.name].fieldList:
                if field.name == var:
                    print 'Multiple declaration of same field variable "' + var + '" found for class : ' + scope.name
                    decaflexer.errorflag = True;
            if (modifier == 'static'):
                fieldMap[counter].applicability='class'
            else:
                fieldMap[counter].applicability='instance'
            if visibility:
                fieldMap[counter].visibility = visibility;
            classesMap[scope.name].fieldList.append(fieldMap[counter])
    if (debug): print 's11'
    pass

def p_method_decl_void(p):
    'method_decl : mod VOID ID LPAREN methodscope param_list_opt RPAREN block'
    scope = fetchScope()
    scope.body = list()
    body = p[8]
    if body:
        for content in body:
            if (not content is None):
                scope.body.append(content)
    if (debug): print ('body void: ' + str(body))
    pop_scope()
    if (debug): print 's12'
    pass


def p_method_decl_nonvoid(p):
    'method_decl : mod type ID LPAREN methodscope param_list_opt RPAREN block'
    scope = fetchScope()
    scope.body = list()
    body = p[8]
    if body:
        for content in body:
            if (not content is None):
                scope.body.append(content)
    if (debug): print ('body non void: ' + str(body))
    pop_scope()
    if (debug): print 's13'
    pass

def p_methodscope(p):
    'methodscope : '
    scope = fetchScope();
    global methodCounter
    methodCounter += 1
    visibility = "private"
    applicability = "instance"
    if (p[-4][0]):
        visibility=str(p[-4][0])
    if (p[-4][1]):
        applicability = "class"
    returnType = p[-3]
    methodName = p[-2]
    methodMap[methodCounter] = Method(methodCounter, name=methodName, containingClass=scope.name, visibility=visibility, applicability=applicability, returnType=returnType)
    classesMap[scope.name].methodList.append(methodMap[methodCounter])
    push_scope(methodMap[methodCounter])
    if (debug): print 's12.1 and s13.1'

def p_constructor_decl(p):
    'constructor_decl : mod ID LPAREN constructorscope param_list_opt RPAREN block'
    scope = fetchScope()
    # Added for body
    scope.body = list()
    body = p[7]
    if (debug): print 'constructor body  :' + str(body)
    if body:
        for content in body:
            if (not content is None):
                scope.body.append(content)
    pop_scope()
    if (debug): print 's14'
    pass

def p_constructorscope(p):
    'constructorscope : '
    scope = fetchScope();
    global constructorCounter
    constructorCounter += 1
    if (scope.name != str(p[-2])):
        print 'Error in constructor name!!!'
    visibility = "private"
    if (p[-3][0]):
        visibility=str(p[-3][0])
    constructorMap[constructorCounter] = Constructor(constructorCounter, visibility)
    classesMap[scope.name].constructorList.append(constructorMap[constructorCounter])
    push_scope(constructorMap[constructorCounter])
    if (debug): print 's14.1'
    pass


def p_mod(p):
    'mod : visibility_mod storage_mod'
    if (debug): print 's15'
    p[0] = (p[1],p[2])
    pass

def p_visibility_mod_pub(p):
    'visibility_mod : PUBLIC'
    if (debug): print 's16'
    p[0] = p[1]
    pass
def p_visibility_mod_priv(p):
    'visibility_mod : PRIVATE'
    if (debug): print 's17'
    p[0] = p[1]
    pass
def p_visibility_mod_empty(p):
    'visibility_mod : '
    if (debug): print 's18'
    pass

def p_storage_mod_static(p):
    'storage_mod : STATIC'
    p[0] = p[1]
    if (debug): print 's19'
    pass
def p_storage_mod_empty(p):
    'storage_mod : '
    if (debug): print 's20'
    pass

def p_var_decl(p):
    'var_decl : type var_list SEMICOLON'
    if (debug): print 's21'
    p[0] = (p[1], p[2])
    pass

def p_type_int(p):
    'type :  INT'
    if (debug): print 's22'
    p[0] = p[1]
    pass
def p_type_bool(p):
    'type :  BOOLEAN'
    if (debug): print 's23'
    p[0] = p[1]
    pass
def p_type_float(p):
    'type :  FLOAT'
    if (debug): print 's24'
    p[0] = p[1]
    pass
def p_type_id(p):
    'type :  ID'
    if (debug): print 's25'
    p[0] = p[1]
    pass

def p_var_list_plus(p):
    'var_list : var_list COMMA var'
    p[0] = p[1]+','+p[3]
    if (debug): print 's26'
    pass
def p_var_list_single(p):
    'var_list : var'
    p[0] = p[1]
    if (debug): print 's27'
    pass

def p_var_id(p):
    'var : ID'
    if (debug): print 's28'
    p[0] = p[1]
    pass

def p_var_array(p):
    'var : var LBRACKET RBRACKET'
    p[0] = 'array('+p[1]
    if (debug): print 's29'
    pass

def p_param_list_opt(p):
    'param_list_opt : param_list'
    p[0] = p[1]
    parameters = list()
    scope = fetchScope()
    variableCount = 0
    if (p[1]):
        for paramTuple in p[1]:
            variableCount += 1
            variable = Variable(paramTuple[1], variableCount, "formal", paramTuple[0])
            parameters.append(variable)
    scope.parameters = parameters;
    if (debug): print 's30'
    pass

def p_param_list_empty(p):
    'param_list_opt : '
    p[0] = None
    if (debug): print 's31'
    pass

def p_param_list(p):
    'param_list : param_list COMMA param'
    p[0] = p[1] + (p[3],)
    if (debug): print 's32'
    pass
def p_param_list_single(p):
    'param_list : param'
    p[0] = (p[1],)
    if (debug): print 's33'
    pass

def p_param(p):
    'param : type ID'
    p[0] = (p[1],p[2])
    if (debug): print 's34'
    pass

# Statements

def p_block(p):
    'block : LBRACE stmt_list RBRACE'
    p[0] = p[2]
    if (debug): print 's35'
    pass

def p_block_error(p):
    'block : LBRACE stmt_list error RBRACE'
    if (debug): print 's36'
    # error within a block; skip to enclosing block
    pass

def p_stmt_list_empty(p):
    'stmt_list : '
    if (debug): print 's37'
    pass
def p_stmt_list(p):
    'stmt_list : stmt_list stmt'
    if p[1] is not None:
        p[0] = p[1]+ (p[2],)
    else:
        p[0] = (p[2],)
    if (debug): print 's38'
    pass


def p_stmt_if(p):
    '''stmt : IF LPAREN expr RPAREN stmt ELSE stmt
          | IF LPAREN expr RPAREN stmt'''
    result = 'If (' + str(p[3]) + ')\n' + 'Then ('
    result += str(p[5])
    result+=')'
    try:
        result += '\nElse ('
        result += str(p[7])
        result+=')'
    except:
        pass

    p[0] = result
    if (debug): print 's39'
    pass

def p_stmt_while(p):
    'stmt : WHILE LPAREN expr RPAREN stmt'
    result = ''
    result += 'While(['

    # Condition
    if p[3] is not None:
        result += str(p[3])
    result += '], '

    # Statement
    result += str(p[5])
    result += ')'
    p[0] = result
    if (debug): print 's40'
    pass

def p_stmt_for(p):
    'stmt : FOR LPAREN stmt_expr_opt SEMICOLON expr_opt SEMICOLON stmt_expr_opt RPAREN stmt'
    result = ''
    result += 'For([\n'

    result += '['
    # stmt_expr_opt
    if p[3] is not None:
        result += str(p[3])
    result += ']\n, '
    result += '['

    # expr_opt
    if p[5] is not None:
        result += str(p[5])
    result += ']\n, '
    result += '['

    # stmt_expr_opt
    if p[7] is not None:
        result += str(p[7])
    result += ']\n, '

    # Statements
    result += str(p[9]);
    result += ']'
    p[0] = result
    if (debug): print 's41'
    pass

def p_stmt_return(p):
    'stmt : RETURN expr_opt SEMICOLON'
    p[0] = 'Return( '+ str(p[2])+' )'
    if (debug): print 's42'
    pass
def p_stmt_stmt_expr(p):
    'stmt : stmt_expr SEMICOLON'
    p[0] = 'Expr( ' + str(p[1]) + ' )'
    if (debug): print 's43'
    pass
def p_stmt_break(p):
    'stmt : BREAK SEMICOLON'
    p[0] = p[1]
    if (debug): print 's44'
    pass
def p_stmt_continue(p):
    'stmt : CONTINUE SEMICOLON'
    p[0] = p[1]
    if (debug): print 's45'
    pass
def p_stmt_block(p):
    'stmt : block'
    expansion = '[\n'
    for elem in p[1]:
        if not elem is None:
            expansion += str(elem) + '\n, '
    expansion = expansion[0:-2]
    p[0] = expansion + ']'
    if (debug): print 's46', 'p1 ',str(p[1])
    pass
def p_stmt_var_decl(p):
    'stmt : var_decl'
    type = p[1][0]
    if (classesMap.has_key(type)):
        type = 'user('+type+')'
    varlist = p[1][1].split(',')
    vList = list()
    scope = fetchScope();
    localvarcounter = len(scope.parameters) + len(scope.variables)
    for var in varlist:
        localtype = type;
        vararr = var.split("(")
        varname = vararr[-1]
        if (__alreadyExistsInScope(varname)):
            print 'Variable name "' + varname + '" already exists in the current scope!'
            decaflexer.errorflag = True;
        else:
            vararr = vararr[0:-1]
            if len(vararr) > 0:
                for arraystr in vararr:
                    localtype = arraystr + '(' + localtype + ')'
            localvarcounter += 1
            scope.variables.append(Variable(varname, localvarcounter, 'local', localtype))
    if (debug): print 's47'
    pass
def p_stmt_error(p):
    'stmt : error SEMICOLON'
    if (debug): print 's48'
    print("Invalid statement near line {}".format(p.lineno(1)))
    decaflexer.errorflag = True

# Expressions
def p_literal_int_const(p):
    'literal : INT_CONST'
    p[0] = 'Constant(Integer-constant('+str(p[1])+'))'
    if (debug): print 's49'
    pass
def p_literal_float_const(p):
    'literal : FLOAT_CONST'
    p[0] = 'Constant(Float-constant('+str(p[1])+'))'
    if (debug): print 's50'
    pass
def p_literal_string_const(p):
    'literal : STRING_CONST'
    p[0] = 'Constant(String-constant('+str(p[1])+'))'
    if (debug): print 's51'
    pass
def p_literal_null(p):
    'literal : NULL'
    p[0] = p[1]
    p[0] = 'Constant('+str(p[1])+')'
    if (debug): print 's52'
    pass
def p_literal_true(p):
    'literal : TRUE'
    p[0] = 'Constant(Boolean-constant('+str(p[1])+')'
    if (debug): print 's53'
    pass
def p_literal_false(p):
    'literal : FALSE'
    p[0] = 'Constant(Boolean-constant('+str(p[1])+')'
    if (debug): print 's54'
    pass

def p_primary_literal(p):
    'primary : literal'
    p[0] = p[1]
    if (debug): print 's55'
    pass
def p_primary_this(p):
    'primary : THIS'
    p[0] = 'This'
    if (debug): print 's56'
    pass
def p_primary_super(p):
    'primary : SUPER'
    p[0] = 'Super'
    if (debug): print 's57'
    pass
def p_primary_paren(p):
    'primary : LPAREN expr RPAREN'
    p[0] = '(' + p[2] + ')'
    if (debug): print 's58'
    pass
def p_primary_newobj(p):
    'primary : NEW ID LPAREN args_opt RPAREN'
    args = '[]'
    if (not p[4] is None):
        args = str(p[4])
    p[0] = 'New-object(' + str(p[2]) + ',' + args + ')'
    if (debug): print 's59'
    pass
def p_primary_lhs(p):
    'primary : lhs'
    if ('Field' in str(p[1])):
        p[0] = p[1]
    else:
        scope = fetchScope();
        found = False
        if (isinstance(scope, Method)):
            fields = classesMap[scope.containingClass].fieldList;
            for field in fields:
                if field.name == str(p[1]):
                    p[0] = 'Field-access(This, ' + str(p[1]) + ')'
                    found = True;
                    break
        if not found:
            varstr = _scopedVariable(str(p[1]));
            p[0] = varstr
    if (debug): print 's60'
    pass

def p_primary_method_invocation(p):
    'primary : method_invocation'
    p[0] = p[1]
    if (debug):     print 's61'
    pass

def p_args_opt_nonempty(p):
    'args_opt : arg_plus'
    p[0] = p[1]
    if (debug): print 's62'
    pass
def p_args_opt_empty(p):
    'args_opt : '
    if (debug): print 's63'
    pass

def p_args_plus(p):
    'arg_plus : arg_plus COMMA expr'
    p[0] = p[1],p[2]
    if (debug): print 's64'
    pass
def p_args_single(p):
    'arg_plus : expr'
    p[0] = p[1]
    if (debug): print 's65'
    pass

def p_lhs(p):
    '''lhs : field_access
           | array_access'''
    p[0] = p[1]
    if (debug): print 's66'
    pass

def p_field_access_dot(p):
    'field_access : primary DOT ID'
    #p[0] = p[1] + ', ' + p[3] + ')'
    p[0] = 'Field-access(' + p[1] + ', ' + p[3] + ')'
    if (debug): print 's67'
    pass
def p_field_access_id(p):
    'field_access : ID'
    p[0] = p[1]
    if (debug): print 's68'
    pass

def p_array_access(p):
    'array_access : primary LBRACKET expr RBRACKET'
    varstr = _scopedVariable(str(p[1]))
    p[0] = 'Array-Access(' + varstr + '),'+str(p[3])+')'
    if (debug): print 's69'
    pass

def p_method_invocation(p):
    'method_invocation : field_access LPAREN args_opt RPAREN'
    result=''
    arguments=p[3]
    if p[3] is None:
        arguments='[]'

    # Remove field access from the string
    if p[1] is not None:
        fieldAccess= str(p[1])
        fieldAccess = fieldAccess[13:]

    result += 'Method-call('+ fieldAccess
    result = result[:-1]
    result += ', ' + arguments+')'
    p[0] = result
    if (debug): print 's70'
    pass

def p_expr_basic(p):
    '''expr : primary
            | assign
            | new_array'''
    p[0] = p[1]
    if (debug): print 's71'
    pass
def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MULTIPLY expr
            | expr DIVIDE expr
            | expr EQ expr
            | expr NEQ expr
            | expr LT expr
            | expr LEQ expr
            | expr GT expr
            | expr GEQ expr
            | expr AND expr
            | expr OR expr
    '''
    if p[2] == '+':
        p[0] = 'Binary(add, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '-':
        p[0] = 'Binary(sub, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '*':
        p[0] = 'Binary(mul, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '/':
        p[0] = 'Binary(div, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '==':
        p[0] = 'Binary(eq, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '!=':
        p[0] = 'Binary(neq, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '<':
        p[0] = 'Binary(lt, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '<=':
        p[0] = 'Binary(leq, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '>':
        p[0] = 'Binary(gt, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '>=':
        p[0] = 'Binary(geq, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '&&':
        p[0] = 'Binary(and, '+str(p[1])+', '+str(p[3])+')'
    elif p[2] == '||':
        p[0] = 'Binary(or, '+str(p[1])+', '+str(p[3])+')'
    if (debug): print 's72'
    pass
def p_expr_unop(p):
    '''expr : PLUS expr %prec UMINUS
            | MINUS expr %prec UMINUS
            | NOT expr'''
    if (p[1] == '-'):
        p[0] = '-' + p[2]
    elif (p[1] == '!'):
        p[0] = 'not' + p[2]
    else:
        p[0] = p[2]
    if (debug): print 's73'
    pass

def p_assign_equals(p):
    'assign : lhs ASSIGN expr'
    pstr = str(p[1])
    varstr = _scopedVariable(pstr);
    p[0] = 'Assign(' + varstr + ', ' + str(p[3]) + ')'
    if (debug): print 's74'
    pass
def p_assign_post_inc(p):
    'assign : lhs INC'
    pstr = str(p[1])
    varstr = _scopedVariable(pstr);
    p[0] = 'Auto('+varstr+', inc, post)'

    if (debug): print 's75'
    pass
def p_assign_pre_inc(p):
    'assign : INC lhs'
    p[0] = 'Auto('+p[2]+', inc, pre)'
    if (debug): print 's76'
    pass
def p_assign_post_dec(p):
    'assign : lhs DEC'
    p[0] = 'Auto('+p[1]+', dec, post)'
    if (debug): print 's77'
    pass
def p_assign_pre_dec(p):
    'assign : DEC lhs'
    p[0] = 'Auto('+p[2]+', inc, pre)'
    if (debug): print 's78'
    pass

def p_new_array(p):
    'new_array : NEW type dim_expr_plus dim_star'
    dimstr = ''
    if (p[3]):
        dimstr = '('
        for elem in p[3]:
            dimstr +=  str(elem)+','
        dimstr = dimstr[0:-1]
        dimstr += ')'
    p[0] = 'New-array(' + str(p[2]) + ',' + dimstr +')'
    if (debug): print 's79'
    pass

def p_dim_expr_plus(p):
    'dim_expr_plus : dim_expr_plus dim_expr'
    if (debug): print 's80'
    p[0] = p[1] + (p[2],)
    pass
def p_dim_expr_single(p):
    'dim_expr_plus : dim_expr'
    p[0] = (p[1],)
    if (debug): print 's81'
    pass

def p_dim_expr(p):
    'dim_expr : LBRACKET expr RBRACKET'
    p[0] = p[2]
    if (debug): print 's82'
    pass

def p_dim_star(p):
    'dim_star : LBRACKET RBRACKET dim_star'
    p[0] = p[3]
    if (debug): print 's83'
    pass
def p_dim_star_empty(p):
    'dim_star : '
    if (debug): print 's84'
    pass

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''
    p[0] = p[1]
    if (debug): print 's85'
    pass

def p_stmt_expr_opt(p):
    'stmt_expr_opt : stmt_expr'
    p[0] = p[1]
    if (debug): print 's86'
    pass
def p_stmt_expr_empty(p):
    'stmt_expr_opt : '
    if (debug): print 's87'
    pass

def p_expr_opt(p):
    'expr_opt : expr'
    p[0] = p[1]
    if (debug): print 's88'
    pass
def p_expr_empty(p):
    'expr_opt : '
    if (debug): print 's89'
    pass


def p_error(p):
    if p is None:
        print ("Unexpected end-of-file")
    elif hasattr(p, 'message'):
        print str(p.message)
    else:
        print ("Unexpected token '{0}' near line {1}".format(p.value, p.lineno))
    parser.errok()
    decaflexer.errorflag = True

parser = yacc.yacc()

def from_file(filename):
    try:
        with open(filename, "rU") as f:
            init()
            p = parser.parse(f.read(), lexer=lex.lex(module=decaflexer), debug=0)
            AST = AbstractSyntaxTree(classlist = classes)
        return not decaflexer.errorflag, AST
    except IOError as e:
        print "I/O error: %s: %s" % (filename, e.strerror)


if __name__ == "__main__" :
    f = open(sys.argv[1], "r")
    logging.basicConfig(
            level=logging.CRITICAL,
    )
    log = logging.getLogger()
    res = parser.parse(f.read(), lexer=lex.lex(module=decaflexer), debug=log)

    if parser.errorok :
        print("Parse succeed")
    else:
        print("Parse failed")
