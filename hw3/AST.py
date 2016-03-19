class Constructor(object):
    def __init__(self):
        self.id = "";
        self.visibility = "";
        self.parameters = list();
        self.variables = dict();
        self.body = "";

class Method(object):
    def __init(self, name, id):
        self.name = name;
        self.id = id;
        self.containingClass = "";
        self.visibility = "";
        self.applicability = "";
        self.parameters = list();
        self.returnType = "";
        self.variables = dict();
        self.body = "";

class Field(object):
    def __init__(self, name, id):
        self.name = name;
        self.id = id;
        self.containingClass = "";
        self.visibility = "";
        self.applicability = "";
        self.type = "";

    def toString(self):
        return ", ".join("FIELD "+self.id, self.name, self.containingClass, self.visibility, self.applicability, self.type);

class Variable(object):
    def __init__(self, name, id):
        self.name = name;
        self.id = id;
        self.kind = "";
        self.type = "";

class Type(object):
    def __init__(self, basetype):
        self.base = basetype

class Statement(object):
    #TODO
    def __init__(self):
        pass;



class DecafClass(object):
    def __init__(self, name):
        self.name = name;
        self.superclass = "";
        self.constructorList = list();
        self.fieldList = list();
        self.methods = list();


    def superClass(self, superclass):
        self.superclass = superclass;


    def toString(self):
        retstr = ""
        retstr += "Class Name: " + self.name + "\n";
        retstr += "Superclass Name: " + self.superclass + "\n";
        retstr += "Fields:\n";
        for field in self.fieldList:
            #retstr += field.toString();
            retstr += ", ".join("FIELD "+field.uid, field.name, field.containingClass, field.visibility, field.applicability, field.type);
        retstr += "Constructors:\n";
        for constructor in self.constructorList:
            retstr += ", ".join("CONSTRUCTOR: " + constructor.uid, constructor.visibility);
            retstr += "\n";
            retstr += "Constructor Parameters: \n";#TODO
            retstr += "Variable Table:\n";#TODO
            retstr += "Constructor Body:\n";#TODO
            for block in constructor.blocks:
                retstr += block.toString()+"\n";#TODO
        retstr += "Methods:\n"
        for method in self.methods:
            retstr += ", ".join("METHOD: "+method.uid,method.name, method.containingClass, method.visibility, method.applicability, method.returnType)
            retstr += "\nMethod Parameters: "+len(method.parameters)
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
            retStr += structure.toString()
            retStr +="\n"
        return retStr;


if __name__ == '__main__':
    new =DecafClass("jugu")
    new.test("soww")
    print new.toString()

