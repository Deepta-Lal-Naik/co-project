REGISTER_MAPPING = {
    "zero": "00000",  
    "ra":   "00001",  
    "sp":   "00010",  
    "gp":   "00011",
    "tp":   "00100",  
    "t0":   "00101",  
    "t1":   "00110", 
    "t2":   "00111", 
    "s0":   "01000",
    "s1":   "01001",
    "a0":   "01010", 
    "a1":   "01011", 
    "a2":   "01100", 
    "a3":   "01101", 
    "a4":   "01110", 
    "a5":   "01111",
    "a6":   "10000",
    "a7":   "10001",
    "s2":   "10010",
    "s3":   "10011",
    "s4":   "10100",
    "s5":   "10101",
    "s6":   "10110",
    "s7":   "10111",
    "s8":   "11000",
    "s9":   "11001",
    "s10":  "11010",
    "s11":  "11011",
    "t3":   "11100", 
    "t4":   "11101", 
    "t5":   "11110", 
    "t6":   "11111", 
}
u_type_info={"auipc":{"opcode":"0010111"},"lui":{"opcode":"0110111"}}   

def u_type(instruction):  

    #parsing
    part1=instruction.split()
    instruction_name = part1[0]

    # instruction validation
    if instruction_name not in u_type_info:
        print("invalid instruction")
        return
    
    part2=part1[1].split(",")
    rd=part2[0]
    imm=part2[1]

    #checking if the register is valid
    if rd not in REGISTER_MAPPING:
        print("invalid register")
        return
    
    #checking if immediate is an integer 
    try:
        int_imm=int(imm)
    except:
        print("immediate is not a valid integer")
        return
    
    #checking if the immediate is in the 20 bit 2's complement range 
    if not (-2**19 <= int_imm <= 2**19 - 1):
        print("the immediate can't be represented using a 20 bit 2's complement representation")
        return
    
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


