from stack import Stack
from constants import KEYWORD
from textParser import TextScanner
import re
class SSM(object):
        
    def __init__(self):
        self.labelPointers = dict()
    def userSSMInput(self):
        instText = ''
        while True:
            line = raw_input()
            if line =='':
                break
            instText += line + '\n'        
        return instText
        
        
        '''
        1. Make sure each element is valid in the list
        2. Make sure each instruction is valid ( making pair of keyword and argument)
        3. Track what is the scope of the label(i and j pointers in the list)
        4. Track jmp/jz/jnz to their corresponding labels
        5. Execute the instructions
        
        6. Before parsing, we also need to extract the labels and store in a map< Label, Index>, where index is
            the index in the input arraylist.
            (Labels are separated by semi colons)
        
    '''
    
    def prepareLabelPointers(self, iArray):
        length = len(iArray)
        index = 0
        while index < length:
            element = iArray[index]
            if re.match(r"^[a-zA-Z][a-zA-Z0-9_]+:$", element):
                self.labelPointers[element] = index
            index += 1 
    

    def processInstructions(self, instructions):
        """
        This function processes the instruction list as received by user from commond line
        """
        #flag to keep check whether we have completed the instructions succesfully
        flag = 0    
        index = 0
        # index to keep track of elements in iArray
    
        # define new stack for program
        stack = Stack()    
        register = dict()        
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
            elif (elt == KEYWORD.JMP):
                label = instructions[index + 1]
                index = self.labelPointers[label+':']

            elif (elt == KEYWORD.IADD):            
                stack.stackAdd()  # 
                index += 1 
            elif (elt == KEYWORD.ISUB):            
                stack.stackSubtract()  # 
                index += 1                       
            elif (elt == KEYWORD.IMUL):            
                stack.stackMultiply()  # 
                index += 1
            elif (elt == KEYWORD.IDIV):            
                stack.stackQuotient()  # 
                index += 1        
            elif (elt == KEYWORD.IMOD):            
                stack.stackRemainder()  # 
                index += 1  
            elif (elt == KEYWORD.DUP):            
                stack.stackDup()  # 
                index += 1
            elif (elt == KEYWORD.SWAP):            
                stack.stackSwap()  # 
                index += 1        
            elif (elt == KEYWORD.LOAD):            
                stack.stackLoad(register)  # 
                index += 1         
            elif (elt == KEYWORD.STORE):            
                stack.store(register)  # 
                index += 1   
            elif (elt == KEYWORD.POP):
                stack.pop() 
                index += 1
            else:
                index += 1
        # Check if instructions were processed successfully; if not flag will be =0
        if(flag):
            print stack.pop()
        else:
            print "Exception Raised: Due to fault in input"

if __name__ == "__main__":
    ssm = SSM() 
    # get input from the user
    instructions = ssm.userSSMInput()
    txtScan = TextScanner()

    #SANITIZATION of Instructions
    # remove comments
    instructions = txtScan.removeComment(instructions)

    # scan text for proper form
    txtScan.scanTextForSyntaxAndSemantics(instructions)
    iArray = instructions.split()

    # prepare pointers for label indexes
    ssm.prepareLabelPointers(iArray)

    # Finally Run the Code
    ssm.processInstructions(iArray)
    