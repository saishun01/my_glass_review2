import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

Ns = 10
#p = 0.1

dt = 0.1
g = 1
kg = 1
e = 1
D = 1
n = 1

def dead_or_alive(Ns, p, f, Nseed, MAXCYCLE, TMAX):

    chem = [i for i in range(Ns)]

    doa_list = []
    for s in range(Nseed):
        Rlist = []
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
            for i in range(int(f*Ns)): # 栄養分子の数変更
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

#Nseed = 10
'''
Nseed = 30
p_alive_list = []
p_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
#p_list = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14]
#p_list = [0, 0.02, 0.04, 0.06, 0.08, 0.1]
for i in range(len(p_list)):
    result = dead_or_alive(Ns=Ns, p=p_list[i], f=0.1 Nseed=Nseed, MAXCYCLE=10, TMAX=10)
    count = 0    
    for j in range(len(result)):
        if result[j] == 1:
            count += 1
    p_alive_list.append(count/Nseed)

plt.scatter(p_list, p_alive_list)
'''

Nseed = 60
p = 0.9
p_alive_list = []
f_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for i in range(len(f_list)):
    result = dead_or_alive(Ns=Ns, p=0.3, f=f_list[i], Nseed=Nseed, MAXCYCLE=10, TMAX=10)
    count = 0    
    for j in range(len(result)):
        if result[j] == 1:
            count += 1
    p_alive_list.append(count/Nseed)

plt.scatter(f_list, p_alive_list)


'''
# 補助線
Ns = 10
p_list = np.arange(0,1,0.01)
q_list = []
for i in range(len(p_list)):
    p = p_list[i]

    q = p
    for i in range(2,Ns):
        q = q*(1+(1-q)*p)
    q_list.append(q)

plt.plot(p_list,q_list)
'''
#plt.xlabel(r'Connection rate $p$')
plt.xlabel(r'Proportion of nutrition $f$')
plt.ylabel('Probability of survival')
plt.show()
