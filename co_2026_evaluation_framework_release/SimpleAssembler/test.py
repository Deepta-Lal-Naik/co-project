import sys

sys.path.append('../../assembler')

from r_type import r_to_bin
from j_type import j_to_bin
from s_type import s_to_bin
from u_type import u_to_bin
from b_type import b_to_bin
from i_type import i_to_bin


def createLabels(data):
    labels = {}
    pc = 0

    for line in data:
        line = line.strip()

        if ":" in line:
            temp = line.split(":")
            label = temp[0].strip()
            labels[label] = pc

        pc += 4

    return labels


data_file = sys.argv[1]
output_file = sys.argv[2]

with open(data_file, "r") as f:
    data = f.readlines()

# clear output file
open(output_file, "w").close()

pc = 0
labels = createLabels(data)

operations = [
    "add","sub","sll","slt","sltu","xor","srl","sra","or","and",
    "jal","sw","auipc","lui",
    "beq","bne","blt","bge","bltu","bgeu",
    "lw","addi","sltiu","jalr"
]

for line in data:

    line = line.strip()
    temp = line.split()

    # remove label if present
    if ":" in line:
        operation = temp[1]
        instruction = line.split(":")[1].strip()
    else:
        operation = temp[0]
        instruction = line

    if operation in operations[0:10]:
        wdata = r_to_bin(instruction)

    elif operation == operations[10]:  # jal
        parts = instruction.split()
        target = parts[1].split(",")[1]

        if target in labels:
            wdata = j_to_bin(instruction, pc, labels[target])
        else:
            wdata = j_to_bin(instruction, pc, int(target))

    elif operation == operations[11]:  # sw
        wdata = s_to_bin(instruction)

    elif operation in operations[12:14]:  # auipc, lui
        wdata = u_to_bin(instruction)

    elif operation in operations[14:20]:  # branch
        wdata = b_to_bin(instruction, pc, labels)

    elif operation in operations[20:24]:  # I-type
        wdata = i_to_bin(instruction)

    else:
        wdata = "Invalid assembly command"

    pc += 4

    with open(output_file, "a") as f:
        f.write(wdata + "\n")