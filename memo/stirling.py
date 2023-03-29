import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

NMAX = 10
n_list = np.arange(1,NMAX)
n_fact = factorial(n_list)

f = lambda n: np.power(n,n)*np.exp(-n)*np.sqrt(2*np.pi*n)
n_stir = f(n_list)

plt.figure()
plt.plot(n_list,n_fact)
plt.plot(n_list,n_stir)
plt.yscale('log')
plt.show()
