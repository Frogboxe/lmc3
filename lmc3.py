
from functools import lru_cache
from sys import argv


class P:
    # Consts
    DBG = True
    SS = [False, [], []]
    S_NUM = 0
    SYS_BITS = 16
    # Vars
    acc = 0
    pc = 0
    hlt = False
    srcMode = True
    script =  []
    memory =  {}
    scripts = {}
    creating = None
    def SetSysMax(bits):
        P.SYS_BITS = bits

def VAL_INP():
    if P.SS[0]:
        P.S_NUM += 1
        return Int(P.SS[1][P.S_NUM-1])
    else:
        return Int(input("INP:: "))

def VAL_OUT(val):
    if P.SS[0]:
        P.SS[2].append(val)
    else:
        print(val)
    
def Int(n):
    return int(n, base=2)

def Next():
    P.pc += 1

def INP():
    P.acc = VAL_INP()
    Next()

def OUT():
    if P.DBG: print("OUT:: ", end="")
    VAL_OUT(bin(P.acc)[2::].rjust(P.SYS_BITS, "0"))
    Next()

def SET(val):
    P.acc = Int(val)
    Next()

def STA(at):
    P.memory[Int(at)] = P.acc
    Next()

def LDA(at):
    P.acc = int(P.memory[Int(at)])
    Next()

def ADD(at):
    P.acc = int(P.acc + P.memory[Int(at)])
    Next()

def SUB(at):
    P.acc = int(P.acc - int(P.memory[Int(at)]))
    Next()

def GOTO(lne):
    P.pc = lne

def BRP(lne):
    lne = Int(lne)
    if int(P.acc) >= 0:
        GOTO(lne)
    else:
        Next()

def BRZ(lne):
    lne = Int(lne)
    if int(P.acc) == 0:
        GOTO(lne)
    else:
        Next()

def HLT():
    P.hlt = True

def ReadMode(cmd, arg):
    if   cmd == "0000": # T1
        HLT()
    elif cmd == "0001":
        INP()
    elif cmd == "0010":
        OUT()
    elif cmd == "0011":
        ADD(arg)
    elif cmd == "0100":
        STA(arg)
    elif cmd == "0101":
        LDA(arg)
    elif cmd == "0110":
        SET(arg)
    elif cmd == "0111":
        SUB(arg)
    elif cmd == "1000": # T2
        GOTO(Int(arg))
    elif cmd == "1001":
        BRZ(arg)
    elif cmd == "1010":
        BRP(arg)
    elif cmd == "1011":
        pass#PAS(arg)                   
    else:
        print("FAILTURE:: LINE {} {} IS INVALID".format(cmd, arg))
        
def ReadLine():
    line = P.script[P.pc]
    cmd = line[0:4]
    arg = line[4::]
    ReadMode(cmd, arg)

def Read(txt):
    P.SetSysMax(Int(txt[0:8])+1)
    txt = txt[8::]
    line = ""
    for char, n in zip(txt, range(len(txt))):
        line += char
        if n % P.SYS_BITS == P.SYS_BITS-1:
            P.script.append(line)
            line = ""
    for n in range(2**(P.SYS_BITS-4)):
        P.script.append("".rjust(P.SYS_BITS, "0"))
    print(P.SYS_BITS)
    while not P.hlt:
        ReadLine()

try:
    with open(argv[1], "r") as f:
        Read("".join(f.readlines()).replace("\n", "").replace(" ", ""))
except IndexError:
    print("RUNNING DEFAULT SCRIPT")
    Read("""
00001111
0110000000000000
0100000010001111
0110000000000001
0100000010001110
0001000000000000
0100000010001101
0101000010001111
0010000000000000
0101000010001101
0111000010001110
1010000000001100
1000000000010101
0101000010001111
0011000010001110
0100000010001100
0101000010001110
0100000010001111
0010000000000000
0101000010001100
0100000010001110
1000000000001000
0000000000000000
""".replace("\n", "").replace(" ", ""))




























