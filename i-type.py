#def itype(command):
instr = { "lw" :["010","0000011"], #0-index: funct3,  1-index: opcode
         "addi" :["000","0010011"],
         "sltiu":["011","0010011"],
         "jalr" :["000","1100111"]  }

# Load instructions to program
S = []
def load(): 
        '''with open("assembly.txt",'r') as fin:
            L = fin.readlines()
            for i in L:
                j = i.replace(",","").split()
                S.append(j)'''
        L = "addi x5, x3, -1"
        j = L.replace(",","").split()
        S.append(j)
        print(S)    
load()

#Function to convert immediate value to binary
def imm_to_bin(imm):
    return format(int(imm),"012b")

#Function to convert register value to binary            
def reg_to_bin(reg):
    return format(int(reg), "05b")            
def twoComp(imm):
     
          
#Function to convert instructions to binary     
def toBinary(S):
    for x in S:
        b = instr.get(x[0])
        funct3, opcode = b

        #CHECKS FOR IMM
        if imm < 0:
            imm  = twoComp(imm)
        #elif len(imm) > 12:
            #      raise error   
        elif imm == []:
            print("Syntax error")
        else:
             #go to label     

        #CHECKS FOR REG
        if rs1 == [0]:
            print("x0 being used to store value!")

        if x[0] == "lw":

            rd = reg_to_bin(x[1][1:])   
            imm, rs1 = x[2].replace(")", "").split("(") #Removing brackets 
            rs = reg_to_bin(rs1[1:])    
            imm = imm_to_bin(imm)
        else:
            rd = reg_to_bin(x[1][1:])
            rs = reg_to_bin(x[2][1:])
            imm = imm_to_bin(x[3])
    print(imm + rs + funct3 + rd + opcode)

toBinary(S)          



                      
                        

              

