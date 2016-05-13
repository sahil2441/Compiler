import absmc;
import sys;
class MIPS:
    STACK = []
    RESULTREGISTER = ['$v0','$v1']
    ARGUMENTREGISTER = ['$a0','$a1','$a2','$a3']
    TEMPORARYREGISTER = ['$t0','$t1','$t2','$t3','$t4','$t5','$t6','$t7','$t8','$t9']
    REGISTERS = {"$v0" : True,\
                 "$v1" : True,
                 "$a0" : True,
                 "$a1" : True,
                 "$a2" : True,
                 "$a3" : True,
                 "$t0" : True,
                 "$t1" : True,
                 "$t2" : True,
                 "$t3" : True,
                 "$t4" : True,
                 "$t5" : True,
                 "$t6" : True,
                 "$t7" : True,
                 "$t8" : True,
                 "$t9" : True,
                 "$s0" : True,
                 "$s1" : True,
                 "$s2" : True,
                 "$s3" : True,
                 "$s4" : True,
                 "$s5" : True,
                 "$s6" : True,
                 "$s7" : True,
                 "$k0" : True,
                 "$k1" : True,
                 "$gp" : True,
                 "$sp" : True,
                 "$fp" : True,
                 "$ra" : True
                 }

def getMipsTemporaryRegister(index):
    return MIPS.TEMPORARYREGISTER[index]

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
    def __init__(self, instruction):
        self.instruction = instruction
        self.successorList = []
        self.definedList = []
        self.usedList = []
        self.inVariables = []
        self.outVariables = []

dotdata = 0
functionList = []
currentFunc = ''
currentBlock = ''
labelBlockMap = dict()
interferanceGraphMap = dict()
graphColorMap = dict() # map to hold mapping of node and the associated color with it

funcToInterferenceGraphMap = dict()
funcToGraphColorMap = dict()


def prepareInterferanceGraphForStatement():
    '''
    This function prepares the intereferance graph for the given set of invariables set
    :return:
    '''
    for func in functionList:
        vertices = [] #set of unique vertices
        inVariableList = []
        interferanceGraphMap = dict()
        for block in func.blockList:
            for stmt in block.statementList:
                inVariableList.append(stmt.inVariables)
                for var in stmt.inVariables:
                    if var not in vertices:
                        vertices.append(var)
                        interferanceGraphMap[var] = [] # add an empty list corresponding to the key as var
                for var in stmt.outVariables:
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
                        listValue  = interferanceGraphMap[v]
                        if x not in listValue:
                            listValue.append(x)
        funcToInterferenceGraphMap[func] = interferanceGraphMap


def prepareInterferanceGraph():
    '''
    This function prepares the intereferance graph for the given set of invariables set
    :return:
    '''
    for func in functionList:
        vertices = [] #set of unique vertices
        inVariableList = []
        interferanceGraphMap = dict()
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
                        listValue  = interferanceGraphMap[v]
                        if x not in listValue:
                            listValue.append(x)
        funcToInterferenceGraphMap[func] = interferanceGraphMap

def colorTheGraph():
    for func in funcToInterferenceGraphMap:
        interferanceGraphMap = funcToInterferenceGraphMap[func]
        colorIndex = 0
        usedColor = []
        neighborColorList = []
        graphColorMap = dict() # map to hold mapping of node and the associated color with it

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
        funcToGraphColorMap[func] = graphColorMap



def translateToMips(filename):
    '''
    This function translates to MIPS code
    :return:
    '''
    for instr in absmc.instructionList:
        print instr.translateToMips()

    orig_stdout = sys.stdout
    filename = filename + '.asm'
    f = open(filename, 'w')
    # sys.stdout = f
    for instr in absmc.instructionList:
        print >>f , instr.translateToMips()
    # sys.stdout = orig_stdout
    f.close()

def processIntermediateCode():
    '''
    Main entry point to process the intermediate code
    :return:
    '''
    currentBlock = None
    currentFunc = None
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
            currentBlock.statementList.append(Statement(instr))
        if (not currentBlock is None):
            instr.block = currentBlock;
        instr.function = currentFunc;

    processBlocks() # call the below method
    analyzeLiveness() # analyze liveness for each block
    analyzeLivenessStatement() # analyze liveness for each statement
    prepareInterferanceGraphForStatement() # prepare the interferance graph and prepare the map interferanceGraphMap
    colorTheGraph() #color the graph

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
            for stmtindex, stmt in enumerate(currentBlock.statementList):
                if (stmtindex + 1 < len(currentBlock.statementList)): # for the next statement in the list
                    stmt.successorList.append(currentBlock.statementList[stmtindex + 1])
                if isinstance(stmt.instruction, absmc.Jmp_Instruction):
                    block = labelBlockMap[stmt.instruction.ra]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                    if block not in stmt.successorList:
                        stmt.successorList.append(block)  # Adding Block to statement successor list

                elif isinstance(stmt.instruction, absmc.Bz_Instruction):
                    block = labelBlockMap[stmt.instruction.rb]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                    if block not in stmt.successorList:
                        stmt.successorList.append(block)
                    if stmt.instruction.ra not in currentBlock.usedList and stmt.instruction.ra not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.ra)
                    stmt.usedList.append(stmt.instruction.ra) # Adding argument to statement used list

                elif isinstance(stmt.instruction, absmc.Bnz_Instruction):
                    block = labelBlockMap[stmt.instruction.rb]
                    if block not in currentBlock.successorList:
                        currentBlock.successorList.append(block)
                    if block not in stmt.successorList:
                        stmt.successorList.append(block)
                    if stmt.instruction.ra not in currentBlock.usedList and stmt.instruction.ra not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.instruction.ra)
                    stmt.usedList.append(stmt.instruction.ra)

                elif isinstance(stmt.instruction, absmc.DefUseInstruction) or isinstance(stmt.instruction, absmc.HloadInstruction):
                    if stmt.instruction.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.instruction.ra)
                    stmt.definedList.append(stmt.instruction.ra)
                    if stmt.instruction.rb not in currentBlock.usedList and stmt.instruction.rb not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.instruction.rb)
                    stmt.usedList.append(stmt.instruction.rb)
                    if stmt.instruction.rc not in currentBlock.usedList  and stmt.instruction.rb not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.instruction.rc)
                    stmt.usedList.append(stmt.instruction.rc)

                elif isinstance(stmt.instruction, absmc.Move_Immed_i_Instruction) or isinstance(stmt.instruction, absmc.Move_Immed_f_Instruction):
                    if stmt.instruction.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.instruction.ra)
                    stmt.definedList.append(stmt.instruction.ra)

                elif isinstance(stmt.instruction, absmc.Move_Instruction) or isinstance(stmt.instruction, absmc.HallocInstruction):
                    if stmt.instruction.ra not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.instruction.ra)
                    stmt.definedList.append(stmt.instruction.ra)
                    if stmt.instruction.rb not in currentBlock.usedList  and stmt.instruction.rb not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.instruction.rb)
                    stmt.usedList.append(stmt.instruction.rb)

                elif isinstance(stmt.instruction, absmc.HstoreInstruction):
                    if stmt.instruction.ra not in currentBlock.usedList and stmt.instruction.ra not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.instruction.ra)
                    stmt.usedList.append(stmt.instruction.ra)
                    if stmt.instruction.rb not in currentBlock.definedList:
                        currentBlock.definedList.append(stmt.instruction.rb)
                    stmt.definedList.append(stmt.instruction.rb)
                    if stmt.instruction.rc not in currentBlock.usedList and stmt.instruction.rc not in currentBlock.definedList:
                        currentBlock.usedList.append(stmt.instruction.rc)
                    stmt.usedList.append(stmt.instruction.rc)

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


def compareStmtList(oldStmtList, stmtList):
    for index in range(len(oldStmtList)):
        oldStmt = oldStmtList[index]
        stmt = oldStmtList[index]
        if not set(oldStmt.inVariables) == set(stmt.inVariables) or\
            not set(oldStmt.outVariables) == set(stmt.outVariables) :
            return False
    return True

def compareBlockList(oldBlockList, blockList):
    for index in range(len(oldBlockList)):
        oldBlock = oldBlockList[index]
        block = blockList[index]
        if not set(oldBlock.inVariables) == set(block.inVariables) or\
            not set(oldBlock.outVariables) == set(block.outVariables) :
            return False
    return True

def analyzeLivenessStatement():
    for function in functionList:
        iterationCount = 0
        for block in reversed(function.blockList):
            n = len(block.statementList)
            while (True):
                oldStmtList = block.statementList[:]
                i = n-1
                while i > -1:
                    currentStatement = block.statementList[i]
                    if iterationCount is 0:
                        currentStatement.inVariables = deriveInSet(currentStatement.usedList, currentStatement.definedList, currentStatement.definedList)
                        currentStatement.outVariables = currentStatement.definedList
                    else:
                        uniqueList = []
                        for inst in currentStatement.successorList:
                            if (isinstance(inst, Block)):
                                currentStatement.outVariables = appendUnique(uniqueList, inst.inVariables)
                            else:
                                currentStatement.outVariables = appendUnique(uniqueList, inst.inVariables)
                        currentStatement.inVariables = deriveInSet(currentStatement.usedList, currentStatement.outVariables,
                                                               currentStatement.definedList)
                    i = i - 1
                iterationCount = iterationCount + 1
                if compareStmtList(oldStmtList, block.statementList):
                    break


def analyzeLiveness():
    for function in functionList:
        iterationCount = 0
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
            for stmt in block.statementList:
                print "stmt.successorList:  -->",stmt.successorList
                print "stmt.usedList:  -->",stmt.usedList
                print "stmt.definedList:  -->",stmt.definedList
                print "stmt.inVariables:  -->",stmt.inVariables
                print "stmt.outVariables:  -->",stmt.outVariables
                print "- - - "
    print "--------Graph-----------------"
    for func in funcToInterferenceGraphMap:
        interferanceGraphMap = funcToInterferenceGraphMap[func]
        print "func --> ", func
        for x in interferanceGraphMap:
            print x, "-->", interferanceGraphMap[x]

    print "--------Graph Coloring-----------------"
    for func in funcToGraphColorMap:
        graphColorMap = funcToGraphColorMap[func]
        print "func --> ", func
        for key in graphColorMap:
            print key,"-->",graphColorMap[key]

def printMap():
    print "----MAP--------------------"
    for key in labelBlockMap:
        print "key: ", key, " value: ", labelBlockMap[key]
