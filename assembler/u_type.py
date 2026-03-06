from store import Register_Mapping,U_Type,twos
REGISTER_MAPPING = Register_Mapping
u_type_info=U_Type

def u_to_bin(cmd):  

    parts = cmd.split(maxsplit=1)
    op = parts[0]
    rest = parts[1]
    rest = rest.replace(" ", "")
    rd,imm = rest.split(",")

    imm = twos(int(imm),20)

    return (
        imm +
        Register_Mapping[rd] +
        ("0110111" if op=="lui" else "0010111")
    )
