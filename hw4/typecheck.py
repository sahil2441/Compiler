from itertools import islice

import ast
errorFlag = False

class ResolvingClass:
    '''
    Data structure to hold the object type and error message and resolved name for the type
    '''
    def __init__(self, objtype, valid, errorMsg="", nameresolution = ""):
        self.objtype = objtype;
        self.valid = valid;
        self.errorMsg = errorMsg;
        self.nameresolution = nameresolution;
# global variable to store class dictionary
classTable = dict();

def fieldResoultion(currentClass, checkClass, fieldName, expr, checkStatic = True):
    '''
    :return: instance of resolvingClass
    This method checks if class is defined.
    If class is defined, check if field is defined.
    If field is defined, check the visibility and storage
    '''
    if (checkClass is None) or not classTable.has_key(checkClass.name):
        return ResolvingClass(ast.Type("error"), False, "No such class constructor exists!")
    if (checkClass.fields.has_key(fieldName)):
        fieldObj = checkClass.fields[fieldName]
        if fieldObj.visibility == 'private' and checkClass.name != currentClass.name:
            return ResolvingClass(ast.Type(fieldObj.type), False, "The field variable is not visible in current class")
        elif checkStatic and fieldObj.storage != 'static':
            return ResolvingClass(ast.Type(fieldObj.type), False, "Cannot access non static variable using class reference")
        expr.resolvedId = fieldObj.id
        return ResolvingClass(fieldObj.type, True)
    else:
        return ResolvingClass(ast.Type(fieldName), False, "No such field exists!")

def getSuperClasses(classInstance):
    '''
    :param classInstance:
    :return: comma separated string of superclass names for a class by recursion
    '''
    if classInstance is None:
        return ""
    l = str(classInstance.name) + ",";
    l = l + (getSuperClasses(classInstance.superclass))
    return l;

def nameResolutionForMethod (currentClass, currentScope, methodName, arguments, base):
    checkClass = None;
    # Check the accessor type : this or super or class literal
    if (base.objtype.kind == 'class'):
        classname = base.objtype.typename
        if currentClass.name == classname:
            checkClass = currentClass;
        elif classTable.has_key(classname):
            checkClass = classTable[classname]
    if checkClass is None:
        return ResolvingClass(ast.Type("error"), False, "The accessor class does not exist!")
    else:
        classesToCheck = getSuperClasses(classInstance=checkClass);
        classesArr = classesToCheck.split(",")
        validMethod = None
        validMethodCount = 0
        # Check if the method is present in the corresponding class and check the visibility and storage
        for classStr in classesArr:
            if classStr == '':
                continue
            checkClass = classTable[classStr]
            allmatchcount = 0;
            for method in checkClass.methods:
                ids = method.vars.get_params();
                if (method.name == methodName):
                    if ((method.visibility == 'private' and checkClass.name == currentClass.name) or method.visibility == 'public'):
                        if (len(arguments) == 0 and len(ids) == 0):
                            validMethod = method
                            break
                        elif len(ids) == len(arguments):
                            match, matchcount = checkParamTypes(method, arguments, currentClass, currentScope)
                            if match:
                                allmatchcount += matchcount;
                                validMethodCount += 1
                                validMethod = method
            if allmatchcount > 0 and validMethodCount > 1:
                return ResolvingClass(ast.Type("error"), False, "The method invocation resolve to more than one method!")
        if validMethod is None:
            return ResolvingClass(ast.Type("error"), False, "The method does not exist!")
        return ResolvingClass(ast.Type(validMethod.rtype), True, nameresolution=validMethod.id)


def nameResolutionForNewObject(currentClass, currentScope, constructorName, arguments):
    # First check whether the class is ever defined or not
    # i.e the class should exist in class table
    classDefined = None
    if classTable.has_key(constructorName):
        classDefined = classTable[constructorName]
    if classDefined is None:
        return ResolvingClass(ast.Type("error"), False, "No such class defined")
    # Now the class is defined. Now check if it has a constructor with same no of arguments
    args_flag = False
    for constructor in classDefined.constructors:
        if len(arguments) == len(constructor.vars.get_params()):
            if (len(arguments) == 0):
                if (constructor.visibility == 'private' and currentClass.name != classDefined.name):
                    return ResolvingClass(ast.Type(constructorName), False, "New object with this constructor cannot be created outside its class")
                return ResolvingClass(ast.Type(constructorName), True, nameresolution = constructor.id)
            args_flag = True
    if args_flag is False:
        return ResolvingClass(ast.Type(constructorName), False, "No such constructor found for class {0}".format(constructorName))

    # Now the number of arguments also match, i.e there exists at least one constructor with those no of
    # arguments. Now match the type.
    allmatchcount = 0
    validconstructorcount = 0;
    validConstructor = None
    for constructor in classTable[constructorName].constructors:
        if len(arguments) == len(constructor.vars.get_params()):
            match, matchcount = checkParamTypes(constructor, arguments, currentClass, currentScope)
            if match:
                allmatchcount += matchcount
                validConstructor =  ResolvingClass(ast.Type(constructorName), True, nameresolution=constructor.id)
                validconstructorcount += 1
    if allmatchcount > 0 and validconstructorcount > 1:
        return ResolvingClass(ast.Type("error"), False, "The object creation resolves using more than one constructor!")
    if not validConstructor is None:
        return validConstructor;
    return ResolvingClass(ast.Type(constructorName), False, "No constructor with those parameters for class {0}".format(constructorName))


def resolve(expr, currentClass = None, currentScope = None):
    '''
    Main recursive method which checks the validity of each expression
    :param expr:
    :param currentClass:
    :param currentScope:
    :return: instance of Resolving class object
    '''
    if isinstance(expr, ast.ThisExpr):
        return ResolvingClass(ast.Type(currentClass.name), True)

    elif isinstance(expr, ast.ClassReferenceExpr):
        return ResolvingClass(ast.Type(expr.classref.name), True)

    elif isinstance(expr, ast.SuperExpr):
        return ResolvingClass(ast.Type(currentClass.superclass.name), True)
    # Evaluate Assign Expression Type
    elif isinstance(expr, ast.AssignExpr):
        lhs = expr.lhs;
        rhs = expr.rhs;
        objRHS = resolve(rhs, currentClass, currentScope);
        objLHS = resolve(lhs, currentClass, currentScope);
        if objRHS.valid and objLHS.valid:
            lhsType = str(objLHS.objtype.typename)
            rhsType = str(objRHS.objtype.typename)
            subTypeBool, sameType = isSubType(objRHS.objtype, objLHS.objtype)
            if subTypeBool:
                expr.lhstype = lhsType;
                expr.rhstype = rhsType
                return ResolvingClass(objRHS.objtype, True)
            else:
                return ResolvingClass(ast.Type("error"), False, "{0} found where {1} is expected".format(lhsType, rhsType))
        elif not objRHS.valid:
            return objRHS;
        else:
            return objLHS;

    # Evaluate New Object Expression
    elif isinstance(expr, ast.NewObjectExpr):
        obj = nameResolutionForNewObject(currentClass, currentScope, expr.classref.name, expr.args)
        if (obj.valid and not obj.objtype is None):
            expr.nameResolution = obj.nameresolution
        return obj
    
    # Evaluate Field Expression Type
    elif isinstance(expr, ast.FieldAccessExpr):
        # If the base object is a Class Reference, then check whether the corresponding field access is for a static variable
        if isinstance(expr.base, ast.ClassReferenceExpr):
            checkClass = expr.base.classref;
            # check if the field access is for a static variable, also check its visibility
            return fieldResoultion(currentClass, checkClass, expr.fname, expr, checkStatic = True);
        elif isinstance(expr.base, ast.SuperExpr):
            return fieldResoultion(currentClass, currentClass.superclass, expr.fname, expr, checkStatic = False);
        else:
            return fieldResoultion(currentClass, currentClass, expr.fname, expr, checkStatic = False);
    
    # Evaluate Auto Expression Type
    elif isinstance(expr, ast.AutoExpr):
        obj = resolve(expr.arg, currentClass, currentScope); # We determine the operand type associated with the auto operators
        if (not obj.objtype.typename in ('int', 'float')): # auto operations are valid for int and float types only
            return ResolvingClass(obj, False, "{0} is found where {1} is expected".format(obj.objtype.typename, '(int or float)'))
        expr.exprtype = str(obj.objtype.typename)
        return ResolvingClass(obj, True)
    
    # Evaluate Unary Expression Type
    elif isinstance(expr, ast.UnaryExpr):
        expected = '';
        if expr.uop == 'uminus': # If operator is -, then only int or float type operands are valid
            obj = resolve(expr.arg, currentClass, currentScope)
            expected = '(int or float)'
            if (obj.valid and obj.objtype.typename in ('int', 'float') ):
                expr.exprtype = str(obj.objtype.typename)
                return obj
        elif expr.uop == 'neg': # If operator is negation, then the operand should be of boolean type only
            expected = 'boolean'
            obj = resolve(expr.arg, currentClass, currentScope)
            if (obj.valid and obj.objtype.typename == 'boolean' ):
                expr.exprtype = str(obj.objtype.typename)
                return obj
        return ResolvingClass(ast.Type("error"), False, "{0} is found where {1} is expected".format(obj.objtype.typename, expected))

    # Evaluate Binary Expression Type
    elif isinstance(expr, ast.BinaryExpr):
        arg1 = expr.arg1;
        arg2 = expr.arg2;
        a = resolve(arg1, currentClass, currentScope);# Recursivlely check the type of the left operand
        b = resolve(arg2, currentClass, currentScope);# Recursivlely check the type of the right operand
        if (a.valid and b.valid):
            if (a.objtype.typename in ('int', 'float') and b.objtype.typename in ('int', 'float')):
                if (a.objtype.typename == 'float'):
                    expr.exprtype = str(a.objtype.typename)
                    return a;
                expr.exprtype = str(b.objtype.typename)
                return b;
        return ResolvingClass(a, False, "Incompatible binary operation on types detected")
    
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
        elif expr.kind == 'error':
            return ResolvingClass(ast.Type('error'), False)
        elif expr.kind == 'void':
            return ResolvingClass(ast.Type('void'), True)
        elif expr.kind == 'True' or expr.kind == 'False':
            return ResolvingClass(ast.Type('boolean'), True)
        
    # Evaluate Variable Expression Type
    elif isinstance(expr, ast.VarExpr):
        kind = expr.var.type.kind
        if (kind == 'array'):
            return ResolvingClass(expr.var.type, True)
        return ResolvingClass(ast.Type(expr.var.type.typename), True)

    # Evaluate Meth Expression Type
    elif isinstance(expr, ast.MethodInvocationExpr):
        base = resolve(expr.base, currentClass, currentScope);
        obj = nameResolutionForMethod(currentClass, currentScope, expr.mname, expr.args, base)
        if (obj.valid):
            expr.nameResolution = obj.nameresolution
        return obj

    # Evaluate array access - the index elements should be of type int
    elif isinstance(expr, ast.ArrayAccessExpr):
        obj = resolve(expr.base, currentClass, currentScope)
        indextype = resolve(expr.index, currentClass, currentScope);
        if (indextype.objtype.typename != 'int'):
            return ResolvingClass(ast.Type("error"), False, "Array access index should be of int type")
        try:
            return ResolvingClass(obj.objtype.basetype, True)
        except:
            return ResolvingClass(ast.Type("error"), False, "Invalid array access!.")

    # Evaluate new array creation - the index elements should be of type int
    elif isinstance(expr, ast.NewArrayExpr):
        for arg in expr.args:
            indextype = resolve(arg, currentClass, currentScope);
            if (indextype.objtype.typename != 'int'):
                return ResolvingClass(ast.Type("error"), False, "Array initialization parameter should be of int type")
        return ResolvingClass(ast.Type(expr.basetype, len(expr.args)), True)

def checkParamTypes(method, arguments, currentClass, currentScope):
    '''
    Check the signature of the parameters and compare with the arugments passed
    :param method:
    :param arguments:
    :param currentClass:
    :param currentScope: constructor or method
    :return:
    '''
    vartable = method.vars
    outermost = vartable.vars[0]
    ids = [outermost[vname].name for vname in outermost if outermost[vname].kind=='formal']
    count = 0;
    sameTypeCount = 0;
    for id in ids:
        argParamObj = resolve(arguments[count], currentClass, currentScope)
        count = count + 1;
        formalParamType = outermost[id].type;
        subTypeBool, sameType = isSubType(argParamObj.objtype, formalParamType)# argParamObj.objtype must be strict subtype of formalParamType in case of multiple parameters
        sameTypeCount += sameType
        if (not subTypeBool):
            return False, 0;
    if (sameTypeCount == len(ids)):
        sameTypeCount = 0 # If the parameters are strict subtypes then it is fine. So we reset the value to 0
    return True, sameTypeCount

def isSubType(aType, fType):
    '''
    Subtype checking for every parameter
    :param aType:
    :param fType:
    :return:
    '''
    if (aType.kind == 'basic'):
        if (fType.kind == 'basic'):
            if (aType.typename  == fType.typename):
                return True, 0;
            if(aType.typename == 'int' and fType.typename == 'float'):
                return True, 1;
        if (aType.typename == 'null' and fType.kind == 'class'):
            return True, 1;
    elif (aType.kind == 'class'):
        if fType.kind == 'class':
            if (aType.typename == fType.typename):
                return True, 0
            if (not classTable.has_key(aType.typename) or not classTable.has_key(fType.typename)):
                return False, 0
            aClass = classTable[aType.typename];
            fClass = classTable[fType.typename];
            asuperClassesStr = getSuperClasses(aClass);
            asuperClasses = asuperClassesStr.split(",")
            for aSuperClass in asuperClasses:
                if aSuperClass == fClass.name:
                    return True , 1;
        return False, 0
    elif (aType.kind == 'array'):
        if (fType.kind == 'array'):
            if (str(aType.typename) == str(fType.typename)):
                return True, 0
            if (not classTable.has_key(aType.typename) or not classTable.has_key(fType.typename)):
                return False, 0
            aClass = classTable[aType.typename];
            fClass = classTable[fType.typename];
            asuperClassesStr = getSuperClasses(aClass);
            asuperClasses = asuperClassesStr.split(",")
            for aSuperClass in asuperClasses:
                if aSuperClass == fClass.name:
                    return True , 1;
    return False, 0;

def resolveBlock(m, c):
    global errorFlag
    mbody = m
    if isinstance(m, ast.Method) or isinstance(m, ast.Constructor):
        mbody = m.body
    for x in mbody.stmtlist:
        if isinstance(x, ast.ExprStmt):
            obj = resolve(x.expr, c, m);
            if not obj.valid:
                msg = obj.errorMsg
                errorFlag = True;
                print "Type error at line " + str(x.lines)+". "+msg
        elif isinstance(x, ast.IfStmt):
            condObj = resolve (x.condition, c, m);
            if (not condObj.valid or (condObj.valid and condObj.objtype.typename != 'boolean')):
                print "Type error at line " + str(x.lines)+". The if condition is not Boolean"
                errorFlag = True;
            resolveBlock (x.thenpart, c);
            resolveBlock (x.elsepart, c);
        elif isinstance(x, ast.WhileStmt):
            condObj = resolve(x.cond, c, m);
            if (not condObj.valid or (condObj.valid and condObj.objtype.typename != 'boolean')):
                print "Type error at line " + str(x.lines)+". The While condition is not Boolean"
                errorFlag = True;
            resolveBlock(x.body, c);
        elif isinstance(x, ast.ForStmt):
            condObj = resolve(x.cond, c, m);
            if (not condObj.valid or (condObj.valid and condObj.objtype.typename != 'boolean')):
                print "Type error at line " + str(x.lines)+". The For condition is not Boolean"
                errorFlag = True;
            initObj = resolve(x.init, c, m)
            if (not initObj.valid):
                print "Type error at line " + str(x.lines)+". The init expression in For is incorrect"
                errorFlag = True;
            updateObj = resolve(x.update, c, m)
            if (not updateObj.valid):
                print "Type error at line " + str(x.lines)+". The update expression in For is incorrect"
                errorFlag = True;
            resolveBlock(x.body, c);
        elif isinstance(x, ast.ReturnStmt):
            if (x.expr is None):
                obj = ResolvingClass(ast.Type("void"), True)
            else:
                obj = resolve(x.expr, c, m)
            if (not obj.valid):
                print "Type error at line " + str(x.lines)+". The return expression is incorrect!"
                errorFlag = True;
            if isinstance(m, ast.Constructor):
                print "Type error at line " + str(x.lines)+". Constructor cannot return anything!"
                errorFlag = True;
            elif isinstance(m, ast.Method):
                subTypeBool, sameType = isSubType(obj.objtype, m.rtype)
                if not subTypeBool:
                    print "Type error at line " + str(x.lines)+". The return type does not match with method return type!"
                    errorFlag = True;
    return errorFlag


'''
Main method which is invoked after the construction of AST for typechecking
'''
def checktype(classtable):
    global errorFlag;
    global classTable;
    classTable = classtable
    for cid in classtable:
        c = classtable[cid]
        for m in c.methods:
            if isinstance(m.body, ast.BlockStmt):
                errorFlag = resolveBlock(m, c);
        for m in c.constructors:
            if isinstance(m.body, ast.BlockStmt):
                errorFlag = resolveBlock(m, c);
    return errorFlag;