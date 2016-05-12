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
    pass

dotdata = 0
functionList = []
currentFunc = ''
currentBlock = ''
labelBlockMap = dict()
interferanceGraphMap = dict()
graphColorMap = dict() # map to hold mapping of node and the associated color with it


def prepareInterferanceGraph():
    '''
    This function prepares the intereferance graph for the given set of invariables set
    :return:
    '''
    vertices = [] #set of unique vertices
    inVariableList = []

    for func in functionList:
        for block in func.blockList:
            inVariableList.append(block.inVariables)
            for var in block.inVariables:
                if var not in vertices:
                    vertices.append(var)
                    interferanceGraphMap[var] = [] # add an empty list corresponding to the key as var

    # iterate over all the unique vertices and find their corresponding edge
    for v in vertices:
        for list in inVariableList:
            if v in list:
                for x in list:
                    if x == v :
                        continue
                    list  = interferanceGraphMap[v]
                    if x not in list:
                        list.append(x)


def colorTheGraph():
    colorIndex = 1
    usedColor = []
    neighborColorList = []
    for key in interferanceGraphMap:
        # check if any used color can be used, by ensuring that it's not its neighbor
        listNeighbor = interferanceGraphMap[key] # prepare the neighbor colors list first
        for x in listNeighbor:
            if x in graphColorMap:
                neighborColorList.append(graphColorMap[x])
        flag = False
        for color in usedColor:
            # assign the node the used color if none of its neighborhas been assigned the same color
            if color not in neighborColorList:
                graphColorMap[key] = color
                flag = True
                break

        if not flag:
            graphColorMap[key] = colorIndex
            usedColor.append(colorIndex)
            colorIndex = colorIndex + 1


def translateToMips():
    '''
    This function translates to MIPS code
    :return:
    '''
    pass


def processIntermediateCode():
    '''
    Main entry point to process the intermediate code
    :return:
    '''
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

    processBlocks() # call the below method
    analyzeLiveness() # analyze liveness
    prepareInterferanceGraph() # prepare the interferance graph and prepare the map interferanceGraphMap
    colorTheGraph() #color the graph
    translateToMips() # to translate code to MIPS code

def processBlocks():
    '''
    This function processes the block
    :return:
    '''
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
                    if stmt.ra not in currentBlock.usedList and stmt.ra not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.ra)
                elif isinstance(stmt, absmc.Bnz_Instruction):
                    block = labelBlockMap[stmt.rb]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                    if stmt.ra not in currentBlock.usedList and stmt.ra not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.ra)
                elif isinstance(stmt, absmc.DefUseInstruction) or isinstance(stmt, absmc.HloadInstruction):
                    if stmt.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.ra)
                    if stmt.rb not in currentBlock.usedList and stmt.rb not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.rb)
                    if stmt.rc not in currentBlock.usedList:
                        currentBlock.usedList.append(stmt.rc)
                elif isinstance(stmt, absmc.Move_Immed_i_Instruction) or isinstance(stmt, absmc.Move_Immed_f_Instruction):
                    if stmt.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.ra)
                elif isinstance(stmt, absmc.Move_Instruction) or isinstance(stmt, absmc.HallocInstruction):
                    if stmt.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.ra)
                    if stmt.rb not in currentBlock.usedList  and stmt.rb not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.rb)
                elif isinstance(stmt, absmc.HstoreInstruction):
                    if stmt.ra not in currentBlock.usedList and stmt.ra not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.ra)
                    if stmt.rb not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.rb)
                    if stmt.rc not in currentBlock.usedList and stmt.rc not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.rc)


def deriveInSet(usedList, outVariables, definedList):
    resultList = usedList[:]
    unionSet = []
    for item in outVariables:
        if item not in definedList:
            unionSet.append(item)

    for x in unionSet:
        if x not in resultList:
            resultList.append(x)

    return resultList


def appendUnique(uniqueList, inVariables):
    for x in inVariables:
        if x not in uniqueList:
            uniqueList.append(x)
    return uniqueList


def compareBlockList(oldBlockList, blockList):
    for index in range(len(oldBlockList)):
        oldBlock = oldBlockList[index]
        block = blockList[index]
        if not set(oldBlock.inVariables) == set(block.inVariables) or\
            not set(oldBlock.outVariables) == set(block.outVariables) :
            return False
    return True


def analyzeLiveness():
    iterationCount = 0
    for function in functionList:
        n = len(function.blockList)
        while(True):
            oldBlockList = function.blockList[:]
            i = n-1
            while i > -1:
                currentBlock = function.blockList[i]
                if iterationCount is 0:
                    currentBlock.inVariables = deriveInSet(currentBlock.usedList, [], [])
                else:
                    uniqueList = []
                    for block in currentBlock.successorList:
                        currentBlock.outVariables = appendUnique(uniqueList, block.inVariables)
                    currentBlock.inVariables = deriveInSet(currentBlock.usedList, currentBlock.outVariables,
                                                           currentBlock.definedList)

                i = i - 1
            iterationCount = iterationCount + 1
            if compareBlockList(oldBlockList, function.blockList):
                break

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
            print "block.inVariables:  -->",block.inVariables
            print "block.outVariables:  -->",block.outVariables
            print "- - - "
    print "--------Graph-----------------"
    for key in interferanceGraphMap:
        print key, "-->", interferanceGraphMap[key]

    print "--------Graph Coloring-----------------"
    for key in graphColorMap:
        print key,"-->",graphColorMap[key]

def printMap():
    print "----MAP--------------------"
    for key in labelBlockMap:
        print "key: ", key, " value: ", labelBlockMap[key]








