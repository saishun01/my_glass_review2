import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

fig = plt.figure(figsize=(10,6))
ax = fig.subplots(2,3)

k1 = 1
k_1 = 0.1
k2 = 1
k3 = 1
a = 1
b = 1
d = 2 # 反応速度が体積の何乗で小さくなるか（拡散しないなら0，拡散しきるなら2．）

def dxdt(state, t):
    N, X1, X2, Y, V = state
    dxdt = np.zeros_like(state)
    dxdt[0] = -k1*N*X1/np.power(V, d) + a*Y 
    dxdt[1] = 2*k2*X2 - k3*X1
    dxdt[2] = k1*N*X1/np.power(V, d) - k_1*X2 - k2*X2 
    dxdt[3] = k3*X1
    dxdt[4] = b*X1*np.power(Y, 0.5) 
    return dxdt


'''
lineObjects = ax[0].plot(t, x[:,4])
ax[0].legend(iter(lineObjects), ('V'))
ax[0].set_yscale('log')
ax[0].set_title("Growth of volume")

lineObjects = ax[1].plot(t, x[:,0:4])
ax[1].legend(iter(lineObjects), ('N', 'X1', 'X2', 'Y'))
ax[1].set_yscale('log')
ax[1].set_title("Growth of components")
'''

x0 = [1, 0.1, 0, 0.01, 0.1]
t = np.arange(0, 20, 0.01)
d_list = [0, 1, 2]

for i in range(0, 3):
    d = d_list[i]
    x = odeint(dxdt, x0, t)
    lineObjects = ax[0,i].plot(t, x[:,0:5])
    ax[0,i].legend(iter(lineObjects), ('N', 'X1', 'X2', 'Y', 'V'))
    ax[0,i].set_yscale('log')
    ax[0,i].set_title("Growth for d = {}".format(d))

    dens = np.zeros_like(x[:,0:4])
    for j in range(4):
        for k in range(len(x[:,0])):
            dens[k,j] = x[k,j]/x[k,4]

    lineObjects = ax[1,i].plot(t, dens[:,0:4])
    ax[1,i].legend(iter(lineObjects), ('n', 'x1', 'x2', 'y'))
    ax[1,i].set_yscale('log')
    ax[1,i].set_title("Density for d = {}".format(d))
    #print("density for d = {}".format(d))
    #print("\t n: {:.2f} -> {:.2f}".format(x[0,0]/x[0,4], x[-1,0]/x[-1,4]))
    #print("\t x1: {:.2f} -> {:.2f}".format(x[0,1]/x[0,4], x[-1,1]/x[-1,4]))
    #print("\t x2: {:.2f} -> {:.2f}".format(x[0,2]/x[0,4], x[-1,2]/x[-1,4]))
    #print("\t y: {:.2f} -> {:.2f}".format(x[0,3]/x[0,4], x[-1,3]/x[-1,4]))

plt.tight_layout()
plt.show()