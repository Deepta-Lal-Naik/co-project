from store import Register_Mapping
REGISTER_MAPPING = Register_Mapping
s_type_info={"sw":{"funct3":"010","opcode":"0100011"}}

def s_type(instruction):    

    #parsing 
    part1=instruction.split()
    instruction_name = part1[0]

    # instruction validation
    if instruction_name not in s_type_info:
        print("invalid instruction")
        return
    
    part2=part1[1].split(",")
    rs2=part2[0]
    base_offset=part2[1].strip(")").split("(")
    rs1=base_offset[1]
    imm=base_offset[0]
    
    #checking if the register is valid
    if rs1 not in REGISTER_MAPPING or rs2 not in REGISTER_MAPPING:
        print("invalid register")
        return
    
    #checking if immediate is an integer 
    try:
        int_imm=int(imm)
    except:
        print("immediate is not a valid integer")
        return
    
    #checking if the immediate is in the 12 bit 2's complement range 
    if not (-2048<=int_imm<=2047):
        print("the immediate can't be represented using a 12 bit 2's complement representation")
        return
    
    #converting the immediate to 12 bit 2's complement form 
    if int_imm>=0:
        imm_binary=(bin(int_imm))[2:]
        immediate="0"*(12-len(imm_binary))+imm_binary
    else:
        int_imm = 2**12 + int_imm
        imm_binary=(bin(int_imm))[2:]
        immediate="0"*(12-len(imm_binary))+imm_binary

    #splitting the intermediate 
    imm_11_5=immediate[:7]
    imm_4_0=immediate[7:]
    
    #final binary instruction
    # S-type format: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
    binary_instruction = imm_11_5 + REGISTER_MAPPING[rs2] + REGISTER_MAPPING[rs1] + s_type_info[instruction_name]["funct3"] + imm_4_0 + s_type_info[instruction_name]["opcode"]
    return binary_instruction






