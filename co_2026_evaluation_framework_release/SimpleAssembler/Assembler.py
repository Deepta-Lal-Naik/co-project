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
operations = ["add","sub","sll","slt","sltu","xor","srl","sra","or","and","jal","sw","auipc","lui",
              "beq","bne","blt","bge","bltu","bgeu","lw","addi","sltiu","jalr"]

for i in data:
    i=i.strip()
    temp = i.split(" ")
    if ":" in i:
        line_label = temp[0][:-1]
        operation = temp[1]
    else:
        operation = temp[0]

    if operation in operations[0:10]:
        wdata = r_to_bin(i)

    elif operation==operations[10]:
        temp1 = i.split()
        target = temp1[1].split(",")[1]
        if target in labels:
            wdata = j_to_bin(i,pc,labels[target])
        else:
            wdata = j_to_bin(i,pc,int(target))

    elif operation==operations[11]:
        wdata = s_to_bin(i)
    elif operation in operations[12:14]:
        wdata = u_to_bin(i)
    elif operation in operations[14:20]:
        wdata = b_to_bin(i)
    elif operation in operations[20:24]:
        wdata = i_to_bin(i)
    pc+=4
    with open(output_file,"a") as f:
        f.write(wdata+'\n')

    



