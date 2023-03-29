import numpy as np
import matplotlib.pyplot as plt

def gNa(V):
    bq = 0.5
    V_star = -40
    return 100/(1+np.exp(bq*(V_star-V))) + 1/5

V = np.linspace(-100, 0, 1000)
g = gNa(V)
g_K = 5
plt.plot(V, g, label='Na')
plt.plot([-100, 0], [g_K, g_K], label='K')
plt.xlim(-100,0)
plt.xlabel('Voltage (mV)')
plt.ylabel('Conductance ($\Omega^{-1}$m$^{-2}$)')
plt.legend()
plt.yscale('log')
plt.grid()
plt.show();