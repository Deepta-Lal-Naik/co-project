import sys
sys.path.append("../../assembler")
from r_type import r_to_bin
from j_type import j_to_bin
from b_type import b_to_bin
from u_type import u_to_bin
from s_type import s_to_bin
from i_type import i_to_bin
from store import I_Type,R_Type,B_Type

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
    labels = c_labels(data)
    for i in data:
        try:

            if ":" in i:
                temp = i.split(":")
                if temp[1].strip()=="":
                    continue
                instruction = temp[1].strip()
            else:
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
        except: 
            print((pc/4)+1)
            pc+=4
            wdata.append("0")


    with open(out_file,"w") as f:
        for i in wdata:
            f.write(i+'\n')

if __name__ == "__main__":
    main()
    