import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

N = 1
g = 1
k1 = 1
k2 = 100
k3 = 100
k4 = 100
kg = 1
TMAX = 10
dt = 0.1
MAXCYCLE = 10

def dxdt(x,t):
    ddt = np.zeros_like(x)
    ddt[0] = g*kg*x[1]
    ddt[1] = -k1*N*x[1] + k2*x[2] + k4*x[4] - g*kg*x[1]
    ddt[2] = k1*N*x[1] - k2*x[2]
    ddt[3] = k2*x[2] - k3*x[3]*x[5]
    ddt[4] = k3*x[3]*x[5] - k4*x[4]
    ddt[5] = - k3*x[3]*x[5] + k4*x[4]
    return ddt

def div_time(x, t):
    t2 = -1
    for i in range(len(t)):
        if float(x[i,0]) > 2:
            t2 = i
            break
    return t2

def div_state(x, t2):
    x0 = []
    x0.append(x[t2,0]/2)
    for i in range(len(x[0,:])-1):
        x0.append(x[t2,1+i])
    return x0

fig = plt.figure(figsize=(8,6))
ax = fig.subplots(2,2)

x0 = [1, 1, 0, 0, 0, 10]
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)
t2 = div_time(x,t)
print(t2, x[t2,0])

lineObjects = ax[0,0].plot(t, x[:,0:6])
ax[0,0].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4', 'x5'))
ax[0,0].set_title("1st generation")
ax[0,0].set_xlim(0,t2*dt)

NMAX = MAXCYCLE - 1
for i in range(NMAX):
    x0 = div_state(x,t2)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)
    print(t2, x[t2,0])

lineObjects = ax[0,1].plot(t, x[:,0:6])
ax[0,1].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4', 'x5'))
ax[0,1].set_title("{}th generation".format(MAXCYCLE))
ax[0,1].set_xlim(0,t2*dt)

plt.tight_layout()
plt.show()

'''
# 1細胞周期スケールの時間発展
plt.figure()
lineObjects = plt.plot(t, x[:,0:5])
plt.legend(iter(lineObjects), ('X1', 'X2', 'X3', 'X4', 'X5'))
plt.yscale('log')
plt.show()
'''
'''
# 数細胞周期スケールの時間発展
x_list = []
for i in range(20):
    x0 = x[-1,:]
    x = odeint(dxdt, x0, t)
    x_list.append(x[-1,:])
plt.figure()
lineObjects = plt.plot(x_list)
plt.legend(iter(lineObjects), ('X1', 'X2', 'X3', 'X4', 'X5'))
plt.yscale('log')
plt.show()
'''
'''
# 初期値に対する安定性評価
dnu = []
inc = []
ratio = []
NMAX = 4
for i1 in range(NMAX):
    for i2 in range(NMAX):
        for i3 in range(NMAX):
            for i4 in range(NMAX):
                k1 = 10**(i1-1)
                k2 = 10**(i2-1)
                k3 = 10**(i3-1)
                k4 = 10**(i4-1)
                x = odeint(dxdt, x0, t)
                dnum = np.array(x[-1,:] - x0).max() - np.array(x[-1,:] - x0).min()
                incre = np.array(x[-1,:] - x0).mean()
                #print('k1, k2, k3, k4 = {}, {}, {}, {}'.format(k1, k2, k3, k4))
                #print(ddens)
                dnu.append(dnum)
                inc.append(incre)
                ratio.append(dnum/incre)

print(np.base_repr(ratio.index(min(ratio)), NMAX))
fig = plt.figure(figsize=(8,2))
ax = fig.subplots(1,3)
ax[0].plot(dnu)
ax[1].plot(inc)
ax[1].set_yscale('log')
ax[2].plot(ratio)
plt.show()
'''