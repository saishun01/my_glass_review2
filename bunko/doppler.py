import numpy as np

kg_to_eV = 5.60959 #from 1e-35kg to eV
mp = 1.66 * 10**8 *kg_to_eV
me = 0.91 * 10**4 * kg_to_eV
kB = 8.62*10**(-5)
T = 300

beta = np.sqrt(3*kB*T/(me+mp))
f_larger = np.sqrt((1+beta)/(1-beta))
f_smaller = np.sqrt((1-beta)/(1+beta))
print(f_larger-1, f_smaller-1)

c = 2.9979 * 10**8
lam = 10**(-7)
dlam = 10**(-10)

f = c/lam
df = c/lam**2*dlam
print(df/f)
