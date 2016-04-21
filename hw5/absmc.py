staticAreaCounter = 0
registerMap = dict() # Map of variable name/id/type to register address
instructionList = list()
attributeRegister = -1;
temporaryRegister = -1;

import ast
class Instruction:
	pass

class AddInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IADD, self.ra, self.rb , self.rc])


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



def getRegister(obj):
    global attributeRegister, temporaryRegister
    if isinstance(obj, ast.ConstantExpr):
        obj.kind = ''
    key =  str(obj.id)
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
