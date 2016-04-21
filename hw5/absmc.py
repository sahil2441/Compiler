staticAreaCounter = 0
registerMap = dict() # Map of variable name/id/type to register address
instructionList = list()
attributeRegister = -1;
temporaryRegister = -1;

import ast
class Instruction:
	pass

class Move_Immed_i_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.MOVE_IMMED_I, self.ra, self.rb])

class Move_Immed_f_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.MOVE_IMMED_F, self.ra, self.rb])

class Move_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.MOVE, self.ra, self.rb])

######################################################################
######################################################################

# Definition for integer

class AddInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IADD, self.ra, self.rb , self.rc])

class SubInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.ISUB, self.ra, self.rb , self.rc])

class MulInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IMUL, self.ra, self.rb , self.rc])

class DivInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IDIV, self.ra, self.rb , self.rc])

class ModInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IMOD, self.ra, self.rb , self.rc])

class GtInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IGT, self.ra, self.rb , self.rc])

class GeqInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.IGEQ, self.ra, self.rb , self.rc])

class LtInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.ILT, self.ra, self.rb , self.rc])

class LeqInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.ILEQ, self.ra, self.rb , self.rc])

class LtInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.ILT, self.ra, self.rb , self.rc])

######################################################################
######################################################################

# similar definitions for float

class AddInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FADD, self.ra, self.rb , self.rc])

class SubInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FSUB, self.ra, self.rb , self.rc])

class MulInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FMUL, self.ra, self.rb , self.rc])

class DivInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FDIV, self.ra, self.rb , self.rc])

class ModInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FMOD, self.ra, self.rb , self.rc])

class GtInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FGT, self.ra, self.rb , self.rc])

class GeqInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FGEQ, self.ra, self.rb , self.rc])

class LtInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FLT, self.ra, self.rb , self.rc])

class LeqInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FLEQ, self.ra, self.rb , self.rc])

class LtInstructionFloat(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.FLT, self.ra, self.rb , self.rc])

######################################################################
######################################################################

class Itof_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.ITOF, self.ra, self.rb])

class Itoi_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.FTOI, self.ra, self.rb])

######################################################################
######################################################################

class HloadInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.HLOAD, self.ra, self.rb , self.rc])

class HstoreInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.HSTORE, self.ra, self.rb , self.rc])

class HallocInstruction(Instruction):
	def __init__(self, ra, rb, rc):
		self.ra = ra
		self.rb = rb
		self.rc = rc

	def __str__(self):
		return " ".join([INSTRUCTION.HALLOC, self.ra, self.rb , self.rc])

######################################################################
######################################################################

class Bz_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.BZ, self.ra, self.rb])

class Bnz_Instruction(Instruction):
	def __init__(self, ra, rb):
		self.ra = ra
		self.rb = rb

	def __str__(self):
		return " ".join([INSTRUCTION.BNZ, self.ra, self.rb])

class Jmp_Instruction(Instruction):
	def __init__(self, ra):
		self.ra = ra

	def __str__(self):
		return " ".join([INSTRUCTION.JMP, self.ra])

######################################################################
######################################################################

class Call_Instruction(Instruction):
	def __init__(self, ra):
		self.ra = ra

	def __str__(self):
		return " ".join([INSTRUCTION.CALL, self.ra])

class Ret_Instruction(Instruction):
	def __init__(self): pass

	def __str__(self):
		return " ".join([INSTRUCTION.RET])

class Save_Instruction(Instruction):
	def __init__(self, ra):
		self.ra = ra

	def __str__(self):
		return " ".join([INSTRUCTION.SAVE, self.ra])

class Restore_Instruction(Instruction):
	def __init__(self, ra):
		self.ra = ra

	def __str__(self):
		return " ".join([INSTRUCTION.RESTORE, self.ra])

class Peek_Instruction(Instruction):
	def __init__(self, ra):
		self.ra = ra

	def __str__(self):
		return " ".join([INSTRUCTION.PEEK, self.ra])

class Nop_Instruction(Instruction):
	def __init__(self, ra):
		self.ra = ra

	def __str__(self):
		return " ".join([INSTRUCTION.NOP, self.ra])

######################################################################
######################################################################

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
