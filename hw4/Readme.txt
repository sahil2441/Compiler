The program is initialized from the file decafch.py
In line 44 it calls the class typecheck.py
            errorFlag = typecheck.checktype(classtable=ast.classtable)

and passes the class table as argument.

The file typecheck.py handles all the typechecking and it's function checktype returns true if it
encounters any error in typechecking.

In the method checktype the idea is to iterate all the classes of the classtable and go through each block/ methods to
check for type errors.

In stage 2, we go through each constructor of the class and resolve type errors.

In the resolveBlock function we check the instance of each statement list and call the function resolve, which is a
recursive function.

To run the program:
Go the directory
~/jsundar-sahjain/hw4
and run
python decafch.py test_case.decaf