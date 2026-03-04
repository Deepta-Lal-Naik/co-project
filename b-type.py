with open("data.txt","r") as f:
    l=f.readlines()

def b_type_encoder(func,r1,r2,off_val):
    b_func3={"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}
    opcode="1100011"
    if off_val.lstrip("-").isdigit():
        offset=int(off_val)
    else:
        if off_val not in labels:
            return "No such Label defined"
        offset=labels[off_val]-pc
    if offset <-2048 or offset >2047:#range -2^(n-1)-(2^(n-1))-1
        return "Offset not in appropriate branch range"
    if offset<0:
        offset=(1<<12)+offset
    imm=format(offset,"012b")
    imm_12=imm[0]
    imm10_5=imm[1:7]
    imm4_1=imm[7:11]
    imm_11=imm[11]
    r1=format(int(r1[1:]),"05b")
    r2=format(int(r2[1:]),"05b")
    return imm_12+imm10_5+r2+r1+b_func3[func]+imm4_1+imm_11+opcode

labels={}#label definition
pc_count=0
for ins in l:
    if ":" in ins:
        b=ins.split(":")
        labels[b[0].strip()]=pc_count
        pc_count+=4
    else:
        pc_count+=4

pc=0
for ins in l:
    if ":" in ins:
        ins = ins.split(":")[1].strip()
    ins=ins.replace(",", " ")
    a=ins.split()
    if a[1]=="zero":
        a[1]="x0"
    if a[2]=="zero":
        a[2]="x0"
    print(b_type_encoder(a[0],a[1],a[2],a[3]))
    pc+=4

