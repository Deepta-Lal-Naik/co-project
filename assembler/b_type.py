from store import Register_Mapping,B_Type,twos
def b_type_encoder(func,r1,r2,off_val,pc,labels):
    b_func3=B_Type
    opcode="1100011"
    if off_val.isdigit():
        offset=int(off_val)
    else:
        offset=labels[off_val]-pc
    imm = twos(offset>>1,12)
    imm_12=imm[0]
    imm10_5=imm[2:8]
    imm4_1=imm[8:12]
    imm_11=imm[1]
    r1=Register_Mapping[r1]
    r2=Register_Mapping[r2]
    return imm_12+imm10_5+r2+r1+b_func3[func]+imm4_1+imm_11+opcode

def b_to_bin(ins,pc,labels):
        ins=ins.replace(",", " ")
        a=ins.split()
        return b_type_encoder(a[0],a[1],a[2],a[3],pc,labels)
ins = "exit: beq zero,zero,0"
if ":" in ins:
    temp =  ins.split(":")
    last_instruction = temp[1].strip()
else:
    pass


last_instruction=last_instruction.replace(",", " ")
a=last_instruction.split()
print((a[1]=="zero" or a[1]=="x0"))