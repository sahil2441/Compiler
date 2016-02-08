'''Simple Calculator'''
import re
from validateInput import Validate
from constants import KEYWORD
class SimpleCalculator(object):
    
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
                        
if __name__ == "__main__":
    sc = SimpleCalculator()
    #iText = sc.getUserInput()
    iText = "x = ~10;   y = - x 1;   z = * x * y + x y;    "
    #iText = "x = 10;   y = - x 1;"
    validate =Validate()
    #validate.validateText(iText)
    sc.compile(iText)

    
    
        
        