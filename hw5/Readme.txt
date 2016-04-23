The program is initialized from the file decafch.py

The Intermediate Codegeneration logic is folded into ast.py

To run the program:
Go the directory
~/jsundar-sahjain/hw5 and run

    python decafch.py test_case.decaf

decafch.py - Commented the printing of AST
             Added a method call "ast.generatecode()" which is defined for all the expressions in ast.py
             This is the starting point of code generation logic

ast.py -     Inside ast.py, the generate code function recursively calls another functions based on the structure
             of the program. For instance, inside class 'BlockStatement', the generatecode loops over every statement
              in the statement list.

                def generatecode(self):
                    for statement in self.stmtlist:
                        statement.generatecode()

               And so on.

            Another aspect is the label generation which is used in cases like, for loop, while loop etc.

SSA form is NOT handled

absmc.py - This file contains definitions of all the instructions to be carried out as part of IR
           The following method prints the output to the file [Filename].ami
                absmc.printAMI(filename);
           where [Filename] is same is test case file in decaf




