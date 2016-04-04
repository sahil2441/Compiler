from itertools import islice

import ast

class ResolvingClass:
    def __init__(self, objtype, valid, found="", expected=""):
        self.objtype = objtype;
        self.valid = valid;
        self.found = found;
        self.expected = expected;

currentMethod = ''
def validateBlock(block):
    for stmt in block.stmtlist:
        if isinstance(stmt, ast.ExprStmt):
            resolve(stmt.expr);

def resolve(expr, currentClass = None, currentScope = None):
    if isinstance(expr, ast.AssignExpr):
        lhs = expr.lhs;
        rhs = expr.rhs;
        objRHS = resolve(rhs, currentClass, currentScope);
        objLHS = resolve(lhs, currentClass, currentScope);
        if objRHS.valid and objLHS.valid:
            if str(objRHS.objtype.typename) == str(objLHS.objtype.typename):
                return ResolvingClass(None, True)
        return ResolvingClass(None, False, objRHS.objtype.typename, objLHS.objtype.typename)
    elif isinstance(expr, ast.FieldAccessExpr):
        if currentClass.fields.has_key(expr.fname):
            fieldobj = currentClass.fields[expr.fname]
            expr.resolvedId = fieldobj.id
            return ResolvingClass(ast.Type(fieldobj.type), True)
    elif isinstance(expr, ast.AutoExpr):
        obj = resolve(expr.arg, currentClass, currentScope);
        if (not obj.objtype.typename in ('int', 'float')):
            return ResolvingClass(obj, False, obj.objtype.typename, '(int or float)')
    elif isinstance(expr, ast.UnaryExpr):
        expected = '';
        if expr.uop == 'uminus':
            obj = resolve(expr.arg, currentClass, currentScope)
            expected = '(int or float)'
            if (obj.valid and obj.objtype.typename in ('int', 'float') ):
                return obj
        elif expr.uop == 'neg':
            expected = 'boolean'
            obj = resolve(expr.arg, currentClass, currentScope)
            if (obj.valid and obj.objtype.typename == 'boolean' ):
                return obj
        return ResolvingClass(None, False, obj.objtype.typename, expected)
    elif isinstance(expr, ast.BinaryExpr):
        arg1 = expr.arg1;
        arg2 = expr.arg2;
        a = resolve(arg1, currentClass, currentScope);
        b = resolve(arg2, currentClass, currentScope);
        if (a.valid and b.valid):
            if (a.objtype.typename == b.objtype.typename):
                return a;
        return ResolvingClass(a, False)
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
    elif isinstance(expr, ast.VarExpr):
        return ResolvingClass(ast.Type(expr.var.type), True)
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
    doSubTypeCheck = False;
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

def checktype(classtable):
    lhstype = ''
    rhstype = ''
    for cid in classtable:
        c = classtable[cid]
        for m in c.methods:
            if isinstance(m.body, ast.BlockStmt):
                for x in m.body.stmtlist:
                    if isinstance(x, ast.ExprStmt):
                        obj = resolve(x.expr, c);
                        if not obj.valid:
                            msg = ". {0} expression found where {1} is expected".format(obj.found, obj.expected)
                            print "Type error at line " + str(x.lines)+msg