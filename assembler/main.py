import sys

# register encoding
REG = {
"x0":"00000","zero":"00000",
"x1":"00001","ra":"00001",
"x2":"00010","sp":"00010",
"x3":"00011","gp":"00011",
"x4":"00100","tp":"00100",
"x5":"00101","t0":"00101",
"x6":"00110","t1":"00110",
"x7":"00111","t2":"00111",
"x8":"01000","s0":"01000","fp":"01000",
"x9":"01001","s1":"01001",
"x10":"01010","a0":"01010",
"x11":"01011","a1":"01011",
"x12":"01100","a2":"01100",
"x13":"01101","a3":"01101",
"x14":"01110","a4":"01110",
"x15":"01111","a5":"01111",
"x16":"10000","a6":"10000",
"x17":"10001","a7":"10001",
"x18":"10010","s2":"10010",
"x19":"10011","s3":"10011",
"x20":"10100","s4":"10100",
"x21":"10101","s5":"10101",
"x22":"10110","s6":"10110",
"x23":"10111","s7":"10111",
"x24":"11000","s8":"11000",
"x25":"11001","s9":"11001",
"x26":"11010","s10":"11010",
"x27":"11011","s11":"11011",
"x28":"11100","t3":"11100",
"x29":"11101","t4":"11101",
"x30":"11110","t5":"11110",
"x31":"11111","t6":"11111"
}

# opcode tables
R_FUNCT = {
    "add":("0000000","000"),
    "sub":("0100000","000"),
    "sll":("0000000","001"),
    "slt":("0000000","010"),
    "sltu":("0000000","011"),
    "xor":("0000000","100"),
    "srl":("0000000","101"),
    "or":("0000000","110"),
    "and":("0000000","111")
}

I_FUNCT = {
    "addi":"000",
    "lw":"010",
    "sltiu":"011",
    "jalr":"000"
}

B_FUNCT = {
    "beq":"000",
    "bne":"001",
    "blt":"100",
    "bge":"101",
    "bltu":"110",
    "bgeu":"111"
}

def twos(val,bits):
    if val < 0:
        val = (1<<bits) + val
    return format(val,f"0{bits}b")


# ---------- R TYPE ----------
def encode_r(cmd):
    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rd,rs1,rs2 = rest.split(",")

    funct7,funct3 = R_FUNCT[op]

    return (
        funct7 +
        REG[rs2] +
        REG[rs1] +
        funct3 +
        REG[rd] +
        "0110011"
    )


# ---------- I TYPE ----------
def encode_i(cmd):

    if cmd.startswith("lw"):
        parts = cmd.split(maxsplit=1)
        op = parts[0]
        rest = parts[1]
        rest = rest.replace(" ", "")
        rd,addr = rest.split(",")
        imm,rs1 = addr.split("(")
        rs1 = rs1[:-1]

    else:
        parts = cmd.split(maxsplit=1)
        op = parts[0]
        rest = parts[1]
        rest = rest.replace(" ", "")
        rd,rs1,imm = rest.split(",")

    imm = twos(int(imm),12)

    return (
        imm +
        REG[rs1] +
        I_FUNCT[op] +
        REG[rd] +
        ("0000011" if op=="lw" else "0010011" if op!="jalr" else "1100111")
    )


# ---------- S TYPE ----------
def encode_s(cmd):

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rs2,addr = rest.split(",")

    imm,rs1 = addr.split("(")
    rs1 = rs1[:-1]

    imm = twos(int(imm),12)

    return (
        imm[:7] +
        REG[rs2] +
        REG[rs1] +
        "010" +
        imm[7:] +
        "0100011"
    )


# ---------- B TYPE ----------
def encode_b(cmd,labels,pc):

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rs1,rs2,label = rest.split(",")

    if label in labels:
        offset = labels[label] - pc
    else:
        offset = int(label)
    imm = twos(offset>>1,12)

    return (
        imm[0] +
        imm[2:8] +
        REG[rs2] +
        REG[rs1] +
        B_FUNCT[op] +
        imm[8:] +
        imm[1] +
        "1100011"
    )


# ---------- U TYPE ----------
def encode_u(cmd):

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rd,imm = rest.split(",")

    imm = twos(int(imm),20)

    return (
        imm +
        REG[rd] +
        ("0110111" if op=="lui" else "0010111")
    )


# ---------- J TYPE ----------
def encode_j(cmd,labels,pc):

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rd,label = rest.split(",")

    offset = labels[label] - pc
    imm = twos(offset>>1,20)

    return (
        imm[0] +
        imm[10:] +
        imm[9] +
        imm[1:9] +
        REG[rd] +
        "1101111"
    )


def read_lines(file):
    out=[]
    with open(file) as f:
        for l in f:
            l=l.strip()
            if l!="":
                out.append(l)
    return out


def collect_labels(lines):

    labels={}
    pc=0

    for line in lines:

        if ":" in line:
            lab,rest=line.split(":")
            labels[lab.strip()]=pc
            if rest.strip()!="":
                pc+=4
        else:
            pc+=4

    return labels


def assemble(lines,labels):

    pc=0
    out=[]

    for line in lines:

        if ":" in line:
            parts=line.split(":")
            if parts[1].strip()=="":
                continue
            line=parts[1].strip()

        op=line.split()[0]

        if op in R_FUNCT:
            out.append(encode_r(line))

        elif op in I_FUNCT:
            out.append(encode_i(line))

        elif op=="sw":
            out.append(encode_s(line))

        elif op in B_FUNCT:
            out.append(encode_b(line,labels,pc))

        elif op in ["lui","auipc"]:
            out.append(encode_u(line))

        elif op=="jal":
            out.append(encode_j(line,labels,pc))

        pc+=4

    return out


def main():

    inp=sys.argv[1]
    outp=sys.argv[2]

    lines=read_lines(inp)
    labels=collect_labels(lines)
    code=assemble(lines,labels)

    with open(outp,"w") as f:
        for c in code:
            f.write(c+"\n")


if __name__=="__main__":
    main()



with open("out.txt","r") as f:
    d = f.readlines()

with open("sol.txt","r") as f:
    d2 = f.readlines()
for i in range(len(d)):
    
    print(f"{i+1}. {d[i]==d2[i]}")