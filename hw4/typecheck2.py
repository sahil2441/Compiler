from itertools import islice

import ast
global globalClassTable

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
        print "objLHS: ", objLHS
        print "objRHS: ", objRHS
        if objRHS is not None and objRHS.valid and objLHS is not None and objLHS.valid:
            if str(objRHS.objtype.typename) == str(objLHS.objtype.typename):
                return ResolvingClass(None, True)
        return ResolvingClass(None, False)

    # TODO New object
    elif isinstance(expr, ast.NewObjectExpr):
        print  "Expr: ", expr
        # print "Current Class: ", currentClass
        # print "args: ", expr.args
        numberOfArguments = len(expr.args)

        if (len(expr.args ) is 0):
            return ResolvingClass(ast.Type(expr.classref.name), True)

        else:
            global globalClassTable
            # print "GCT: ", globalClassTable
            constructorClassName = expr.classref.name

            # First check whether the class is ever defined or not
            # i.e the class should exist in class table
            classDefined = False
            for key in globalClassTable:
                # print "Key: ", key
                if key == constructorClassName:
                    classDefined = True
            if classDefined is False:
                return ResolvingClass(None, False)

            # Now the class is defined. Now check if it has a constructor with same no of arguments
            args_flag = False
            for constructor in globalClassTable[constructorClassName].constructors:
                if numberOfArguments == len(constructor.vars.get_params()):
                    args_flag = True
            if args_flag is False:
                print "No constructor exists with those number of parameters."
                return ResolvingClass(None, False)

            # Now the number of arguments also match, i.e there exists at least one constructor with those no of
            # arguments. Now match the type.
            constructor_match_flag = False
            for constructor in globalClassTable[constructorClassName].constructors:
                if numberOfArguments == len(constructor.vars.get_params()):
                    print "param: ", constructor.vars[0]
                    # list_of_variables = constructor.vars.vars
                    # print "list of var: ", list_of_variables
                    # for i in range(len(list_of_variables)):
                    #     if(list_of_variables[i].vtype!= expr.args[i].vtype):
                    #         break
                    #     elif i== len(constructor.vars)-1:
                    #         constructor_match_flag = True
            if constructor_match_flag is False:
                return ResolvingClass(None, False)
            else:
                return ResolvingClass(ast.Type(expr.classref.name), True)

    elif isinstance(expr, ast.FieldAccessExpr):
        if currentClass.fields.has_key(expr.fname):
            fieldobj = currentClass.fields[expr.fname]
            expr.resolvedId = fieldobj.id
            return ResolvingClass(ast.Type(fieldobj.type), True)
    elif isinstance(expr, ast.AutoExpr):
        obj = resolve(expr.arg, currentClass, currentScope);
        if (not obj.objtype.typename in ('int', 'float')):
            return ResolvingClass(None, False)
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
                return a;
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
    global globalClassTable
    globalClassTable = classtable
    for cid in classtable:
        c = classtable[cid]
        for m in c.methods:
            if isinstance(m.body, ast.BlockStmt):
                for x in m.body.stmtlist:
                    if isinstance(x, ast.ExprStmt):
                        obj = resolve(x.expr, c);
                        if not obj.valid:
                            print "Error at line " + str(x.lines)+". Incomaptible type found"