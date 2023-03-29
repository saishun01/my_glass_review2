import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

n = np.arange(2,6)
de = np.array([6.442,3.172,1.875,0.752])
error = np.array([0.1,0.1,0.1,0.1])
X = np.linspace(1,6,10000)

f = lambda x, a: a*(x-1)**2/x**5
popt, pcov = curve_fit(f,n,de,sigma=error)
print('a: ',popt[0], 'pm', pcov[0][0])

#Y = 6.442*2**5*(X-1)**2/X**5

plt.figure()
plt.scatter(n,de, label='Data')
plt.errorbar(n,de,yerr=error,linestyle="None", capsize=6, linewidth=5)
plt.plot(X, f(X,popt[0]), label=r'$\Delta E = 200(n-1)^2/n^5$')
#plt.plot(X,Y, label=r'$\Delta E \propto (n-1)^2/n^5$')
plt.xlabel(r'$n$')
plt.ylabel(r'Energy width $\Delta E$ (meV)')
#plt.yscale('log')
plt.xlim(1,6)
plt.ylim(0,8)
plt.grid()
plt.legend()
plt.show()