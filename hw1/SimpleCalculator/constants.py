class KEYWORD(object):
    keyList = ['ildc', 'iadd', 'isub','imul','idiv','imod','pop','dup','swap','jz','jnz','jmp','load','store']
    keysWithIntegerArguments = ['ildc']
    keysWithNoArguments = ['iadd','isub','imul','idiv','imod','pop','dup','swap','load','store']
    keysWithLabelArguments=['jz','jnz','jmp']
    ILDC, IADD, ISUB, IMUL, IDIV,\
    IMOD, POP, DUP, SWAP, JZ, JNZ, \
    JMP, LOAD, STORE = keyList
    
    ACTIONLIST = ['+','-','/','%','*']
    PLUS, MINUS, DIVIDE, MOD, MULTIPLY = ACTIONLIST
    
    
        
    