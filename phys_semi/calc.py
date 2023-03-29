import numpy as np
z = float(input("z:"))
c_in = float(input("c_in:"))
c_out = float(input("c_out:"))
def V_ner(z, c_in, c_out):
    return 27/z*np.log(c_out/c_in)
print(V_ner(z, c_in, c_out))
