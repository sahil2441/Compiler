''' main python function to put together parser/lexer '''
from ply import *
import decaflexer
import decafparser

def getDataFromFile(filename):
    file=open(filename)
    data = file.read()
    file.close()
    return data

if __name__ == '__main__':
    filename = 'test_case_2.txt'#raw_input('Enter file name: ') # user must input file name
    data = getDataFromFile(filename)
    decaflexer.printTokens(data) # print tokens using lexer
    try:
        decafparser.parse(data) # parse program using parser
        print 'Yes'
    except:
        print 'The program has syntax errors'


