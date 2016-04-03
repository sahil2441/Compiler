from itertools import islice

import ast

class ResolvingClass:
    def __init__(self, objtype, valid):
        self.objtype = objtype;
        self.valid = valid;

currentMethod = ''
def validateBlock(block):
    for stmt in block.stmtlist:
        if isinstance(stmt, ast.ExprStmt):
            resolve(stmt.expr);

def resolve(expr, currentClass, currentScope = None):
    if isinstance(expr, ast.AssignExpr):
        lhs = expr.lhs;
        rhs = expr.rhs;
        objRHS = resolve(rhs, currentClass, currentScope);
        objLHS = resolve(lhs, currentClass, currentScope);
        if objRHS.valid and objLHS.valid:
            if str(objRHS.objtype.typename) == str(objLHS.objtype.typename):
                return ResolvingClass(None, True)
        return ResolvingClass(None, False)
    elif isinstance(expr, ast.FieldAccessExpr):
        if currentClass.fields.has_key(expr.fname):
            fieldobj = currentClass.fields[expr.fname]
            expr.resolvedId = fieldobj.id
            return ResolvingClass(ast.Type(fieldobj.type), True)
    elif isinstance(expr, ast.UnaryExpr):
        if expr.uop == 'uminus':
            obj = resolve(expr.arg, currentClass, currentScope)
            if (obj.valid and obj.objtype.typename in ('int', 'float') ):
                return obj
        elif expr.uop == 'neg':
            obj = resolve(expr.arg, currentClass, currentScope)
            if (obj.valid and obj.objtype.typename == 'boolean' ):
                return obj
        return ResolvingClass(None, False)
    elif isinstance(expr, ast.BinaryExpr):
        arg1 = expr.arg1;
        arg2 = expr.arg2;
        a = resolve(arg1, currentClass, currentScope);
        b = resolve(arg2, currentClass, currentScope);
        if (a.valid and b.valid):
            if (a.objtype.typename == b.objtype.typename):
                return ResolvingClass(None, True)
        return ResolvingClass(None, False)
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
                            print "Error at line " + str(x.lines)+". Incomaptible type found"