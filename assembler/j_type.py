from store import Register_Mapping

def j_to_bin(instruction,pc,label_adrr):

    l = instruction.split(" ")
    l1 = l[1].split(",")
    command = l[0]
    if command!="jal":
        raise Exception

    rd = Register_Mapping[l1[0]]
    offset = label_adrr-pc
    if offset<0:
        offset=not(offset)
        offset+=1
    offset = format(offset>>1,"021b")

    print(offset)
    imm20 = offset[0]
    imm10_1 = offset[10:20]
    imm11 = offset[9]
    imm19_12 = offset[1:9]

    return imm20+imm10_1+imm11+imm19_12+rd+"1101111"

def j_to_bin(instruction,imm):

    l = instruction.split(" ")
    l1 = l[1].split(",")
    command = l[0]
    if command!="jal":
        raise Exception

    rd = Register_Mapping[l1[0]]
    offset = imm
    if offset<0:
        offset=not(offset)
        offset+=1
    offset = format(offset>>1,"021b")

    print(offset)
    imm20 = offset[0]
    imm10_1 = offset[10:20]
    imm11 = offset[9]
    imm19_12 = offset[1:9]
    return imm20+imm10_1+imm11+imm19_12+rd+"1101111"
