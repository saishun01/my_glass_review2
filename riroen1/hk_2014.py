import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

fig = plt.figure(figsize=(10,3))
ax = fig.subplots(1,3)

kx = 1
ky = 1
k = 1
l = 1
p = 1
g = 1

s = 1

def dndt(state,t):
    x, y, V = state
    dxdt = np.zeros_like(state)
    lamb = g*p*y
    dxdt[0] = kx*x*(k*s - x) - x*lamb
    dxdt[1] = ky*x*(l*s - y) - p*y - y*lamb
    dxdt[2] = lamb*V
    return dxdt 


n0 = [0.1, 0.1, 0.1]
t = np.arange(0, 20, 0.01)

x = odeint(dndt, n0, t)
lineObjects = ax[0].plot(t, x[:,0:3])
ax[0].legend(iter(lineObjects), ('x', 'y', 'V'))
ax[0].set_yscale('log')
ax[0].set_title("Growth")
plt.show()