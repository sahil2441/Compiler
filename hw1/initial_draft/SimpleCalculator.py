'''Simple Calculator'''

class SimpleCalculator(object):
    def getUserInput(self):
        instText = ''
        while True:
            line = raw_input()
            if line =='':
                break
            instText += line + '\n'        
        return instText