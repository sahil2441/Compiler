import absmc;

class Function:
    def __init__(self, name):
        self.blockList = []
        self.name = name;

class Block:
    def __init__(self, name):
        self.statementList = []
        self.successorList = []
        self.definedList = []
        self.usedList = []
        self.inVariables = []
        self.outVariables = []

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
            labelBlockMap[str(instr.label)] = currentBlock # Update the map
            currentFunc.blockList.append(newBlock)
            currentBlock = newBlock

        else:
            currentBlock.statementList.append(instr)

    # call the below method
    processBlocks()

def processBlocks():
    for func in functionList:
        for index, currentBlock in enumerate(func.blockList):
            if (index + 1 < len(func.blockList)): # for the next block in the list
                currentBlock.successorList.append(func.blockList[index+1])

            # also iterate all the statements in the block and check which are the successor blocks
            for stmt in currentBlock.statementList:
                if isinstance(stmt, absmc.Jmp_Instruction):
                    block = labelBlockMap[stmt.ra]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                elif isinstance(stmt, absmc.Bz_Instruction):
                    block = labelBlockMap[stmt.rb]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                    if stmt.ra not in currentBlock.usedList:
                        currentBlock.usedList.append(stmt.ra)
                elif isinstance(stmt, absmc.Bnz_Instruction):
                    block = labelBlockMap[stmt.rb]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                    if stmt.ra not in currentBlock.usedList:
                        currentBlock.usedList.append(stmt.ra)
                elif isinstance(stmt, absmc.DefUseInstruction):
                    if stmt.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.ra)
                    if stmt.rb not in currentBlock.usedList:
                        currentBlock.usedList.append(stmt.rb)
                    if stmt.rc not in currentBlock.usedList:
                        currentBlock.usedList.append(stmt.rc)
                elif isinstance(stmt, absmc.Move_Immed_i_Instruction) \
                    or isinstance(stmt, absmc.Move_Immed_f_Instruction):
                    if stmt.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.ra)
                elif isinstance(stmt, absmc.Move_Instruction):
                    if stmt.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.ra)
                    if stmt.rb not in currentBlock.usedList:
                        currentBlock.usedList.append(stmt.rb)

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
            print "block.successorList:  -->",block.successorList
            print "block.usedList:  -->",block.usedList
            print "block.definedList:  -->",block.definedList
            print "- - - "

def printMap():
    print "----MAP--------------------"
    for key in labelBlockMap:
        print "key: ", key, " value: ", labelBlockMap[key]







