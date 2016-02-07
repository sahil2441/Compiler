from exception import CustomException
from constants import KEYWORD
import re
'''
This class consists of methods used to sanitize the input provided by user.
'''
class TextScanner(object):
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
            if (nextChar == '#'):              # If '#' is encountered, then escape the remaining line from the input(till newline)
                while nextChar != '\n' and index < length:
                    index += 1
                    nextChar = instText[index]
            else:
                noCommentText += nextChar
            index += 1            
        return noCommentText     
        
    def scanTextForSyntaxAndSemantics(self, instText):
        nextChar = ''        
        length = len(instText)
        currentText = ''
        prevText = ''
        index = 0
        labelList = list()
        labelVerifiedDict = dict()
        while index < length:
            nextChar = instText[index]    
            if not re.match(r"[a-z0-9:_\s|-]", nextChar):                      # If we ever encounter a symbol which is not in the character set, then input is wrong
                raise CustomException("Unsupported instruction found")        
            if re.match(r"\s", nextChar):                 
                if currentText != '':  
                    if re.match(r"^-?[0-9]+$", currentText):                   # If the current text matches an integer
                        if prevText == '' or (prevText != '' and not prevText in KEYWORD.keysWithIntegerArguments):
                            raise CustomException('Bad instruction - Integer provided without supporting command')
                    elif prevText != '' and prevText in KEYWORD.keyList:
                        if prevText in KEYWORD.keysWithIntegerArguments and not re.match(r"^-?[0-9]+$", currentText):
                            raise CustomException("Bad instruction - Integer argument expected")   
                        elif prevText in KEYWORD.keysWithLabelArguments:                        
                            if not currentText in labelList:
                                if currentText in KEYWORD.keyList:
                                    raise CustomException('Invalid Argument- Reserved Keyword cannot be used as label- '+currentText)
                                labelList.append(currentText)
                                labelVerifiedDict[currentText] = False                                            
                    elif not currentText in KEYWORD.keyList and not currentText in labelList:
                        raise CustomException('Unsupported instruction found- '+ currentText )
                    prevText = currentText          
                currentText = ''
            elif nextChar == ':':
                currentText = currentText.strip()
                if re.search(r"^[a-z][a-z0-9]*$", currentText):
                    if not currentText in labelList:
                        if currentText in KEYWORD.keyList:
                            raise CustomException('Invalid Argument- Reserved Keyword cannot be used as label- '+currentText)
                        labelList.append(currentText)
                    elif labelVerifiedDict[currentText]:
                        raise CustomException('2 instructions cannot have the same label')
                    labelVerifiedDict[currentText] = True
                    currentText = ''
                else:
                    raise CustomException('Invalid label name construction- ' + currentText)
            else:                
                currentText += nextChar
            index += 1     
        for key, value in labelVerifiedDict.iteritems():    
            if not value:
                raise CustomException('Undefined Label found- '+ key)
        return labelList                        
            
    '''def areElementsValid(self, instList, labelList):
        index = 0
        length = len(instList)
        while index < length:
            element = instList[index]            
            if element in [KEYWORD.JMP, KEYWORD.JZ, KEYWORD.JNZ]:
                if (index + 1 < length):
                    nextElem = instList[index+1]
                    if not nextElem in labelList:
                        raise CustomException("Invalid label found")
            index += 1'''
