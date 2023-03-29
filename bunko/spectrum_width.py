import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

SCANSPEED = 6
PAPERSPEED = 500
pm_mm = SCANSPEED/PAPERSPEED*1000

delta_x = np.array([5,10,20,30,40,50,100,150,200])
#delta_y = np.array([4,7,6,7,9,12,23,36,47])
delta_y = np.array([5,6,6,8,9,12,24,36,47])
delta_y_err = np.ones(9) * 0.5

delta_lam = pm_mm*delta_y
delta_lam_err = pm_mm*delta_y_err

print(delta_lam)

f = lambda x, a, b: a*x + b

nc = 4
popt, pcov = curve_fit(f,delta_x[nc:], delta_lam[nc:], sigma=delta_lam_err[nc:])
a_err = np.sqrt(pcov[0][0])
b_err = np.sqrt(pcov[1][1])
print('a:', popt[0], a_err)
print('b:', popt[1], b_err)

plt.figure()
#plt.scatter(delta_x, delta_lam)
plt.errorbar(delta_x, delta_lam, yerr=delta_lam_err, linestyle="None", capsize=6, linewidth=5, label='Data')

X = np.linspace(0,300)
plt.plot(X,f(X,popt[0],popt[1]), label='$\Delta \lambda = 2.86\Delta x$')

plt.xlim(0,210)
plt.ylim(0,600)
plt.xlabel(r'Slit width $\Delta x$ (um)')
plt.ylabel(r'Spectrum width $\Delta \lambda$ (pm)')
plt.grid()
plt.legend()
plt.show()