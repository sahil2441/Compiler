class Constructor(object):
    def __init__(self, id, visibility="private"):
        self.id = id;
        self.visibility = visibility;
        self.parameters = list();
        self.variables = dict();
        self.body = "";
        self.blocks=list();

class Method(object):
    def __init__(self, id, name, containingClass = "", visibility="private", applicability="", returnType="void"):
        self.name = name;
        self.id = id;
        self.containingClass = containingClass;
        self.visibility = visibility;
        self.applicability = applicability;
        self.parameters = list();
        self.returnType = returnType;
        self.variables = dict();
        self.body = "";
    def toString(self):#TODO parameters, body
        return ", ".join(["METHOD: "+str(self.id), self.name, self.containingClass, self.visibility, self.applicability, self.returnType]);

class Field(object):
    def __init__(self, name, id, containingclass="", visibility="private", applicability="", type=""):
        self.name = name;
        self.id = id;
        self.containingClass = containingclass;
        self.visibility = visibility;
        self.applicability = applicability;
        self.type = type;

    def toString(self):
        return ", ".join(["FIELD "+str(self.id), self.name, self.containingClass, self.visibility, self.applicability, self.type]);

class Variable(object):
    def __init__(self, name, id=0, type=""):
        self.name = name;
        self.id = id;
        self.type = type;

class Type(object):
    def __init__(self, basetype):
        self.base = basetype

class Statement(object):
    #TODO
    def __init__(self):
        pass;



class DecafClass(object):
    def __init__(self, name, superclass=""):
        self.name = name;
        self.superclass = superclass;
        self.constructorList = list();
        self.fieldList = list();
        self.methodList = list();



    def toString(self):
        retstr = ""
        retstr += "Class Name: " + self.name + "\n";
        retstr += "Superclass Name: " + self.superclass + "\n";
        retstr += "Fields:\n";
        for field in self.fieldList:
            #retstr += field.toString();
            retstr +=', '.join(["FIELD "+str(field.id), field.name, field.containingClass, field.visibility, field.applicability, field.type])
            retstr +='\n'
        retstr += "Constructors:\n";
        for constructor in self.constructorList:
            retstr += ", ".join(["CONSTRUCTOR: " + str(constructor.id), constructor.visibility]);
            retstr += "\n";
            retstr += "Constructor Parameters:";
            paramstr = ""
            for param in constructor.parameters:
                paramstr += str(param.id)+ ","
            if (len(paramstr) > 0):
                paramstr = paramstr[0:-1]
                retstr += paramstr+"\n"
            retstr += "Variable Table:\n";#TODO
            retstr += "Constructor Body:\n";#TODO
            for block in constructor.blocks:
                retstr += block.toString()+"\n";#TODO
        retstr += "Methods:\n"
        for method in self.methodList:
            retstr += ", ".join(["METHOD: "+str(method.id), method.name, method.containingClass, method.visibility, method.applicability, method.returnType])
            retstr += "\nMethod Parameters: "+str(len(method.parameters))
            retstr += "\n"
            retstr += "Variable Table:\n"
            for variable in method.variables:
                retstr += ", ".join("VARIABLE: ", variable.id, variable.name, variable.containingClass, variable.kind, variable.type)
                retstr +="\n"
            retstr += "Method Body:\n"
            for block in method.body:
                retstr += block.toString() + "\n";#TODO




        return retstr

class AbstractSyntaxTree(object):
    def __init__(self, classlist):
        self.classes = classlist

    def toString(self):
        retStr = ""
        for structure in self.classes:
            print structure
            retStr += structure.toString()
            retStr +="---------------------------------------------------------------------------------------------\n"
        return retStr;


if __name__ == '__main__':
    new =DecafClass("jugu")
    new.test("soww")
    print new.toString()

