Homework 3

The file AST.py contains the class definition for Constructor, Method, Field, Variable, Type and DecafClass.
The toString() method of DecafClass prepares the output by iterating over all the fields and methods.

The stub methods are added in decafParser.py to elaborate the leaves and creating the syntax tree, and also to
handle the errors.

The file decafflexer.py has not been modified.

To run the program open the terminal from the root folder and type:

python decafch.py <file_name.decaf>


To include and print the In and Out classes, please copy and include the following snippet in the test case:

class In{
public static int scan_int()
{
}

public static float scan_float()
{
}

}

class Out {
public static void print (int i)
{
}
public static void print (int f)
{
}
public static void print (int b)
{
}
public static void print (int s)
{
}
}