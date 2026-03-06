from store import Register_Mapping,I_Type
instr = I_Type

#Function to convert immediate value to binary
def imm_to_bin(imm):
    imm = int(imm)
    if imm < 0:
        imm = (1<<12) + imm
    return format(imm,"012b") 

#Function to convert register value to binary            
def reg_to_bin(reg):
    return Register_Mapping[reg]
          
#Function to convert instructions to binary     
def i_to_bin(inp, pc = None, label = None):
    
    try:
        x = inp.replace(",", " ").split()

        b = instr.get(x[0])
        if b is None:
             raise Exception()
        
        funct3, opcode = b     

        if x[0] == "lw":
                rd = reg_to_bin(x[1])   
                imm, rs1 = x[2].replace(")", "").split("(") #Removing brackets 
                rs = reg_to_bin(rs1)    
                imm = imm_to_bin(imm)
        
        else:
                rd = reg_to_bin(x[1])
                rs = reg_to_bin(x[2])
                imm = imm_to_bin(x[3])
                
        return imm + rs + funct3 + rd + opcode
   
    except:
        raise Exception("Invalid assembly command")
                      
                        

              



