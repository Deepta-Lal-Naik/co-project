import sys
sys.path.append("../../assembler")
from r_type import r_to_bin 
from j_type import j_to_bin 
from s_type import s_to_bin 
from u_type import u_to_bin 
from b_type import b_to_bin 
from i_type import i_to_bin 
from store import R_Type, I_Type, B_Type, S_Type, U_Type

def createLabels(data):
    d={}
    pc=0
    for i in data:
        if ":" in i:
            temp = i.split(":")
            d[temp[0].strip()]=pc
            if temp[1].strip()!="":
                pc+=4
        else:
            pc+=4

    return d
            

data_file = sys.argv[1]
output_file = sys.argv[2]
with open(data_file,"r") as f:
    data = f.readlines()
pc=0
for i in data:
    i=i.strip()

labels = createLabels(data)
with open(output_file,"w") as out:
    for i in data:
        
        if ":" in i:
            temp = i.split(":")
            if temp[1].strip()=="":
                continue
            instruction=temp[1].strip()
        instruction=i
        operation=i.split()[0]

        if operation in R_Type:
            wdata = r_to_bin(instruction)

        elif operation=="jal":
            wdata = j_to_bin(instruction,pc,labels)

        elif operation in S_Type:
            wdata = s_to_bin(instruction)

        elif operation in U_Type:
            wdata = u_to_bin(instruction)

        elif operation in B_Type:
            wdata = b_to_bin(instruction,pc,labels)

        elif operation in I_Type:
            wdata = i_to_bin(instruction)
        
        out.write(wdata+'\n')
        pc+=4

    



