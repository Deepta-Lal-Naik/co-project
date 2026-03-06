from store import Register_Mapping,B_Type
def b_to_bin(cmd,labels,pc):

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rs1,rs2,label = rest.split(",")

    if label in labels:
        offset = labels[label] - pc
    else:
        offset = int(label)
    imm = twos(offset>>1,12)

    return (
        imm[0] +
        imm[2:8] +
        Register_Mapping[rs2] +
        Register_Mapping[rs1] +
        B_Type[op] +
        imm[8:] +
        imm[1] +
        "1100011"
    )
