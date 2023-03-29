import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

n2 = np.arange(3,9)
n2_2 = 1/n2**2
wl_obs = np.array([654.88,484.48,432.60,408.78,395.42,387.32])
wl_obs_2 = np.array([654.96,484.54,432.38,408.68,395.46,387.40])
dw_obs = np.abs(wl_obs - wl_obs_2)

calib = lambda x: x + 1.7
wl_real = [calib(x) for x in wl_obs]
wl_real_2 = [calib(x) for x in wl_obs_2]
energy = [1239.84/y for y in wl_real]
energy_2 = [1239.84/y for y in wl_real_2]
denergy = np.abs(np.array(energy_2) - np.array(energy))
#denergy = 1239.84*dw_obs/np.power(wl_real,2.0)

f = lambda x, a, R: R*(a - x)
xdata = n2_2
ydata = energy
popt, pcov = curve_fit(f, xdata, ydata, sigma=denergy)
#popt, pcov = curve_fit(f, xdata, ydata)

plt.figure()
plt.scatter(n2_2, energy, label=r'Data')
#plt.errorbar(n2_2,energy,yerr=denergy,linestyle="None", capsize=6, linewidth=5)
X = np.linspace(0, 0.2)
plt.plot(X, f(X,popt[0],popt[1]), label=r'$E = 13.601(0.25 - 1/n_2^2)$')
a_err = np.sqrt(pcov[0][0])
R_err = np.sqrt(pcov[1][1])
print('1/n1^2: ', popt[0], a_err)
print('R:', popt[1], R_err)
plt.xlim(0,0.2)
plt.ylim(0.5,3.5)

plt.xlabel(r'$1/n_2^2$')
plt.ylabel(r'E (eV)')
plt.grid()
plt.legend()
plt.show()