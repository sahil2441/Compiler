staticAreaCounter = 0
registerMap = dict() # Map of variable name/id/type to register address
attributeRegister = -1;
temporaryRegister = -1;

class INSTRUCTION(object):
    instList =  ['ildc','iadd']#TODO CREATE LIST OF ALL INSTRUCTIONS WHICH IS MENTIONED IN HW5 DETAILS
    ILDC, IADD = instList


def methodMachineCode():
    pass

def constructorMachineCode():
    pass

def SSA():
    pass


def getRegister(obj):
    global attributeRegister, temporaryRegister
    key =  ','.join([obj.name, obj.id, obj.kind])
    if (not registerMap.has_key(key)):
        if (obj.kind == 'formal'):
            attributeRegister = attributeRegister + 1;
            registerMap[key] = attributeRegister;
            return attributeRegister
        else:
            temporaryRegister += 1;
            registerMap[key] = temporaryRegister
            return temporaryRegister
    else:
        return registerMap[key]


def printAMI():
    pass
    # create new file
    # print the generated machine code into new file
