'''
This class mimics store instruction
'''
class Register(object):
    def __init__(self):
        self.register = dict()
    
    def push(self, address, value):
        self.register[address] = value
    
    
        