import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

E1 = [0.478, 0.341, 1.062]
V1 = [50, 30, 83]
dV1 = [10, 7, 7]

E2 = [0.662, 0.511, 1.275]
V2 = [130, 118, 250]
dV2 = [10, 6, 10]

def f(x, a, b):
    return a*x + b

#プラシンのフィッティング
popt1, pcov1 = curve_fit(f, E1, V1, p0=[70,9] ,sigma=dV1)

print("a1 = ", popt1[0])
print("a1_err =", np.sqrt(pcov1[0][0]))
print("b1 = ", popt1[1])
print("b1_err =", np.sqrt(pcov1[1][1]))

#NaIのフィッティング
popt2, pcov2 = curve_fit(f, E2, V2, p0=[174,26], sigma=dV2)

print("a2 = ", popt2[0])
print("a2_err =", np.sqrt(pcov2[0][0]))
print("b2 = ", popt2[1])
print("b2_err =", np.sqrt(pcov2[1][1]))

#プラシンの図
X = 1.3
fig = plt.figure()
plt.errorbar(E1, V1, dV1, fmt='o', capsize=5, label='Measured')#, ecolor = 'black', markeredgecolor='black', color='w')
x = np.linspace(0, X)
y = f(x,popt1[0],popt1[1])
plt.plot(x,y, color='black', label='Caliburation line')

plt.xlim(0, X)
plt.ylim(0, f(X,popt1[0],popt1[1]))
plt.xlabel('Energy$\,$(MeV)')
plt.ylabel('Voltage$\,$(mV)')
plt.legend()
plt.grid()
plt.show()

#NaIの図
X = 1.5
fig = plt.figure()
plt.errorbar(E2, V2, dV2, fmt='o', capsize=5, label='Measured')#, ecolor = 'black', markeredgecolor='black', color='w')
x = np.linspace(0, X)
y = f(x,popt2[0],popt2[1])
plt.plot(x,y, color='black', label='Caliburation line')

plt.xlim(0, X)
plt.ylim(0, f(X,popt2[0],popt2[1]))
plt.xlabel('Energy$\,$(MeV)')
plt.ylabel('Voltage$\,$(mV)')
plt.legend()
plt.grid()
plt.show()


