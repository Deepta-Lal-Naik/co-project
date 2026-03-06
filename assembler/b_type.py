from store import Register_Mapping,B_Type
def b_type_encoder(func,r1,r2,off_val,pc,labels):
    b_func3=B_Type
    opcode="1100011"
    if off_val.lstrip("-").isdigit():
        offset=int(off_val)
    else:
        if off_val not in labels:
            raise Exception
        offset=labels[off_val]-pc
    if offset <-2048 or offset >2047:#range -2^(n-1)-(2^(n-1))-1
        raise Exception
    if offset<0:
        offset=(1<<12)+offset
    imm=format(offset,"012b")
    imm_12=imm[0]
    imm10_5=imm[1:7]
    imm4_1=imm[7:11]
    imm_11=imm[11]
    r1=Register_Mapping[r1]
    r2=Register_Mapping[r2]
    return imm_12+imm10_5+r2+r1+b_func3[func]+imm4_1+imm_11+opcode

def b_to_bin(ins,pc,labels):
    try:
        if ":" in ins:
            ins = ins.split(":")[1].strip()
        ins=ins.replace(",", " ")
        a=ins.split()
        return b_type_encoder(a[0],a[1],a[2],a[3],pc,labels)
    except:
        raise Exception("There is some error in the instruction passed")
