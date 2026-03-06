from i_type import i_to_bin

with open("data.txt","r") as fin:
    L = fin.readlines()
try:
    for i in L:
        a = i_to_bin(i)
        print(a)        
except:
    raise Exception("wrong")   