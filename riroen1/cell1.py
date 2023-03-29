import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

k = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #k[0]=3にすると半死
d = [0, 1, 0, 0, 0, 1, 0, 1/3, 0, 0, 0, 0]
a = 1 # 栄養の吸引力（膜面積当たり）
b = 1 # 成長速度


def dxdt(state, t):
    N = state[0]
    V = state[1]
    X = state[2:]
    
    r = np.zeros(len(k))
    for i in range(len(k)):
        r[i] = k[i]/np.power(V, d[i])
    
    ddt = np.zeros_like(state)
    ddt[0] = -(r[0]+r[4]+r[8])*N + a*np.power(V, 2/3) # N
    ddt[1] = b*r[7]*X[6]*np.power(V, 1/3) # V
    ddt[2+0] = r[0]*N - r[1]*X[0]*X[2] # X0
    ddt[2+1] = r[1]*X[0]*X[2] - (r[2]+r[3])*X[1] # X1
    ddt[2+2] = (2*r[2]+r[3])*X[1] - r[1]*X[0]*X[2] # X2
    ddt[2+3] = r[3]*X[1] - r[5]*X[3]*X[4] + r[6]*X[5] # X3
    ddt[2+4] = r[4]*N - r[5]*X[3]*X[4] # X4
    ddt[2+5] = r[5]*X[3]*X[4] - r[6]*X[5] # X5
    ddt[2+6] = r[6]*X[5] - r[7]*X[6] #X6
    return ddt

fig = plt.figure(figsize=(12,6))
# ax = fig.subplots(1,3)
ax = fig.subplots(2,3)


x0 = [1, 1, 0, 0, 0.1, 0, 0, 0, 0]
t = np.arange(0, 10, 0.01)
x = odeint(dxdt, x0, t)
for i in range(len(t)):
    if float(x[i,1]) > 2:
        t2 = i
        break
#print(t2)

lineObjects = ax[0,0].plot(t, x[:,0:9])
ax[0,0].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[0,0].set_title("1st generation")
ax[0,0].set_xlim(0,t2*0.01)
ax[0,0].set_ylim(0, 3)

x0 = np.array(x[t2,:])/2
t = np.arange(0, 5, 0.01)
x = odeint(dxdt, x0, t)
for i in range(len(t)):
    if float(x[i,1]) > 2:
        t2 = i
        break
lineObjects = ax[0,1].plot(t, x[:,0:9])
#ax[0,1].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[0,1].set_title("2nd generation")
ax[0,1].set_xlim(0,t2*0.01)
ax[0,1].set_ylim(0, 3)


x0 = np.array(x[t2,:])/2
t = np.arange(0, 5, 0.01)
x = odeint(dxdt, x0, t)
for i in range(len(t)):
    if float(x[i,1]) > 2:
        t2 = i
        break
lineObjects = ax[0,2].plot(t, x[:,0:9])
#ax[0,2].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[0,2].set_title("3rd generation")
ax[0,2].set_xlim(0,t2*0.01)
ax[0,2].set_ylim(0, 3)

NMAX = 97
for i in range(NMAX):
    x0 = np.array(x[t2,:])/2
    t = np.arange(0, 5, 0.01)
    x = odeint(dxdt, x0, t)    
    for j in range(len(t)):
        if float(x[j,1]) > 2:
            t2 = j
            break
lineObjects = ax[1,0].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[1,0].set_title("{}th generation".format(NMAX+3))
ax[1,0].set_xlim(0,t2*0.01)
ax[1,0].set_ylim(0, 3)

dens = []
dens_n = []
for j in range(len(t)):
        dens_n.append(x[j,0]/x[j,1])
dens.append(dens_n)

for i in range(7):
    dens_i = []
    for j in range(len(t)):
        dens_i.append(x[j,i+2]/x[j,1])
    dens.append(dens_i)
dens = np.array(dens).T
lineObjects = ax[1,1].plot(t, dens)
ax[1,1].legend(iter(lineObjects), ('N', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[1,1].set_title("Density in {}th generation".format(NMAX+3))
ax[1,1].set_xlim(0,t2*0.01)
ax[1,1].set_ylim(0,0.6)
for i in range(7):
    ddens = dens[-1,i] - dens[0,i]
    print("ddens of i={} is {:.4f}".format(i,ddens))

x0 = np.array(x[t2,:])/2
#t = np.arange(0, 100, 0.1)
t = np.arange(0, 30, 0.1)
x = odeint(dxdt, x0, t)
lineObjects = ax[1,2].plot(t, x[:,0:9])
#ax[1,2].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[1,2].set_title("Growth after {}th generation".format(NMAX+3))
#ax[1,2].set_ylim(10**(-2), 10**(5))
ax[1,2].set_ylim(10**(-2), 10**(3))
ax[1,2].set_yscale('log')

'''
d[4] = 0
x = odeint(dxdt, x0, t)
lineObjects = ax[0].plot(t, x[:,0:9])
ax[0].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[0].set_yscale('log')
ax[0].set_title("Growth for d4 = {}".format(d[4]))
ax[0].set_ylim(10**(-3), 10**6)

d[4] = 1
x = odeint(dxdt, x0, t)
lineObjects = ax[1].plot(t, x[:,0:9])
ax[1].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[1].set_yscale('log')
ax[1].set_title("Growth for d4 = {}".format(d[4]))
ax[1].set_ylim(10**(-3), 10**6)

d[4] = 2
x = odeint(dxdt, x0, t)
lineObjects = ax[2].plot(t, x[:,0:9])
ax[2].legend(iter(lineObjects), ('N', 'V', 'amino', 'X1', 'rib', 'enzyme', 'X4', 'X5', 'plipid'))
ax[2].set_yscale('log')
ax[2].set_title("Growth for d4 = {}".format(d[4]))
ax[2].set_ylim(10**(-3), 10**6)
'''
plt.tight_layout()
plt.show()
#fig.savefig("riroen/cell_{}gen.png".format(NMAX+3))