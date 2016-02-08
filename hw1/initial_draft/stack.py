from exception import CustomException
'''
Stack class to support operations on the stack object for Simple Stack Machine instructions
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
        val = register[a]
        self.push(val)

    # store: Treat the second-to-top element on the stack as an address a, and the top-most element as an integer i.
    # Pop the top two elements from stack. The cell at address a in the store is updated with integer i.
    def store(self, register):
        i = self.pop()
        a = self.pop()
        register[a] = i
    
                    
    def __str__(self):
        return '['+', '.join([str(i) for i in self.stackValues])+']'
        
if __name__ == "__main__":
    s = Stack()
    try:
        print s.stackAdd()
    except Exception, e:
        print str(e)