from store import Register_Mapping

instr = { "lw" :["010","0000011"], #0-index: funct3,  1-index: opcode
         "addi" :["000","0010011"],
         "sltiu":["011","0010011"],
         "jalr" :["000","1100111"]  }


inp = "addi x5, x3, -1"

#Function to convert immediate value to binary
def imm_to_bin(imm, pc = None, label = None):
    imm = int(imm)
    if imm >= 0:
        return format(imm, "012b")
    else:
        return format( (1<<12) - abs(imm), "012b")

#Function to convert register value to binary            
def reg_to_bin(reg, pc = None, label = None):
    return format(int(Register_Mapping[reg]), "05b")
          
#Function to convert instructions to binary     
def itoBinary(inp, pc = None, label = None):
    cmd = []
    cmd.append(inp.replace(",","").split())
    try:
        for x in cmd:
            b = instr.get(x[0])
            funct3, opcode = b     

            if x[0] == "lw":
                rd = reg_to_bin(x[1])   
                imm, rs1 = x[2].replace(")", "").split("(") #Removing brackets 
                rs = reg_to_bin(rs1[1])    
                imm = imm_to_bin(imm)
        
            else:
                rd = reg_to_bin(x[1])
                rs = reg_to_bin(x[2])
                imm = imm_to_bin(x[3])
                
        print(imm + rs + funct3 + rd + opcode)
    except:
            raise Exception("Invalid assembly command")
itoBinary(inp)          

                      
                        

              



