class KEYWORD(object):

    '''A class to store all the constants and instruction keywords'''
    
    keyList = ['ildc', 'iadd', 'isub','imul','idiv','imod','pop','dup','swap','jz','jnz','jmp','load','store']
    keysWithIntegerArguments = ['ildc']
    keysWithNoArguments = ['iadd','isub','imul','idiv','imod','pop','dup','swap','load','store']
    keysWithLabelArguments=['jz','jnz','jmp']
    
    ILDC, IADD, ISUB, IMUL, IDIV,\
    IMOD, POP, DUP, SWAP, JZ, JNZ, \
    JMP, LOAD, STORE = keyList
    
    ACTIONLIST = ['+','-','/','%','*']
    
    PLUS, MINUS, DIVIDE, MOD, MULTIPLY = ACTIONLIST

class CustomException(Exception):
    
    '''A custom Exception class for optional flexibility'''
    
    def __init___(self,args):
        self.args = args
        
class Stack(object):

    '''Stack class to support operations on the stack object for Simple Stack Machine instructions'''    
    
    def __init__(self):
        self.stackValues=[]
    
    # add element to top of stack
    def push(self,element):
        self.stackValues.append(element)
    
    # remove element from top of stack
    def pop(self):
        topValue = None
        stackLength = len(self.stackValues)
        if (stackLength > 0):
            topValue = self.stackValues[stackLength - 1]
            del self.stackValues[-1]
        else:
            raise CustomException('Stack is Empty')
        return topValue
 
    # pop top two elements from stack, add them, and push their sum to the top of stack
    def stackAdd(self):
        a = self.pop()
        b = self.pop()
        val = a + b
        self.push(val)
        return val
        
    # pop top two elements from stack, subtract first popped element from the second popped element, and push their difference to top of stack
    def stackSubtract(self):
        a = self.pop()
        b = self.pop()
        val = b - a
        self.push(val)
        return val
    
    # pop top two elements from stack, divide second popped element from first popped element, and push the quotient to top of stack
    def stackQuotient(self):
        a = self.pop()
        b = self.pop()
        val = b/a
        self.push(val)
        return val
    
    # pop top two elements from stack, perform modulo using first popped element on second popped element, and push the remainder to top of stack
    def stackRemainder(self):
        a = self.pop()
        b = self.pop()
        val = b%a        
        self.push(val)
        return val
    
    # pop top two elements from stack, and push their product to top of stack
    def stackMultiply(self):
        a = self.pop()
        b = self.pop()
        val = a*b
        self.push(val)
        return val
        
    # pop top element from stack and push the element twice into the stack
    def stackDup(self):
        a = self.pop()
        self.push(a)
        self.push(a)
        
    # pop top two elements from stack and while pushing back to stack swap their order in the stack
    def stackSwap(self):
        a = self.pop()
        b = self.pop()
        self.push(a)
        self.push(b)
        
    # return top value from the stack    
    def getTop(self):
        return self.stackValues[-1]

    # load: the top-most element of the stack is the address in store, say a.
    # This instruction pops the top-most element, and pushes the value at address a in store.
    def stackLoad(self, register):
        a = self.pop()
        if register.has_key(a):
            val = register[a]
        else:
            raise CustomException("Compilation Error: invalid load address")
        self.push(val)

    # store: Treat the second-to-top element on the stack as an address a, and the top-most element as an integer i.
    # Pop the top two elements from stack. The cell at address a in the store is updated with integer i.
    def store(self, register):
        i = self.pop()
        a = self.pop()
        register[a] = i
    
    # print stack elements                
    def __str__(self):
        return '['+', '.join([str(i) for i in self.stackValues])+']'


class TextScanner(object):

    ''' This class consists of methods used to sanitize the input provided by user.'''

    pass          
          
    # We need to remove comments from the input text
    def removeComment(self, instText):
        nextChar = ''
        index = 0
        noCommentText = ''
        length = len(instText)
        if re.match(r"\s*$",instText):          # If the input is only having white spaces or empty string
            raise CustomException("No instructions found")

        while index < length:
            nextChar = instText[index]
            # If '#' is encountered, then escape the remaining line from the input(till newline)
            if (nextChar == '#'):
                while nextChar != '\n' and index < length - 1:
                    index += 1
                    nextChar = instText[index]
            else:
                noCommentText += nextChar
            index += 1            
        return noCommentText     
        
    
    #Main method to scan and analyze the code text for syntax and semantics
    def areElementsValid(self, instList):  # instList is an array of individual elements extracted from the code text with no whitespaces
        index = 0
        length = len(instList)
        labelVerifiedDict = dict()  # a dictionary object used to track labels used in the code text
        
        #loop over each element of the instruction list and validate its presence
        while index < length:
            element = instList[index]      
            # If the current element is an integer, then previous element should be a key(ildc) with integer argument
            if re.match(r"^-?[0-9]+$", element):
                if index >= 1:
                    prevElem = instList[index - 1]
                    if prevElem not in KEYWORD.keysWithIntegerArguments:
                        raise CustomException('Compilation Error: Bad instruction - Integer provided without supporting command')      
            # If the current element is a jump key, then the next element should be a label
            elif element in KEYWORD.keysWithLabelArguments:
                if (index + 1 < length):
                    nextElem = instList[index + 1]
                    if nextElem in KEYWORD.keyList:
                        raise CustomException('Compilation Error: Invalid Argument- Reserved Keyword cannot be used as label- '+nextElem)       
                    if not labelVerifiedDict.has_key(nextElem):
                        labelVerifiedDict[nextElem] = False                 
                else:
                    raise CustomException("Compilation Error: Missing label")
            # If the current element is a key requiring integer argument, then the next element should be an integer
            elif element in KEYWORD.keysWithIntegerArguments:
                if (index + 1 < length):
                    nextElem = instList[index + 1]
                    if not re.match(r"^-?[0-9]+$", nextElem):
                        raise CustomException("Compilation Error: Bad instruction - Integer argument expected")
                else:
                    raise CustomException("Compilation Error: Missing Argument")
            # Check for label if the current element has ':' in the string form.
            # If the current element is ':' then the previous element should be a valid label
            elif ':' in element:
                if re.match(r"^:$", element):
                    if index > 0:
                        prevElem = instList[index - 1]
                        if prevElem in KEYWORD.keyList:
                            raise CustomException('Compilation Error: Invalid Argument- Reserved Keyword cannot be used as label- ' + element)       
                        labelVerifiedDict[prevElem] = True
                    else:
                        raise CustomException("Compilation Error: Missing Label name")
                else:
                    element = element[0:-1]
                    if element in KEYWORD.keyList:
                        raise CustomException('Compilation Error: Invalid Argument- Reserved Keyword cannot be used as label- ' + element)       
                    else:
                        labelVerifiedDict[element] = True        
            # If all others pass, then check if element is valid instruction or label else raise an exception           
            elif not element in KEYWORD.keyList and not labelVerifiedDict.has_key(element):
                raiseError = True
                if not labelVerifiedDict.has_key(element):
                    if index + 1 < length:
                        nextElem = instList[index + 1]                        
                        if re.match(r"^:$", nextElem):
                            labelVerifiedDict[element] = True
                            raiseError = False
                if raiseError:
                    raise CustomException('Compilation Error : Unsupported instruction found- '+ element)            
            index += 1
        for key, value in labelVerifiedDict.iteritems():    
            if not value:
                raise CustomException('Compilation Error: Undefined Label found- '+ key)                        
        
import re
class SSM(object):
        
    ''' Main class which will invoke the program to validate and process the input SSM code    '''
    
    def __init__(self):
        self.labelPointers = dict()
    
    # Get user input from stdin
    def userSSMInput(self):
        instText = ''
        while True:
            line = raw_input()
            if line =='':
                break
            instText += line + '\n'        
        return instText                
    
    # The function prepares pointers for each label in the instruction code when evaluating the input code
    def prepareLabelPointers(self, iArray):
        length = len(iArray)
        index = 0
        while index < length:
            element = iArray[index]
            if re.match(r"^[a-zA-Z][a-zA-Z0-9_]*\s*:$", element) or re.match(r"^:$",element):
                if re.match(r"^:$",element):
                    prevElement = iArray[index - 1]
                    self.labelPointers[prevElement + element] = index
                else:
                    self.labelPointers[element] = index
            index += 1 
    

    # This function processes the instruction list as received by user from commond line
    def processInstructions(self, instructions):

        flag = 0    #flag to keep check whether we have completed the instructions succesfully
        index = 0     # index to keep track of elements in iArray
    
        stack = Stack()    # define new stack for program
        register = dict()  # register to enable storing and loading of values during runtime
            
        while (True):
            if (index == len(instructions)):
                # this flag indicates that instructions were processed successfully
                flag=1
                break    
            elt = instructions[index]
            if (elt == KEYWORD.ILDC):
                stack.push(int(instructions[index + 1]))  # just made this as parse int
                index += 2
            elif (elt == KEYWORD.JZ):                     # jump Zero
                stackTop = stack.pop()
                if (stackTop == 0):                       # if the top most element is 0 in the stack, then move instruction index to the label
                    label = instructions[index + 1]    
                    index = self.labelPointers[label+':']
                else:
                    index += 2                             # If the top element is not 0 in the stack , proceed to next instruction 
            elif (elt == KEYWORD.JNZ):                    # jump Not Zero
                stackTop = stack.pop()    
                if (stackTop != 0):                       # if the top most element is NOT 0 in the stack, then move index to the label
                    label = instructions[index + 1]    
                    index = self.labelPointers[label+':']
                else:
                    index += 2                            # If the top element is equal to 0 in the stack , proceed to next instruction 
            elif (elt == KEYWORD.JMP):                    # Jump to the label specified
                label = instructions[index + 1]
                index = self.labelPointers[label+':']
            elif (elt == KEYWORD.IADD):                   # invoke instruction to add from stack
                stack.stackAdd()  
                index += 1 
            elif (elt == KEYWORD.ISUB):                   # invoke instruction to subtract from stack  
                stack.stackSubtract()  
                index += 1                       
            elif (elt == KEYWORD.IMUL):                   # invoke instruction to multiply from stack 
                stack.stackMultiply()  
                index += 1
            elif (elt == KEYWORD.IDIV):                   # invoke instruction to divide from stack
                stack.stackQuotient()   
                index += 1        
            elif (elt == KEYWORD.IMOD):                   # invoke instruction to get modulus from stack           
                stack.stackRemainder()   
                index += 1  
            elif (elt == KEYWORD.DUP):                    # invoke instruction to duplicate top value on stack         
                stack.stackDup()   
                index += 1
            elif (elt == KEYWORD.SWAP):                   # invoke instruction to swap top two values on stack
                stack.stackSwap()   
                index += 1        
            elif (elt == KEYWORD.LOAD):                   # invoke instruction to load stored value from register using stack
                stack.stackLoad(register)   
                index += 1         
            elif (elt == KEYWORD.STORE):                  # invoke instruction to store value into register        
                stack.store(register)   
                index += 1   
            elif (elt == KEYWORD.POP):                    # invoke instruction to pop value from stack
                stack.pop() 
                index += 1
            else:
                index += 1
        # Check if instructions were processed successfully; if not flag will be =0
        if (flag):
            print stack.pop()
        else:
            print "Exception Raised: Due to fault in input"

# MAIN method to execute the code
if __name__ == "__main__":
    ssm = SSM() 
    instructions = ssm.userSSMInput()     # get input from the user
    #SANITIZATION of Instructions    
    txtScan = TextScanner()
    instructions = txtScan.removeComment(instructions)  # remove comments
    iArray = instructions.split()        # split instructions into elements with no whitespaces
    txtScan.areElementsValid(iArray)     # scan text for proper form
    ssm.prepareLabelPointers(iArray)     # prepare pointers for label indexes
    ssm.processInstructions(iArray)      # Finally Run the Code 
    
'''
TEST CASES:
     
     a
     ildc
     ildc 10
     iadd
     store
     load
     :
     here:
     here :
     here: ildc 10 ildc 20 iadd
     ildc 10 # load value 10
     ildc 10 ildc 0 jz there here : ildc 44 there : ildc 10 imul               
'''
    
        
    