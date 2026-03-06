from store import Register_Mapping,U_TYPE
REGISTER_MAPPING = Register_Mapping
u_type_info=U_TYPE 

def u_to_bin(instruction):  

    #parsing
    part1=instruction.split()
    instruction_name = part1[0]

    # instruction validation
    if instruction_name not in u_type_info:
        raise ValueError("invalid instruction")
            
    part2=part1[1].split(",")
    rd=part2[0]
    imm=part2[1]

    #checking if the register is valid
    if rd not in REGISTER_MAPPING:
        raise ValueError("invalid register")
            
    #checking if immediate is an integer 
    try:
        int_imm=int(imm)
    except:
        raise ValueError("immediate is not a valid integer")
            
    #checking if the immediate is in the 20 bit 2's complement range 
    if not (-2**19 <= int_imm <= 2**19 - 1):
        raise ValueError("immediate out of range")
            
     #converting the immediate to 20 bit 2's complement form 
    if int_imm>=0:
        imm_binary=(bin(int_imm))[2:]
        immediate="0"*(20-len(imm_binary))+imm_binary
    else:
        int_imm = 2**20 + int_imm
        imm_binary=(bin(int_imm))[2:]
        immediate="0"*(20-len(imm_binary))+imm_binary
        
    #final binary instruction
    # U-type instruction format: imm[31:12] | rd | opcode
    binary_instruction = immediate + REGISTER_MAPPING[rd] + u_type_info[instruction_name]["opcode"]
    return binary_instruction


