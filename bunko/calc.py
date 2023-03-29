import numpy as np
E = lambda n: 13.6*(1/4 - 1/n**2)
lam = lambda x: 1239.8/x
print([lam(E(n)) for n in range(3,9)])