from itertools import islice

import ast
def checktype(classtable):
    for cid in classtable:
        c = classtable[cid]
        for m in c.methods:
            if isinstance(m.body, ast.BlockStmt):
                for x in m.body.stmtlist:
                    if isinstance(x, ast.ExprStmt):
                        if isinstance(x.expr, ast.AssignExpr):
                            obj = x.expr;
                            # Determine type of LHS:
                            # Determine type of RHS:
                            # Make sure they match
                            if isinstance(obj.lhs, ast.FieldAccessExpr):
                                newobj = obj.lhs
                                print "fieldname : " + newobj.fname
                                if (c.fields.has_key(newobj.fname)):
                                    fieldobj = c.fields[newobj.fname]
                                    lhstype = fieldobj.type
                                    print 'lhs ' + str(lhstype)
                            elif isinstance(obj.lhs, ast.ArrayAccessExpr):
                                #TODO
                            elif isinstance(obj.lhs, ast.VarExpr):
                                #TODO
                            if isinstance(obj.rhs, ast.ConstantExpr):
                                newobj = obj.rhs
                                print 'rhs ' + newobj.kind
                                rhstype = newobj.kind
                            elif isinstance(obj.rhs, ast.BinaryExpr):
                                #TODO
                            elif isinstance(obj.rhs, ast.UnaryExpr):
                                #TODO
                            if str(lhstype) != str(rhstype):
                                print 'Error'