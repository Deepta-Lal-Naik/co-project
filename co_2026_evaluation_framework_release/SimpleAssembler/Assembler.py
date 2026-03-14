import sys

Register_Mapping = {
"x0":"00000","zero":"00000",
"x1":"00001","ra":"00001",
"x2":"00010","sp":"00010",
"x3":"00011","gp":"00011",
"x4":"00100","tp":"00100",
"x5":"00101","t0":"00101",
"x6":"00110","t1":"00110",
"x7":"00111","t2":"00111",
"x8":"01000","s0":"01000","fp":"01000",
"x9":"01001","s1":"01001",
"x10":"01010","a0":"01010",
"x11":"01011","a1":"01011",
"x12":"01100","a2":"01100",
"x13":"01101","a3":"01101",
"x14":"01110","a4":"01110",
"x15":"01111","a5":"01111",
"x16":"10000","a6":"10000",
"x17":"10001","a7":"10001",
"x18":"10010","s2":"10010",
"x19":"10011","s3":"10011",
"x20":"10100","s4":"10100",
"x21":"10101","s5":"10101",
"x22":"10110","s6":"10110",
"x23":"10111","s7":"10111",
"x24":"11000","s8":"11000",
"x25":"11001","s9":"11001",
"x26":"11010","s10":"11010",
"x27":"11011","s11":"11011",
"x28":"11100","t3":"11100",
"x29":"11101","t4":"11101",
"x30":"11110","t5":"11110",
"x31":"11111","t6":"11111"
}

R_Type = {
"add": ["0000000","000"],
"sub": ["0100000","000"],
"sll": ["0000000","001"],
"slt": ["0000000","010"],
"sltu": ["0000000","011"],
"xor": ["0000000","100"],
"srl": ["0000000","101"],
"or":  ["0000000","110"],
"and": ["0000000","111"]
}

def twos(val,bits):
    if val < 0:
        val = (1<<bits) + val
    return format(val,f"0{bits}b")

def imm_range(imm,n):
    if imm>=((-2)**(n-1)) and imm<=((2**(n-1))-1):
        pass
    else:
        raise Exception("Immediate is out of range")
#I-type
#funct3,opcode values in list
I_Type = { "lw" :["010","0000011"], #0-index: funct3,  1-index: opcode
         "addi" :["000","0010011"],
         "sltiu":["011","0010011"],
         "jalr" :["000","1100111"]  }


#S-type
#funct3,opcode values in list
S_Type ={"sw":{"funct3":"010","opcode":"0100011"}}

#B-type
#funct3,opcode values in list
B_Type = {"beq":"000","bne":"001","blt":"100","bge":"101","bltu":"110","bgeu":"111"}

#U-type
#opcode as value
U_Type = {"auipc":{"opcode":"0010111"},"lui":{"opcode":"0110111"}}  

#r-type
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
    
#j-type
def j_to_bin(instruction,pc,labels):

    l = instruction.split(maxsplit=1)
    l1 = l[1].replace(" ","").split(",")
    label=l1[1]
    rd = Register_Mapping[l1[0]]
    if label.isdigit():
        offset = int(label)
    else:
        offset = labels[label]-pc
    imm_range(offset,20)
    offset = twos(offset>>1,20)
    
    imm20 = offset[0]
    imm10_1 = offset[10:]
    imm11 = offset[9]
    imm19_12 = offset[1:9]
    return imm20+imm10_1+imm11+imm19_12+rd+"1101111"


#b-type 

def b_type_encoder(func,r1,r2,off_val,pc,labels):
    opcode="1100011"
    if off_val.isdigit():
        offset=int(off_val)
    else:
        offset=labels[off_val]-pc
    imm_range(offset,12)
    imm = twos(offset>>1,12)
    imm_12=imm[0]
    imm10_5=imm[2:8]
    imm4_1=imm[8:12]
    imm_11=imm[1]
    r1=Register_Mapping[r1]
    r2=Register_Mapping[r2]
    return imm_12+imm10_5+r2+r1+B_Type[func]+imm4_1+imm_11+opcode

def b_to_bin(ins,pc,labels):
        ins=ins.replace(",", " ")
        a=ins.split()
        return b_type_encoder(a[0],a[1],a[2],a[3],pc,labels)

#u-type
def u_to_bin(instruction):  

    #parsing
    part1=instruction.split(maxsplit=1)
    instruction_name = part1[0]
    part2=part1[1].replace(" ","").split(",")
    rd=part2[0]
    imm=part2[1]

    #checking if immediate is an integer 
    int_imm=int(imm)
    immediate=twos(int_imm,20)
    # imm_range(int_imm,20)
    #final binary instruction
    # U-type instruction format: imm[31:12] | rd | opcode
    binary_instruction = immediate + Register_Mapping[rd] + U_Type[instruction_name]["opcode"]
    return binary_instruction

#s-type

def s_to_bin(instruction):    

    #parsing 
    part1=instruction.split(maxsplit=1)
    instruction_name = part1[0]
    part2=part1[1].replace(" ","").split(",")
    rs2=part2[0]
    base_offset=part2[1].strip(")").split("(")
    rs1=base_offset[1]
    imm=base_offset[0]
    
    
    #checking if immediate is an integer 

    int_imm=int(imm)
    immediate=twos(int_imm,12)
    # imm_range(int_imm,12)
    #checking if the immediate is in the 12 bit 2's complement range 

    #converting the immediate to 12 bit 2's complement form 
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
    binary_instruction = imm_11_5 + Register_Mapping[rs2] + Register_Mapping[rs1] + S_Type[instruction_name]["funct3"] + imm_4_0 + S_Type[instruction_name]["opcode"]
    return binary_instruction

#i-type
#Function to convert immediate value to binary
def imm_to_bin(imm, pc = None, label = None):
    imm = int(imm)
    imm_range(imm,12)
    ct_twos = twos(int(imm),12)
    return ct_twos

#Function to convert register value to binary            
def reg_to_bin(reg, pc = None, label = None):
    return Register_Mapping[reg]
          
#Function to convert instructions to binary     
def i_to_bin(inp, pc = None, label = None):
    
    
        x = inp.replace(",", " ").split()

        b = I_Type.get(x[0])
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
    

def virtual_halt(ins,labels):
    try:
        ins=ins.replace(",", " ")
        a=ins.split()
        try:
            a[3]=int(a[3])
        except:
            a[3]=labels[a[3]]

        if a[0]=="beq" and (a[1]=="zero" or a[1]=="x0") and (a[2]=="zero" or a[2]=="x0") and int(a[3])==0:
            return 
        else:
            raise Exception("Virtual halt is not the last instruction")
    except:
        raise Exception("Virtual halt is not the last instruction")
    
def c_labels(data):
        dic = {}
        pc=0
        for i in data:
            if ":" in i:
                label = i.split(":")[0]
                dic[label.strip()]=pc
                t = i.split(":")[1]
                if t.strip!="":
                    pc+=4
            else:
                pc+=4

        return dic

def main():
    data_file = sys.argv[1]
    out_file = sys.argv[2]
    with open(data_file,"r") as f:
        data = [i.strip() for i in f.readlines()]

    wdata = []
    pc=0
    if ":" in data[-1]:
        temp =  data[-1].split(":")
        last_instruction = temp[1].strip()
    else:
        last_instruction=data[-1]
    labels = c_labels(data)
    for i in data:
        try:
            if ":" in i:
                temp = i.split(":")
                line_label = temp[0]
                if temp[1].strip()=="":
                    continue
                instruction = temp[1].strip()
            else:
                instruction=i
            operation = instruction.split()[0]
            if operation not in list(R_Type.keys())+list(I_Type.keys())+list(B_Type.keys())+list(S_Type.keys())+["jal"]+list(U_Type.keys()):
                raise Exception("Wrong operation")
            if operation in R_Type:
                wdata.append(r_to_bin(instruction))
            elif operation in I_Type:
                wdata.append(i_to_bin(instruction))
            elif operation in B_Type:
                wdata.append(b_to_bin(instruction,pc,labels))
            elif operation=="sw":
                wdata.append(s_to_bin(instruction))
            elif operation=="jal":
                wdata.append(j_to_bin(instruction,pc,labels))
            elif operation in ["lui","auipc"]:
                wdata.append(u_to_bin(instruction))
            pc+=4
        except KeyError:
            print("Error at line",(pc/4)+1, ": Typo in instruction")
            return
        except Exception as e:
            print("Error at line",(pc/4)+1,e)
            return
    with open(out_file,"w") as f:
        for i in wdata:
            f.write(i+'\n')
    try:
        virtual_halt(last_instruction,labels)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()