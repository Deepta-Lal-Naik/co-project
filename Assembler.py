import sys
from assembler.r_type import r_to_bin
from assembler.j_type import j_to_bin
from assembler.i_type import i_to_bin
from assembler.b_type import b_to_bin
from assembler.u_type import u_to_bin
from assembler.s_type import s_to_bin
from assembler.store import I_Type,R_Type,B_Type

data_file = sys.argv[1]
out_file = sys.argv[2]
with open(data_file,"r") as f:
    data = [i.strip() for i in f.readlines()]

def labels(data):
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

wdata = []
pc=0
labels = labels(data)
for i in data:
    if ":" in i:
        temp = i.split(":")
        if temp[1].strip()=="":
            continue
        instruction = temp[1].strip()
    instruction=i
    operation = instruction.split()[0]

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


with open(out_file,"w") as f:
    for i in wdata:
        f.write(i+'\n')