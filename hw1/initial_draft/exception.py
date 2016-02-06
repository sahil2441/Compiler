from constants import CONSTANT
class CustomException(Exception):
    def __init___(self,args):
        self.args = args
    
