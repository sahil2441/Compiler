sapRegisterOffset = {}
staticAreaCounter = 0
heapStartRegister = 0
registerMap = dict() # Map of variable name/id/type to register address
instructionList = list()
attributeRegister = -1;
temporaryRegister = -1;
controlStack = []
dataStack = []
labelCounter = 0
labelStack = []
registerSizeMap = {}

currentLoopInLabel = '' # Track the current Loop's in label in case of continue statement
currentLoopOutLabel = '' # Track the current Loop's out label in case of break statement

mainFunction = False

import ast
import sys
import controlflow

class Instruction:
    pass

class DefUseInstruction(Instruction):
    pass

class UseInstruction(Instruction):
    pass

class Misc_Instruction(Instruction):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.stmt = ", ".join([arg1, arg2]);
        self.block = None

    def translateToMips(self):
        retstr = ''
        if ("static_" in self.arg1):
            retstr =  '.data ' + str(self.arg2)
            retstr += '\n.text'
        return retstr


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.stmt

class Label_Instruction(Instruction):
    def __init__(self, arg1):
        self.label = arg1;

    def translateToMips(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.label+  ':'

class FunctionLabel_Instruction(Instruction):
    def __init__(self, arg1):
        self.label = arg1;

    def translateToMips(self):
        global mainFunction
        if 'M_main_' in self.label:
            mainFunction = True
            return 'main_entry_point:'
        else:
            mainFunction = False
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.label + ':'

class Move_Immed_i_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegister = graphcolorMap[self.ra];
        mappedRegister = controlflow.getMipsTemporaryRegister(mappedRegister)
        return ', '.join(['li ' + mappedRegister, str(self.rb)])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.MOVE_IMMED_I, str(self.ra), str(self.rb)])

class Move_Immed_f_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegister = graphcolorMap[self.ra];
        mappedRegister = controlflow.getMipsTemporaryRegister(mappedRegister)
        return ', '.join(['li '+ mappedRegister, str(self.rb)])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.MOVE_IMMED_F, str(self.ra), str(self.rb)])

class Move_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterA = controlflow.getMipsTemporaryRegister(mappedRegisterA)
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterB = controlflow.getMipsTemporaryRegister(mappedRegisterB)
        return ", ".join(["move "+ mappedRegisterA, mappedRegisterB])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.MOVE, self.ra, self.rb])

######################################################################
######################################################################

# Definition for integer

class AddInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterA = controlflow.getMipsTemporaryRegister(mappedRegisterA)
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterB = controlflow.getMipsTemporaryRegister(mappedRegisterB)
        mappedRegisterC = graphcolorMap[self.rc];
        mappedRegisterC = controlflow.getMipsTemporaryRegister(mappedRegisterC)
        return ', '.join(['add '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.IADD, self.ra, self.rb , self.rc])

class SubInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sub '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.ISUB, self.ra, self.rb , self.rc])

class MulInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['mul '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.IMUL, self.ra, self.rb , self.rc])

class DivInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['div '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.IDIV, self.ra, self.rb , self.rc])

class ModInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['rem '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.IMOD, self.ra, self.rb , self.rc])

class GtInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sgt '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.IGT, self.ra, self.rb , self.rc])

class GeqInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sge '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.IGEQ, self.ra, self.rb , self.rc])

class LtInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['slt ' + mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.ILT, self.ra, self.rb , self.rc])

class LeqInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sle '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.ILEQ, self.ra, self.rb , self.rc])

######################################################################
######################################################################

# similar definitions for float

class AddInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['add '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FADD, self.ra, self.rb , self.rc])

class SubInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sub '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FSUB, self.ra, self.rb , self.rc])

class MulInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['mul '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FMUL, self.ra, self.rb , self.rc])

class DivInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['div '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FDIV, self.ra, self.rb , self.rc])

class ModInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['rem '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FMOD, self.ra, self.rb , self.rc])

class GtInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sgt '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FGT, self.ra, self.rb , self.rc])

class GeqInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sge '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FGEQ, self.ra, self.rb , self.rc])

class LtInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['slt '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FLT, self.ra, self.rb , self.rc])

class LeqInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['sle '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FLEQ, self.ra, self.rb , self.rc])

class LtInstructionFloat(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        mappedRegisterB = graphcolorMap[self.rb];
        mappedRegisterC = graphcolorMap[self.rc];
        return ', '.join(['slt '+ mappedRegisterA, mappedRegisterB, mappedRegisterC])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FLT, self.ra, self.rb , self.rc])

######################################################################
######################################################################

class Itof_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.ITOF, self.ra, self.rb])

class Itoi_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.FTOI, self.ra, self.rb])

######################################################################
######################################################################

class HloadInstruction(DefUseInstruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        return 'TODO HLOAD'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.HLOAD, self.ra, self.rb , self.rc])

class HstoreInstruction(Instruction):
    def __init__(self, ra, rb, rc):
        self.ra = ra
        self.rb = rb
        self.rc = rc

    def translateToMips(self):
        return 'TODO HLOAD'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.HSTORE, self.ra, self.rb , self.rc])

class HallocInstruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def translateToMips(self):
        return 'TODO HALLOC'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.HALLOC, self.ra, self.rb])

######################################################################
######################################################################

class Bz_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        return ', '.join(['beqz '+ mappedRegisterA, self.rb])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.BZ, self.ra, self.rb])

class Bnz_Instruction(Instruction):
    def __init__(self, ra, rb):
        self.ra = ra
        self.rb = rb

    def translateToMips(self):
        graphcolorMap = controlflow.funcToGraphColorMap[self.function];
        mappedRegisterA = graphcolorMap[self.ra];
        return ', '.join(['bneqz '+ mappedRegisterA, self.rb])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.BNZ, self.ra, self.rb])

class Jmp_Instruction(Instruction):
    def __init__(self, ra):
        self.ra = ra

    def translateToMips(self):
        return ' '.join(['j', self.ra])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.JMP, self.ra])

######################################################################
######################################################################

class Call_Instruction(Instruction):
    def __init__(self, ra):
        self.ra = ra

    def translateToMips(self):
        return ' '.join(['jal', self.ra])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.CALL, self.ra])

class Ret_Instruction(Instruction):
    def __init__(self): pass

    def translateToMips(self):
        global mainFunction
        if mainFunction:
            return 'li $v0, 10\nsyscall'  # Exit
        return 'jr $ra'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.RET])

class Save_Instruction(Instruction):
    def __init__(self, ra):
        self.ra = ra

    def translateToMips(self):
        return 'TODO SAVE'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.SAVE, self.ra])

class Restore_Instruction(Instruction):
    def __init__(self, ra):
        self.ra = ra

    def translateToMips(self):
        return 'TODO RESTORE'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.RESTORE, self.ra])

class Peek_Instruction(Instruction):
    def __init__(self, ra):
        self.ra = ra

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return " ".join([INSTRUCTION.PEEK, self.ra])

class Nop_Instruction(Instruction):
    def __init__(self, ra):
        self.ra = ra

    def __repr__(self):
        return self.__str__()

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

def add(instruction):
    instructionList.append(instruction)

def addAll(instList):
    for inst in instList:
        instructionList.append(inst)

def generateTemporaryRegister():
    global temporaryRegister
    temporaryRegister += 1;
    regStr = 't' + str(temporaryRegister);
    return regStr

def printAMI(filename):
    for instr in instructionList:
        print instr;

    # create new file
    # print the generated machine code into new file

    orig_stdout = sys.stdout
    filename = filename + '.ami'
    f = open(filename, 'w')
    # sys.stdout = f

    for instr in instructionList:
        print >>f , instr

    # sys.stdout = orig_stdout
    f.close()

def generateLabel():
    global labelCounter
    labelCounter += 1
    labelStr = 'label' + str(labelCounter);
    return labelStr

######################################################################
######################################################################

