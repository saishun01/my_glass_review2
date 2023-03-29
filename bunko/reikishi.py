import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

lam = np.array([578.25,574.55,573.25,572.55])
lam_true = lam + 1.7
energy = 1239.8/lam_true

N = np.array([2,3,4,5])
N_2 = 1/N**2

f = lambda x, a, b: a*x + b
popt, pcov = curve_fit(f, N_2, energy)
print(popt,pcov)

plt.figure()
plt.scatter(N_2, energy)
X = np.linspace(0,0.3)
plt.plot(X, f(X,popt[0],popt[1]))
plt.xlabel(r'$1/n^2$')
plt.ylabel(r'Energy (eV)')
plt.grid()
plt.show()
