from store import Register_Mapping

def j_to_bin(instruction):

    l = instruction.split(" ")
    l1 = l[1].split(",")
    command = l[0]
    if command!="jal":
        print("Wrong command")
        pass
    if int(l1[1][:])%2==1:
        print("Odd immediate")
        pass

    rd = Register_Mapping[l1[0]]
    offset = format(int(l1[1][:])>>1,"021b")
    imm20 = offset[0]
    imm10_1 = offset[10:20]
    imm11 = offset[9]
    imm19_12 = offset[1:9]
    print(imm20+imm10_1+imm11+imm19_12+rd+"1101111")
    return imm20+imm10_1+imm11+imm19_12+rd+"1101111"
j_to_bin()