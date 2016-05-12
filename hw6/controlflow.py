import absmc;

class Function:
    def __init__(self, name):
        self.blockList = []
        self.name = name;

class Block:
    def __init__(self, name):
        self.statementList = []
        self.successorList = []

class Statement:
    def __init__(self):
        self.liveList = []
        self.inSet = []
        self.outSet = []

dotdata = 0
functionList = []
currentFunc = ''
currentBlock = ''
labelBlockMap = dict()

def processIntermediateCode():
    for instr in absmc.instructionList:
        if isinstance(instr, absmc.Misc_Instruction) and 'static_data' in instr.stmt:
            dotdata = int(instr.arg2)

        elif isinstance(instr, absmc.FunctionLabel_Instruction):
            newFunc = Function(instr.label)
            functionList.append(newFunc)
            currentFunc = newFunc
            currentBlock = Block(instr.label) # same name as function start
            labelBlockMap[str(instr.label)] = currentBlock # Update the map
            currentFunc.blockList.append(currentBlock)

        elif isinstance(instr, absmc.Label_Instruction):
            newBlock = Block(instr.label) # Same name as block label
            labelBlockMap[instr.label] = currentBlock # Update the map
            currentFunc.blockList.append(newBlock)
            currentBlock = newBlock

        else:
            currentBlock.statementList.append(instr)

def generateSuccessorBlocks():
    for func in functionList:
        for currentBlock in func.blockList:
            pass

def analyzeLiveness():
    for function in functionList:
        for block in function.blockList:
            # getRegistersUsedInBlock(block)
            # getRegistersUsedInBlock(block)
            pass


# print methods for debug

def printInstructionList():
    for instr in absmc.instructionList:
        print instr
    print "------------------------"
    print "----AMI ENDS--------------------"

def printFucntionList():
    for func in functionList:
        print "---------Func Decl---------------"
        for block in func.blockList:
            for stmt in block.statementList:
                print stmt
            print "- - - "

def printMap():
    print "----MAP--------------------"
    for key in labelBlockMap:
        print "key: ", key, " value: ", labelBlockMap[key]





