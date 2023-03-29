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

#print("a1 = ", popt1[0])
#print("a1_err =", np.sqrt(pcov1[0][0]))
#print("b1 = ", popt1[1])
#print("b1_err =", np.sqrt(pcov1[1][1]))

#NaIのフィッティング
popt2, pcov2 = curve_fit(f, E2, V2, p0=[174,26], sigma=dV2)

#print("a2 = ", popt2[0])
#print("a2_err =", np.sqrt(pcov2[0][0]))
#print("b2 = ", popt2[1])
#print("b2_err =", np.sqrt(pcov2[1][1]))

E1_mu = 2.01
print("pla:", f(E1_mu, popt1[0], popt1[1]))

err_ax1 = np.sqrt(pcov1[0][0]) * E1_mu
err1 = np.sqrt(err_ax1**2 + pcov1[1][1])
print("pla_err:", err1)

E2_mu = 6.08
print("NaI:", f(E2_mu, popt2[0], popt2[1]))
err_ax2 = np.sqrt(pcov2[0][0]) * E2_mu
err2 = np.sqrt(err_ax2**2 + pcov2[1][1])
print("NaI_err:", err2)