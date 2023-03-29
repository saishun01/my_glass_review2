import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

N = np.array([2, 3, 4, 5])
E = np.array([2.137586, 2.151497, 2.156737, 2.158990])
E_th = np.array([2.1466558270854224,2.1596248120379653,2.1641639567713558,2.1662649323336676])
print(E-E_th)

N_2 = 1/N**2

f = lambda x,R,Eg:Eg-R*x
popt, pcov = curve_fit(f, N_2, E)
R_err = np.sqrt(pcov[0][0])
Eg_err = np.sqrt(pcov[1][1])

print('R:',popt[0], R_err)
print('Eg:',popt[1], Eg_err)

plt.scatter(N_2, E)

X = np.linspace(0, 1)
plt.plot(X, f(X,popt[0],popt[1]))
plt.xlim(0,0.3)
plt.ylim(2.13,2.17)

plt.xlabel(r'$1/n^2$')
plt.ylabel(r'Energy (eV)')
#plt.yscale('log')
plt.grid()
plt.show()