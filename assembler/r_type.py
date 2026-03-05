from store import R_type,Register_Mapping
def r_to_bin(instruction):
    try:
        l = instruction.split(" ")
        command = l[0]
        if command not in R_type:
            raise Exception("Wrong assembly command")

        l1 = l[1].split(",")
        rs2 = Register_Mapping[l1[2]]
        rs1 = Register_Mapping[l1[1]]
        rd = Register_Mapping[l1[0]]
        funct7 = R_type[l[0]][0]
        funct3 = R_type[l[0]][1]
        opcode = "0110011"
        return funct7+rs2+rs1+funct3+rd+opcode
    
    except:
        raise Exception("Wrong assembly command")
