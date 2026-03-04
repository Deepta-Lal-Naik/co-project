def b_type_encoder(func,r1,r2,off_val)
    b_func3={"beq":"000","bne":"001","blt":"100","bge":"101","btlu":"110","bgeu":"111"}
    opcode="1100011"
    if off_val.isdigit():
        offset=off_val
    else:
        offset=l_dict[off_val]-pc
    if offset<0:
        offset=(1<<12)+offset
    imm=format(offset,"012b")
    imm_12=imm[0]
    imm10_5=imm[1:7]
    imm4_1=imm[7:11]
    imm_11=imm[11]

    return 

for ins in l:
    ins="beq rs1, rs2, imm[12:1]"
    a=ins.split(" ")
    b_type_encoder(a[0],a[1].rstrip(","),a[2].rstrip(","),a[3])

