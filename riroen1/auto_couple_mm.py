import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

Va1 = 1
Va2 = 1
Vb1 = 5
Vb2 = 5
Vc1 = 1
Vc2 = 10
Ka1 = 1
Ka2 = 1
Kb1 = 10
Kb2 = 10
Kc1 = 10
Kc2 = 1

def dxdt(state,t):
    X1, X2 = state
    ddt = np.zeros_like(state)
    ddt[0] = Va1*X1/(Ka1 + X1) - Vb1*X1/(Kb1 + X1) + Vc2*X2/(Kc2 + X2) - Vc1*X1/(Kc1 + X1)
    ddt[1] = Va2*X2/(Ka2 + X2) - Vb2*X2/(Kb2 + X2) + Vc1*X1/(Kc1 + X1) - Vc2*X2/(Kc2 + X2)
    return ddt

x0 = [0.1, 0.1]
t = np.arange(0, 30, 0.01)
x = odeint(dxdt, x0, t)

plt.figure()
plt.plot(t, x)
plt.yscale('log')
plt.show()