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
    filename = 'intList.txt'#raw_input('Enter file name: ') # user must input file name
    data = getDataFromFile(filename)

    # print tokens using lexer -- uncomment to see tokens in the input file
    # decaflexer.printTokens(data)

    # parse program using parser
    if decafparser.parse(data) :
        print 'Yes'


