
from sys import argv

CODE_TABLE = {
    "HLT":"0000",
    "INP":"0001",
    "OUT":"0010",
    "ADD":"0011",
    "STA":"0100",
    "LDA":"0101",
    "SET":"0110",
    "SUB":"0111",
    "BRA":"1000",
    "BRZ":"1001",
    "BRP":"1010",
    "   ":"1011",
    "   ":"1100",
    "   ":"1101",
    "   ":"1110",
    "   ":"1111"
    }

LINE_REQUIRE = ("BRA", "BRZ", "BRP")

class CompilerError(Exception):
    pass

def Bin(n, bits):
    return bin(n)[2::].rjust(bits-4, "0")

def IsReserved(cmd):
    if cmd in CODE_TABLE:
        return True
    return False

def IsLineRequire(cmd):
    return cmd in LINE_REQUIRE

def IsLineTag(cmd, arg):
    if (cmd+arg).isdecimal():
        return False
    elif arg.isdecimal():
        return False
    return True

def ProcReserved(cmd):
    return CODE_TABLE[cmd]

# LineTag is inline

def Read(txt, bits, old):
    script = []
    line = ""
    for char in txt:
        if char != ";":
            line += char
        else:
            script.append(line)
            line = ""
    lines = []
    tags = {}
    flush = set()
    ref = {}
    t = ((bits-4) ** 2) - 1
    n = 0
    for line in script:
        bre = True
        cmd = line[0:3]
        arg = line[3::]
        # CMD
        if IsReserved(cmd):
            line = ProcReserved(cmd)
        elif IsLineTag(cmd, arg):
            bre = False
            n += 1
            line += cmd+arg
            flush.add(cmd+arg)
            ref[cmd+arg] = n
        # ARG
        if IsLineRequire(cmd):
            if arg in tags:
                line += Bin(tags[arg], bits)
            else:
                line += arg
                flush.add(arg)
        elif arg.isdecimal():
            line += Bin(int(arg), bits)
        elif arg == "":
            line += Bin(0, bits)
        elif arg in tags:
            line += tags[arg]
        elif not cmd+arg in flush:
            tags[arg] = Bin(t, bits)
            t -= 1
            line += tags[arg]
        if bre:
            lines.append(line)
        n += 1
        if t == 0:
            raise CompilerError("RAN OUT OF COMPILE MEMORY BY LN {}!"
                                .format(n-1))    
    print(tags)
    print(lines)
    lines = "\n".join(lines)
    if not old:
        for item in flush:
            lines = lines.replace(item, Bin(ref[item]+1, bits))
    return lines
    
with open("config.cfg", "r") as f:
    lines = f.readlines()
    bitLength = int(lines[0])

print(bitLength)
    
try:
    with open(argv[1], "r") as f:
        txt = "".join(f.readlines())
except IndexError:
    print("COMPILING DEFAULT SCRIPT")
    txt = """

SET 0;
STA A;
SET 1;
STA B;
INP;
STA LIMIT;

LDA A;
OUT;

LOOP;
LDA LIMIT;
SUB B;
BRP NEXT;
BRA EXIT;

NEXT;
LDA A;
ADD B;
STA C;

LDA B;
STA A;
OUT;

LDA C;
STA B;

BRA LOOP;

EXIT;
HLT;

"""
txt = txt.replace("\n", "").replace(" ", "").replace("#", "").upper()

script = Read(txt, bitLength, old=False)

try:
    with open(argv[1].split(".")[0:-1]+".lmc", "w") as f:
        print(bin(bitLength-1)[2::].rjust(8, "0"), file=f)
        print(line, file=f)
except IndexError:
    print("not compiling... default script")
    print(bin(bitLength-1)[2::].rjust(8, "0"))
    print(script)


input("EXIT")































