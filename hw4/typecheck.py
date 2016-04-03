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

def resolve(expr, currentClass):
    if isinstance(expr, ast.AssignExpr):
        lhs = expr.lhs;
        rhs = expr.rhs;
        print 'lhs '+ str(type(lhs))
        print 'lhs '+ str(type(rhs))
        objRHS = resolve(rhs, currentClass);
        objLHS = resolve(lhs, currentClass);
        if objRHS.valid and objLHS.valid:
            if str(objRHS.objtype.kind) == str(objLHS.objtype.kind):
                return ResolvingClass(None, True)
        return ResolvingClass(None, False)
    elif isinstance(expr, ast.FieldAccessExpr):
        if currentClass.fields.has_key(expr.fname):
            fieldobj = currentClass.fields[expr.fname]
            expr.resolvedId = fieldobj.id
            return ResolvingClass(ast.Type(fieldobj.type), True)
    elif isinstance(expr, ast.BinaryExpr):
        arg1 = expr.arg1;
        arg2 = expr.arg2;
        a = resolve(arg1, currentClass);
        b = resolve(arg2, currentClass);
        if (a.valid and b.valid):
            if (a.objtype.kind == b.objtype.kind):
                return ResolvingClass(None, True)
    elif isinstance(expr, ast.ConstantExpr):
        if expr.kind == 'int':
            return ResolvingClass(ast.Type('int'), True)



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
                        if obj.valid:
                            print 'Everything is Fine'