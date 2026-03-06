from store import Register_Mapping,U_Type
REGISTER_MAPPING = Register_Mapping
u_type_info=U_Type

def u_to_bin(instruction):  

    try:
        #parsing
        part1=instruction.split()
        instruction_name = part1[0]

        part2=part1[1].split(",")
        rd=part2[0]
        imm=part2[1]

        int_imm=int(imm)
        
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

    except:
        raise Exception("Invalid assembly command")
