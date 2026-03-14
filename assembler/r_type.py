from store import R_Type,Register_Mapping
def r_to_bin(instruction):
  
        l = instruction.split(maxsplit=1)
        command = l[0]
        l1 = l[1].replace(" ","").split(",")
        rs2 = Register_Mapping[l1[2]]
        rs1 = Register_Mapping[l1[1]]
        rd = Register_Mapping[l1[0]]
        funct7 = R_Type[command][0]
        funct3 = R_Type[command][1]
        opcode = "0110011"
        return funct7+rs2+rs1+funct3+rd+opcode
    
