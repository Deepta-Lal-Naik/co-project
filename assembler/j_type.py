from store import Register_Mapping,twos

def j_to_bin(instruction,pc,labels):

    l = instruction.split(maxsplit=1)
    l1 = l[1].replace(" ","").split(",")
    label=l1[1]
    rd = Register_Mapping[l1[0]]
    offset = labels[label]-pc
    offset = twos(offset>>1,20)

    imm20 = offset[0]
    imm10_1 = offset[10:]
    imm11 = offset[9]
    imm19_12 = offset[1:9]

    return imm20+imm10_1+imm11+imm19_12+rd+"1101111"
