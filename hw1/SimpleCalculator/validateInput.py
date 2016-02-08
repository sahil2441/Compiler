"This class validates the input for Simple calculator"
from exception import CustomException
from stack import Stack
import re

class Validate(object):
    def validateText(self, input):
        if not re.match(r"[a-z0-9_;=+ - *\s]", input):
            raise CustomException("Unsupported instruction found")

        # split input based on semi colon so tht we have each statement
        input=input.strip()
        mylist = input.split(';')

        if not self.analyzeStatement(mylist):
            raise CustomException("Unsupported instruction found")



        return input

    def analyzeStatement(self,mylist):
        """
        This method analyses each statement passed to it in a list.
        1. Each statement must have only one =
        2. Character(String) before the '=' must  be a variable
        3. String after '=' must be a valid prefix expression
        4. Create a stack that holds each character in right expression.
            Pop the stack till it's empty and check if this variable has been initialized.

        :return: True/False
        """
        # set to hold characters
        mySet=set()

        for statement in mylist:
            if len(statement)<1:
                continue

            statement=statement.strip()
            if statement.count('=') is not 1:
                return False

            index =statement.index('=')
            left=statement[:index]
            right=statement[index+1:]

            if not self.isValidVariable(left):
                return False
            if not self.isValidPrefixExpression(right):
                return False
            if not self.isVariablesInitialized(mySet,right):
                return False

            #      Enter the current variable in the map/set.
            mySet.add(left)

        return True

    def isVariablesInitialized(self,set,right):
        """
        Confirm that each variable has been initialized and hence exists in map.
        :return: Boolean
        """
        right=right.strip()
        list=right.split(' ');

        index=len(list)-1

        for element in reversed(list):

            if self.isInt(element):
              continue

            elif(self.isValidVariable(element) and not set.__contains__(element)):
                return False
        return True

    def isValidVariable(self,left):
        """
        Validate a variable:
        Variables are identifiers, represented by sequences of alphabetic characters or numeric characters
        or underscore ("_"), beginning with an alphabetic character.

        :return: True/False
        """
        left=left.strip()
        pattern = '^\w+$'

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
        list=right.split(' ');
        n=len(list)

        # base case
        if n<1:
            return True

        stack=Stack()
        index=n-1

        # set of all operations
        mySet=set()
        mySet.add('+')
        mySet.add('%')
        mySet.add('/')
        mySet.add('*')
        mySet.add('-')


        while(index>=0):
            element=list[index]
            if self.isInt(element):
                stack.push(element)

            elif self.isValidVariable(element):
                stack.push(self,element)

            elif mySet.__contains__(element):
                # equivalent to evaluating an expression and pushing the result
                stack.pop()

            index-=1

        stack.pop()
        return stack.stackValues == []

    def isInt(self,x):
        try:
            int(x)
            return True
        except ValueError:
            return False




