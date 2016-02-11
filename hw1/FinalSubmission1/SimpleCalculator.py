import re
class KEYWORD(object):
    
    ''' Class containing all the constants and functional keywords''' 
    
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
    
    ''' Custom exception class for optional flexibility'''
    
    def __init___(self,args):
        self.args = args

'''
Stack class to support operations on the stack object used during input validation
'''
class Stack(object):
    
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
         
    # return top value from the stack    
    def getTop(self):
        return self.stackValues[-1]
                    
    def __str__(self):
        return '['+', '.join([str(i) for i in self.stackValues])+']'

class Validate(object):
    
    ''' Class having functions which validate the input code '''
    
    # Method to validate text elements
    def validateText(self, input):
        if not re.match(r"[a-z0-9_;=+ - *~\s]", input):
            raise CustomException("Unsupported instruction found")

        if not self.analyzeStatement(input):
            raise CustomException("Unsupported instruction found")

        return input

    def analyzeStatement(self,input):
        """
        This method analyses each statement passed to it in a list.
        1. Each statement must have only one =
        2. Character(String) before the '=' must  be a variable
        3. String after '=' must be a valid prefix expression
        4. Create a stack that holds each character in right expression.
            Pop the stack till it's empty and check if this variable has been initialized.

        :return: True/False
        """
         # split input based on semi colon so tht we have each statement
        input=input.strip()

        if len(input)<1:
            return False
        if not input.endswith(';'):
            return False

        input=input[:len(input)-1]
        mylist = input.split(';')

        # set to hold characters
        mySet=set()

        for statement in mylist:
            # TODO: check ;; <--case
            if len(statement)<1:
                return False

            statement=statement.strip()
            # Step 1
            if statement.count('=') is not 1:
                return False

            # Break about '='
            index =statement.index('=')
            left=statement[:index].strip()
            right=statement[index+1:].strip()

            if not self.isValidVariable(left):
                raise CustomException("Not a valid variable on LHS")
            if not self.isValidPrefixExpression(right):
                raise CustomException("Not a valid prefix expression")
            if not self.isVariablesInitialized(mySet,right):
                raise CustomException("Variables not initialized properly")

            #      Enter the current variable in the map/set.
            mySet.add(left)
            #     Also add the neagtive of current variable
            mySet.add('~'+left)


        return True

    def isVariablesInitialized(self, variableSet, right):
        """
        Confirm that each variable has been initialized and hence exists in map.
        :return: Boolean
        """
        right=right.strip()
        list=right.split();

        index=len(list)-1

        for element in reversed(list):
            if self.isInt(element):
              continue

            elif(self.isValidVariable(element) and not variableSet.__contains__(element)):
                return False
        return True

    def isValidVariable(self,left):
        """
        Validate a variable:
        Variables are identifiers, represented by sequences of alphabetic characters or numeric characters
        or underscore ("_"), beginning with an alphabetic character.

        :return: True/False
        """
        if len(left)<1:
            return False
        if left[0] is '~':
            left=left[1:]

        left=left.strip()
        pattern = '^[A-Za-z0-9_]+$'

        if not left[0].isalpha():
            return False

        if not re.match(pattern,left):
            return False

        return True


    def isValidPrefixExpression(self,right):
        """
        Returns true if right is a valid prefix expression.
        Create a stack and keep adding elements using operations.
        pop the last element and return true if stack is empty
        :param right:
        :return: Boolean
        """
        right=right.strip()
        list=right.split();
        n=len(list)

        # base case
        if n<1:
            return True

        stack=Stack()

        # set of all operations
        mySet=set()
        mySet.add('+')
        mySet.add('%')
        mySet.add('/')
        mySet.add('*')
        mySet.add('-')

        # + * 4 3 - 2 3

        # traverse list from right to left
        for element in reversed(list):
            if self.isInt(element):
                stack.push(element)

            elif self.isValidVariable(element):
                stack.push(element)

            elif mySet.__contains__(element):
                # equivalent to evaluating an expression and pushing the result
                stack.pop()

        stack.pop()
        return stack.stackValues == []

    def isInt(self,x):
        # if first character is ~ , then remove it
        if x[0] is '~':
            x=x[1:]
        pattern = '^[0-9]+$'
        if not re.match(pattern,x):
            return False

        try:
            int(x)
            return True
        except ValueError:
            return False

    
class SimpleCalculator(object):
    
    ''' Class which has methods to get user input, and compile the input code into SSM form '''     
    
    def __init__(self):
        self.variableRegisterMap = dict()
        
    def getUserInput(self):
        instText = ''
        while True:
            line = raw_input()
            if line =='':
                break
            instText += line + '\n'        
        return instText
    
    '''
        x = 10;
        y = - x 1;
        z = * x * y + x y;

        Points to be noted to validate input
        1. Make sure all characters are valid in input
            Acceptable char are: alphanumeric, _ ; = + - *
        2. Split text based on ';'
        3. Split text based on '='
        4. LHS should a valid variable construction( alphanumeric, only one word...)
        5. RHS should be a valid expression construction
        6. Maintain map for initialized variables. If uninialized variable found then throw exception 
    '''

    def ILDC_INSTRUCTION(self, val):
        return KEYWORD.ILDC + ' ' + str(val)
    
    def compile(self, iText):
        statements = iText.split(';')[0:-1]
        registerCount = 0
        instructionList = list()
        for statement in statements:
            components = statement.split('=')       
            lhs = components[0].strip()
            # Check if the register address is present for LHS variable, if not, create a new register address
            if not self.variableRegisterMap.has_key(lhs):
                self.variableRegisterMap[lhs] = registerCount
                registerCount += 1
            variableRegister = self.variableRegisterMap[lhs]
            # for each statement first instruction will load the register address where the variable value will be stored
            instructionList.append(self.ILDC_INSTRUCTION(variableRegister))
            
            # Manipulating RHS expression for compilation to instructions
            rhs = components[1]
            rhsExpressions = rhs.split()
            lenRHS = len(rhsExpressions)
            index = 0        
            # Scan the RHS from left to right to insert variable/constants instruction set    
            while index < lenRHS:
                expr = rhsExpressions[index]
                if re.match(r"^~?[0-9]+$", expr):
                    if '~' in expr:
                        expr = expr.replace('~', '-')
                    instructionList.append(self.ILDC_INSTRUCTION(expr))
                elif re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", expr):
                    variableRegister = self.variableRegisterMap[expr]
                    instructionList.append(self.ILDC_INSTRUCTION(variableRegister)+'\n'+KEYWORD.LOAD)
                index += 1   
            
            #Now scan the rhs expression( from Right to Left) to insert proper action instructions
            index = lenRHS - 1            
            while index >= 0:
                expr = rhsExpressions[index]            
                if not expr in KEYWORD.ACTIONLIST: 
                    index -= 1                       
                    continue                                        
                if expr in KEYWORD.PLUS:                    
                    instructionList.append(KEYWORD.IADD)
                elif expr == KEYWORD.MINUS:
                    instructionList.append(KEYWORD.ISUB)                      
                elif expr == KEYWORD.MULTIPLY:
                    instructionList.append(KEYWORD.IMUL)                    
                elif expr == KEYWORD.MOD:
                    instructionList.append(KEYWORD.IMOD)
                elif expr == KEYWORD.DIVIDE:
                    instructionList.append(KEYWORD.IDIV)                                           
                index -= 1  
            instructionList.append(KEYWORD.STORE)                           
        for i in instructionList:
            print i

def fetchTestCases():
    """
    Function to generate a list of test cases.
    :return:
    """
    list=[
    'x ',
    '= ',
    '-1 ',
    '~1 ',
    ';   ',
    'x = -1; ',
    'x = ~1; ',
    'x = x + 1; ',
    'x = + x 1; ',
    'x = x 1 +; ',
    'x = - ~x ~1 ',
    'x = - ~x ~1; ',
    'x = * 1 ~x; ',
    'x = * 1 6; ',
    'x = 10; y = x;',
    'x = 1; y = ~x; ',
    'x = 1; y = * x x;',
    'x = -1;y = 5;x = x  + y;']

    return list


def test():
    list=fetchTestCases()
    validate =Validate()
    sc = SimpleCalculator()

    # Test the first part of HW -- Validate
    for input in list:
        try:
            validate.validateText(input)
            print "Validating Input: "+ input+ " PASSED"
        except Exception:
            print "Validating Input: "+ input+" FAILED"

    print '\n'

    # Test the second part of HW -- Compile
    for input in list:
        try:
            sc.compile(input)
            print "Compiling Input: "+ input+ " PASSED"
        except Exception:
            print "Compiling Input: "+ input+" FAILED"





if __name__ == "__main__":

    # TODO: This needs to uncommented before submission

    # sc = SimpleCalculator()
    #iText = sc.getUserInput()
    # validate =Validate()
    # validate.validateText(iText)
    # sc.compile(iText)

    # TODO: Comment this before submission
    test()