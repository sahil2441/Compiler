'''Simple Calculator'''
import re
from exception import CustomException
from validateInput import Validate

class SimpleCalculator(object):
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
        
if __name__ == "__main__":
    sc = SimpleCalculator()
    # iText = sc.getUserInput()
    iText = "x = 10;"

    validate =Validate()
    validate.validateText(iText)

    print iText

    
    
        
        