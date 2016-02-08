"This class validates the input for Simple calculator"
from exception import CustomException
from stack import Stack
import re

class Validate(object):
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
        try:
            int(x)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    iText = "x = * * 10 20 * 20 ~30;"
            # "y = - x 1;   " \
            # "z = * x * y + x y;"
    val=Validate()
    if Validate.validateText(val,iText):
        print iText


