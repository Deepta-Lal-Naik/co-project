from store import Register_Mapping,S_Type
REGISTER_MAPPING = Register_Mapping
s_type_info=S_Type

def s_to_bin(instruction):    

    try:
        #parsing 
        part1=instruction.split()
        instruction_name = part1[0]  
        part2=part1[1].split(",")
        rs2=part2[0]
        base_offset=part2[1].strip(")").split("(")
        rs1=base_offset[1]
        imm=(base_offset[0]) 
        int_imm=int(imm) 
        if int_imm>=0:
            imm_binary=(bin(int_imm))[2:]
            immediate="0"*(12-len(imm_binary))+imm_binary
        else:
            int_imm = 2**12 + int_imm
            imm_binary=(bin(int_imm))[2:]
            immediate="0"*(12-len(imm_binary))+imm_binary

        #splitting the immediate 
        imm_11_5=immediate[:7]
        imm_4_0=immediate[7:]
        
        #final binary instruction
        # S-type format: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
        binary_instruction = imm_11_5 + REGISTER_MAPPING[rs2] + REGISTER_MAPPING[rs1] + s_type_info[instruction_name]["funct3"] + imm_4_0 + s_type_info[instruction_name]["opcode"]
        return binary_instruction

    except:
        raise Exception("Invalid assembly command")



