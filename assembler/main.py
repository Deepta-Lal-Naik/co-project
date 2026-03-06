from i_type import i_to_bin

with open("data.txt","r") as fin:
    L = fin.readlines()
for i in L:
    a = i_to_bin(i)
    print(a)        