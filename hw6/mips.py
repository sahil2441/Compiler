
class INSTRUCTION(object):
    mipsRegisterSet =  [ 'zero',
                  'at',
                  'v0',
                  'v1',
                  'a0',
                  'a1',
                  'a2',
                  'a3',
                  't0',
                  't1',
                  't2',
                  't3',
                  't4',
                  't5',
                  't6',
                  't7',
                  't8',
                  't9',
                  's0',
                  's1',
                  's2',
                  's3',
                  's4',
                  's5',
                  's6',
                  's7',
                  'k0',
                  'k1',
                  'gp',
                  'sp',
                  'fp',
                  'ra'
                  ]

    ZERO,AT,V0,V1,A0,A1,A2,A3,T0,T1,T2,T3,T4,T5,T6,T7,T8, \
    T9,S0,S1,S2,S3,S4,S5,S6,S7,K0,K1,GP,SP,FP,RA = mipsRegisterSet

    arithmeticInstructions = ['abs',
                              'add(u)',
                              'and',
                              'div(u)',
                              'mul',
                              'mulo',
                              'mult(u)',
                              'neg(u)',
                              'nor',
                              'not',
                              'or',
                              'rem',
                              'rol',
                              'ror',
                              'sll',
                              'sra',
                              'srl',
                              'sub(u)',
                              'xor'
                            ]
    ABS,ADD,AND,DIV,MUL,MULO,MULT,NEG,NOR,NOT,OR,REM,ROL,ROR,SLL,SRA,SRL,SUB,XOR = arithmeticInstructions

















