staticAreaCounter = 0
registerMap = dict() # Map of variable name/id/type to register address
attributeRegister = -1;
temporaryRegister = -1;

class INSTRUCTION(object):
    instList =  [ 'move_immed_i',
                  'move_immed_f',
                  'move',
                  'iadd',
                  'isub',
                  'imul',
                  'idiv',
                  'imod',
                  'igt',
                  'igeq',
                  'ilt',
                  'ileq',
                  'fadd',
                  'fsub',
                  'fmul',
                  'fdiv',
                  'fgt',
                  'fgeq',
                  'flt',
                  'fleq',
                  'itof',
                  'ftoi',
                  'hload',
                  'hstore',
                  'halloc',
                  'bz',
                  'bnz',
                  'jmp',
                  'call',
                  'ret',
                  'save',
                  'restore',
                  'peek',
                  'nop',
                  ]

    MOVE_IMMED_I,MOVE_IMMED_F,MOVE, IADD,ISUB,IMUL,IDIV,IMOD,IGT,IGEQ,ILT,ILEQ, \
    FADD,FSUB,FMUL,FDIV,FGT,FGEQ,FLT,FLEQ, ITOF,FTOI, \
    HLOAD,HSTORE,HALLOC,BZ,BNZ,JMP, CALL,RET,SAVE,RESTORE,PEEK,NOP = instList


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
