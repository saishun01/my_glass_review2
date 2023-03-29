import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

Ns = 10
p = 0.1
fp = 0.1

dt = 0.1
g = 1
kg = 1
e = 1
D = 1
n = 1

Rlist = []
chem = [i for i in range(Ns)]

def dead_or_alive(MAXCYCLE, TMAX):

    doa_list = []
    for s in range(10):
        for i in range(Ns):
            for j in range(Ns):
                if i == j:
                    continue
                else:
                    if np.random.rand() < p:
                        Rlist.append([i,j,random.choice(chem)])

        def dxdt(state,t):
            ddt = np.zeros_like(state)
            V = state[0]
            x = state[1:] 
            ddt[0] = g*kg*x[0]*V # x[0]が膜分子だと考える
            ddt[1+0] -= kg*x[0]
            for r in range(len(Rlist)):
                i,j,k = Rlist[r]
                ddt[1+j] += e*x[i]*x[k]
                ddt[1+i] -= e*x[i]*x[k]
            for i in range(len(x)):
                ddt[1+i] -= ddt[0]/V*x[i]
            for i in range(int(len(x)*fp)):
                ddt[2+i] += D*(n-x[1+i]) # 全成分のうちfpの割合が出入りする（膜分子は除く）
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

        x0 = np.ones(1+Ns) # 時間発展させたい体積・濃度
        t = np.arange(0,TMAX,dt)
        x = odeint(dxdt, x0, t)
        t2 = div_time(x, t)

        NMAX = MAXCYCLE - 1
        x0_list = [x0]
        for i in range(NMAX):
            x0 = div_state(x,t2)
            x0_list.append(x0)
            t = np.arange(0, TMAX, dt)
            x = odeint(dxdt, x0, t)    
            t2 = div_time(x,t)
        
        if x0_list[-1][0] > 1:
            doa_list.append(1)
        else:
            doa_list.append(0)
        
    return doa_list

print(dead_or_alive(100,10))