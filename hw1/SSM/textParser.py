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
            # If '#' is encountered, then escape the remaining line from the input(till newline)
            if (nextChar == '#'):
                while nextChar != '\n' and index < length - 1:
                    index += 1
                    nextChar = instText[index]
            else:
                noCommentText += nextChar
            index += 1            
        return noCommentText     
        
    
    def areElementsValid(self, instList):
        '''
        Main method to scan and analyze the code for compilation
        '''
        index = 0
        length = len(instList)
        labelVerifiedDict = dict()
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
            # Check for label if the current element has ':' in the string form
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
            # If all others pass, then check if element is valid instruction or label            
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


    def scanTextForSyntaxAndSemantics(self, instText):
        """ If the input string passes this function then it's a valid input and therefore can be
        evaluated. This function checks whether it's a valid input.
        :param instText:
        :return:
        """

        nextChar = ''
        length = len(instText)
        currentText = ''
        prevText = ''
        index = 0
        labelList = list()
        labelVerifiedDict = dict()

        while index < length:
            nextChar = instText[index]    

            # If we ever encounter a symbol which is not in the character set, then input is wrong
            if not re.match(r"[a-z0-9:_\s|-]", nextChar):
                raise CustomException("Unsupported instruction found")        

            if re.match(r"\s", nextChar):
                if currentText != '':
                    # If the current text matches an integer
                    if re.match(r"^-?[0-9]+$", currentText):
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
