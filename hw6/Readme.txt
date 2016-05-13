absmc.py - For each instruction of intermediate code (ami) we have added the corresponding MIPS translation

controlflow.py - For liveness analysis, intereference graph construction, coloring of graph, register allocation, and storing lookup structure
                 the MIPS registers, we have used this file. All the main logic for HW6 is incorporated in this file

decafch.py - In this file we are calling the utility method which prints and stores the "asm" file once the intermediate code is generated and the final code is generated using register allocation logic

- SSA form has not been implemented

How to Run?
- In terminal pass the decaf program file as an input argument and run the program as
  python decafch.py <test_case.decaf>
  This will generate the 'test_case.asm' file in the same folder where the decaf program was located.





