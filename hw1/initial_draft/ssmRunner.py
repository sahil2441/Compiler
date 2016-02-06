from stack import Stack
from constants import KEYWORD
from label import Label
class SSM(object):
        
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
        
        here:
            here2:
                here3:    
        there:
            jmp here
            
        ['ildc',
        '20',   
        'ildc',
        '5',
        'here:',
        'ildc',
        '1',
        'isub',
        'dup',
        'jz',
        'there',
        'swap',
        'ildc',
        '10',
        'iadd',
        'swap',
        'jmp',
        'here',
        'there:',
        'pop']
        
        '''        

    def processInstructions(self,instructions):
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
                if (index + 1 >= len(instructions)):
                    break
                stack.push(int(instructions[index + 1]))  # just made this as parse int
                index += 2
            elif (elt == KEYWORD.JZ):       # jump Zero
                # first check if the top most element is 0 in the stack
                # if the element is not 0, proceed to next instruction                
                if (index + 1 >= len(instructions)):
                    break    
                stackTop = stack.pop()    
                label = (instructions[index + 1])    
                if (stackTop != 0):
                    index += 2  # If the top element is not 0 in the stack 
            elif (elt == KEYWORD.JNZ):       # jump Not Zero
                # first check if the top most element is 0 in the stack
                # if the element is not 0, proceed to next instruction                
                if (index + 1 >= len(instructions)):
                    break    
                label = (instructions[index + 1])    
                index += 2  # If the top element is 0 in the stack       
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
        # Check if instructions were processed successfully; if not flag will be =0
        if(flag):
            print stack.pop()
        else:
            print "Exception Raised: Due to fault in input"


if __name__ == "__main__":
    ssm = SSM()
    instructions = ssm.userSSMInput()
    iArray = instructions.split()
    print iArray

    # TODO parse array to store labels into map -- Label are identified by statements terminating with a colon

    # TODO check and match whether each instruction belong to the given list of valid instructions -- or it could
    # belong to the set of labels

    ssm.processInstructions(iArray)


