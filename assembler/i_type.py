from store import Register_Mapping,twos,I_Type

#Function to convert immediate value to binary
def i_to_bin(cmd):

    if cmd.startswith("lw"):
        parts = cmd.split(maxsplit=1)
        op = parts[0]
        rest = parts[1]
        rest = rest.replace(" ", "")
        rd,addr = rest.split(",")
        imm,rs1 = addr.split("(")
        rs1 = rs1[:-1]

    else:
        parts = cmd.split(maxsplit=1)
        op = parts[0]
        rest = parts[1]
        rest = rest.replace(" ", "")
        rd,rs1,imm = rest.split(",")

    imm = twos(int(imm),12)

    return (
        imm +
        Register_Mapping[rs1] +
        I_Type[op] +
        Register_Mapping[rd] +
        ("0000011" if op=="lw" else "0010011" if op!="jalr" else "1100111")
    )

                        

              



