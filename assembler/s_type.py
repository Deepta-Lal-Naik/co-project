from store import Register_Mapping,S_Type,twos
REGISTER_MAPPING = Register_Mapping
s_type_info=S_Type

def s_to_bin(cmd):

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rs2,addr = rest.split(",")

    imm,rs1 = addr.split("(")
    rs1 = rs1[:-1]

    imm = twos(int(imm),12)

    return (
        imm[:7] +
        Register_Mapping[rs2] +
        Register_Mapping[rs1] +
        "010" +
        imm[7:] +
        "0100011"
    )
