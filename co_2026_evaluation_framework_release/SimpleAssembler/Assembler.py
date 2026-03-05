import sys
sys.path.append('../../assembler')
from r_type import r_to_bin
from j_type import j_to_bin
from s_type import s_to_bin
from u_type import u_to_bin
from b_type import b_to_bin
from i_type import i_to_bin

def createLabels(data):
    d={}
    pc=0
    for i in data:
        if ":" in i:
            temp = i.split(":")
            d[temp[0]]=pc
        pc+=4
    
    return d
            

data_file = sys.argv[1]
output_file = sys.argv[2]
with open(data_file,"r") as f:
    data = f.readlines()
pc=0
labels = createLabels(data)
operations = ["add","sub","sll","slt","sltu","xor","srl","sra","or","and","jal","sw","auipc","lui"]

for i in data:
    temp = i.split(" ")
    if temp[0] in operations[0:10]:
        wdata = r_to_bin(i)

    elif temp[0]==operations[10]:
        label = temp[1].split(",")[1]
        if label in labels:
            wdata = j_to_bin(i,pc,labels[label])
        else:
            wdata = j_to_bin(i,int(label))
    elif temp[0]==operations[11]:
        wdata = s_to_bin(i)

    elif temp[0] in operations[12:14]:
        wdata = u_to_bin(i)


    



