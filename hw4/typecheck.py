from itertools import islice

import ast

class ResolvingClass:
    def __init__(self, objtype, valid, found="", expected="", nameresolution = ""):
        self.objtype = objtype;
        self.valid = valid;
        self.found = found;
        self.expected = expected;
        self.nameresolution = nameresolution;

classTable = dict();

def nameResolutionForNewObject(currentClass, currentScope, constructorName, arguments):
    # First check whether the class is ever defined or not
    # i.e the class should exist in class table
    classDefined = None
    if classTable.has_key(constructorName):
        classDefined = classTable[constructorName]
    if classDefined is None:
        return ResolvingClass(None, False, 'None', constructorName)
    # Now the class is defined. Now check if it has a constructor with same no of arguments
    args_flag = False
    for constructor in classDefined.constructors:
        if len(arguments) == len(constructor.vars.get_params()):
            if (len(arguments) == 0):
                return ResolvingClass(ast.Type(constructorName), True, nameresolution = constructor.id)
            args_flag = True
    if args_flag is False:
        return ResolvingClass(ast.Type("No constructor with those parameters"), False)

    # Now the number of arguments also match, i.e there exists at least one constructor with those no of
    # arguments. Now match the type.
    constructor_match_flag = False
    for constructor in classTable[constructorName].constructors:
        if len(arguments) == len(constructor.vars.get_params()) and checkParamTypes(constructor, arguments):
            return ResolvingClass(ast.Type(constructorName), True, nameresolution=constructor.id)
    return ResolvingClass(ast.Type("No constructor with those parameters"), False)


def resolve(expr, currentClass = None, currentScope = None):
    
    # Evaluate Assign Expression Type
    if isinstance(expr, ast.AssignExpr):
        lhs = expr.lhs;
        rhs = expr.rhs;
        objRHS = resolve(rhs, currentClass, currentScope);
        objLHS = resolve(lhs, currentClass, currentScope);
        if objRHS.valid and objLHS.valid:
            if str(objRHS.objtype.typename) == str(objLHS.objtype.typename):
                return ResolvingClass(objRHS.objtype, True)
        return ResolvingClass(None, False, objRHS.objtype.typename, objLHS.objtype.typename)

    # Evaluate New Object Expression
    elif isinstance(expr, ast.NewObjectExpr):
        # print "Current Class: ", currentClass
        # print "args: ", expr.args
        numberOfArguments = len(expr.args)
        obj = nameResolutionForNewObject(currentClass, currentScope, expr.classref.name, expr.args)
        if (obj.valid and not obj.objtype is None):
            expr.nameResolution = obj.nameresolution
        return obj
    
    # Evaluate Field Expression Type
    elif isinstance(expr, ast.FieldAccessExpr):
        if currentClass.fields.has_key(expr.fname):
            fieldobj = currentClass.fields[expr.fname]
            expr.resolvedId = fieldobj.id
            return ResolvingClass(ast.Type(fieldobj.type), True)
    
    # Evaluate Auto Expression Type
    elif isinstance(expr, ast.AutoExpr):
        obj = resolve(expr.arg, currentClass, currentScope); # We determine the operand type associated with the auto operators
        if (not obj.objtype.typename in ('int', 'float')): # auto operations are valid for int and float types only
            return ResolvingClass(obj, False, obj.objtype.typename, '(int or float)')
    
    # Evaluate Unary Expression Type
    elif isinstance(expr, ast.UnaryExpr):
        expected = '';
        if expr.uop == 'uminus': # If operator is -, then only int or float type operands are valid
            obj = resolve(expr.arg, currentClass, currentScope)
            expected = '(int or float)'
            if (obj.valid and obj.objtype.typename in ('int', 'float') ):
                return obj
        elif expr.uop == 'neg': # If operator is negation, then the operand should be of boolean type only
            expected = 'boolean'
            obj = resolve(expr.arg, currentClass, currentScope)
            if (obj.valid and obj.objtype.typename == 'boolean' ):
                return obj
        return ResolvingClass(None, False, obj.objtype.typename, expected)

    # Evaluate Binary Expression Type
    elif isinstance(expr, ast.BinaryExpr):
        arg1 = expr.arg1;
        arg2 = expr.arg2;
        a = resolve(arg1, currentClass, currentScope);# Recursivlely check the type of the left operand
        b = resolve(arg2, currentClass, currentScope);# Recursivlely check the type of the right operand
        if (a.valid and b.valid):
            if (a.objtype.typename == b.objtype.typename): #TODO subtyping
                return a;
        return ResolvingClass(a, False)
    
    # Evaluate Constant Expression Type
    elif isinstance(expr, ast.ConstantExpr):
        if expr.kind == 'int':
            return ResolvingClass(ast.Type('int'), True)
        elif expr.kind == 'float':
            return ResolvingClass(ast.Type('float'), True)
        elif expr.kind == 'string':
            return ResolvingClass(ast.Type('string'), True)
        elif expr.kind == 'Null':
            return ResolvingClass(ast.Type('null'), True)
        elif expr.kind == 'True' or expr.kind == 'False':
            return ResolvingClass(ast.Type('boolean'), True)
        
    # Evaluate Variable Expression Type
    elif isinstance(expr, ast.VarExpr):
        return ResolvingClass(ast.Type(expr.var.type), True)
    
    # Evaluate Meth Expression Type
    elif isinstance(expr, ast.MethodInvocationExpr):
        for method in currentClass.methods:
            if (method.name == expr.mname):
                ids = method.vars.get_params();
                if (len(ids) == len(expr.args) and checkParamTypes(method, expr.args)):
                    return ResolvingClass(ast.Type(method.rtype), True)
        return ResolvingClass(None, False)

def checkParamTypes(method, arguments):
    vartable = method.vars
    outermost = vartable.vars[0]
    ids = [outermost[vname].name for vname in outermost if outermost[vname].kind=='formal']
    count = 0;
    for id in ids:
        argParamObj = resolve(arguments[count])
        count = count + 1;
        formalParamType = str(outermost[id].type)
        if argParamObj.objtype.typename != formalParamType:
            if (not isSubType(argParamObj.objtype.typename, formalParamType)):
                return False;
    return True

def isSubType(aType, fType):
    if (aType == 'int' and fType == 'float'):
        return True;

def resolveBlock(m, c):
    for x in m.body.stmtlist:
        if isinstance(x, ast.ExprStmt):
            obj = resolve(x.expr, c, m);
            if not obj.valid:
                msg = ". {0} expression found where {1} is expected".format(obj.found, obj.expected)
                print "Type error at line " + str(x.lines)+msg

def checktype(classtable):
    lhstype = ''
    rhstype = ''
    global classTable
    classTable = classtable
    for cid in classtable:
        c = classtable[cid]
        for m in c.methods:
            if isinstance(m.body, ast.BlockStmt):
                resolveBlock(m, c);