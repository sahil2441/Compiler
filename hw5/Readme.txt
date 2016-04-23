The program is initialized from the file decafch.py

To run the program:
Go the directory
~/jsundar-sahjain/hw4
and run
python decafch.py test_case.decaf

In line 43 it calls the class generatecode
                ast.generatecode();

which does the code generation for the input program.
Then in the next line, it prints the output to the file [Filename].ami
                absmc.printAMI(filename);

Inside ast.py, the generate code function recursively calls another functions based on the structure
of the program. For instance, inside class 'BlockStatement', the generatecode loops over every statement
in the statement list.

    def generatecode(self):
        for statement in self.stmtlist:
            statement.generatecode()

And so on.

Another aspect is the label generation which is used in cases like, for loop, while loop etc.



