import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

E1 = [0.478, 0.341, 1.062]
V1 = [50, 40, 110]
dV1 = [5, 5, 5]

def f(x, a, b):
    return a*x + b

#プラシンのフィッティング
popt1, pcov1 = curve_fit(f, E1, V1, p0=[70,9] ,sigma=dV1)

print("a1 = ", popt1[0])
print("a1_err =", np.sqrt(pcov1[0][0]))
print("b1 = ", popt1[1])
print("b1_err =", np.sqrt(pcov1[1][1]))

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