import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

TMAX = 10**12 # 10**(12) when himeoka_trans
dt = 10**(-7)*TMAX # 10**(-7)*TMAX when himeoka_trans

v = 0.1 # 0.1
K = 1 # 1
Kt = 10 # 10
kp = 1 # 1
km = 10**(-6) # 10**(-6)
dA = 10**(-5) # 10**(-5)
dB = 10**(-5) # 10**(-5)
dC = 10**(-12) # 10**(-12)


def FA(S):
    return v*S/(K+S)*S/(Kt+S) # himeoka error
    #return v*S # riroen error

def FB(S):
    return v*S/(K+S)*Kt/(Kt+S) # himeoka error
    #return v*S*Kt/(Kt+S) # riroen error

def G(A,B,C):
    return kp*A*B-km*C

Sext_indices = np.arange(-5,6,0.2) # for himeoka error
#Sext_indices = np.arange(-10,3,0.5) # for riroen error
print(Sext_indices)
t_lists = []
x_lists = []
nuts = []
mus = []
As = []

for i in range(len(Sext_indices)):
    Sext = 10**(Sext_indices[i].tolist())
    nuts.append(Sext)

    # x = [S, A, B, C]
    def dxdt(x, t):
        # non-negative
        for i in range(len(x)):
            if x[i] < 0:
                x[i] = 0
        ddt = np.zeros_like(x)

        # dilution and decay
        mu = FA(x[0])*x[1]
        d = [0, dA, dB, dC]
        for i in range(len(x)):
            ddt[i] += - mu*x[i] - d[i]*x[i]
        
        # diffusion
        ddt[0] += x[1]*(Sext - x[0]) # A is transporter
        #ddt[0] += 1*(Sext - x[0]) # constant diffusion

        # chemical reaction
        ddt[0] += - FA(x[0])*x[1] - FB(x[0])*x[1]
        ddt[1] += FA(x[0])*x[1] - G(x[1],x[2],x[3])
        ddt[2] += FB(x[0])*x[1] - G(x[1],x[2],x[3])
        ddt[3] += G(x[1],x[2],x[3])

        return ddt

    x0 = np.zeros(4) # 時間発展させたい濃度
    for i in range(2):
        x0[i] = 1.0

    t_list = np.arange(0,TMAX,dt)
    x_list = odeint(dxdt, x0, t_list)

    t_lists.append(t_list)
    x_lists.append(x_list)

    #mu_list = []
    #for i in range(len(x_list)):
    #    mu_list.append(FA(x_list[i,0])*x_list[i,1])
    
    mu = FA(x_list[-1,0])*x_list[-1,1]
    mus.append(mu)
    As.append(x_list[-1,1])

fig = plt.figure()
ax = fig.add_subplot(111)

#for i in range(len(x_list[0,:])):
#    ax.plot(t_list,x_list[:,i], label='{}'.format(i))


ax.scatter(nuts,mus, label='mu')
ax.scatter(nuts,As, label='A')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel('Sext')
print('mus = {}'.format(mus))
print('As = {}'.format(As))

ax.set_ylim(10**(-20),10**1)
plt.legend()
plt.show()