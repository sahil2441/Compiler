import absmc;

class Function:
    def __init__(self, name):
        self.blockList = []
        self.name = name;

class Block:
    def __init__(self, name):
        self.statementList = []

class Statement:
    def __init__(self):
        self.liveList = []
        self.inSet = []
        self.outSet = []

dotdata = 0
functionList = []
currentFunc = ''
currentBlock = ''
def processIntermediateCode():
    for instr in absmc.instructionList:
        if isinstance(instr, absmc.Misc_Instruction) and 'static_data' in instr.stmt:
            dotdata = int(instr.arg2)
        elif isinstance(instr, absmc.FunctionLabel_Instruction):
            newFunc = Function(instr.label)
            functionList.append(newFunc)
            currentFunc = newFunc
            currentBlock = Block(instr.label)  # Same name as function start
            currentFunc.blockList.append(currentBlock)
        elif isinstance(instr, absmc.Label_Instruction):
            currentBlock = Block(instr.label)
            currentFunc.blockList.append(currentBlock)
        else:
            currentBlock.statementList.append()

def analyzeLiveness():
    for function in functionList:
        for block in function.blockList:
            getRegistersUsedInBlock(block)
            getRegistersUsedInBlock(block)





