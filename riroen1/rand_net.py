import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

Ns = 10

MAXCYCLE = 10
TMAX = 10
dt = 0.1
g = 1
kg = 1
e = 1

p = 0.1

D = 1
n = 1
fp = 0.1

#Nr = 2
#SM = np.zeros((Ns,Nr))
Rlist = []
#Clist = []
chem = [i for i in range(Ns)]
'''
for i in range(Nr):
    #reac = np.random.randint(0, Ns, 3) # [reactant, product, catalyst]
    reac = random.sample(chem, 2) # [reactant, product]
    cata = random.choice(chem) # catalyst
    #print(reac, cata)
    SM[reac[0],i] = - 1
    SM[reac[1],i] = 1
    Clist.append(cata)
print(SM)
'''


#SM = []
for i in range(Ns):
    for j in range(Ns):
        if i == j:
            continue
        else:
            if np.random.rand() < p:
                #sm = np.zeros(Ns)
                #sm[i] = - 1
                #sm[j] = 1
                #SM.append(sm)
                Rlist.append([i,j,random.choice(chem)])
                #Clist.append(random.choice(chem))

#SM = np.array(SM).T
#print(SM)
print(Rlist)


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
        ddt[1+i] -= g*kg*x[0]*x[i]
        #ddt[1+i] -= ddt[0]/V*x[i]
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
#print(t2*dt)

fig = plt.figure(figsize=(10,3))
ax = fig.subplots(1,3)

lineObjects = ax[0].plot(t, x)
ax[0].legend(iter(lineObjects), ('V', 'mem'))
ax[0].set_title("1st generation")
ax[0].set_xlim(0,t2*dt)
ax[0].set_ylim(0,1.1*max(x[t2,:]))
ax[0].set_xlabel("Time")

NMAX = MAXCYCLE - 1
x0_list = [x0]
for i in range(NMAX):
    x0 = div_state(x,t2)
    x0_list.append(x0)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)

for i in range(7):
    ddens = x[t2,i] - x[0,i]
    print("ddens of i={} is {:.4f}".format(i,ddens))


lineObjects = ax[1].plot(t, x)
ax[1].legend(iter(lineObjects), ('V', 'mem'))
ax[1].set_title("{}th generation".format(MAXCYCLE))
ax[1].set_xlim(0,t2*dt)
ax[1].set_ylim(0,1.1*max(x[t2,:]))
ax[1].set_xlabel("Time")

lineObjects = ax[2].plot(x0_list)
ax[2].legend(iter(lineObjects), ('V', 'mem'))
ax[2].set_xlabel('Generation')
ax[2].set_ylabel('Initial state')

plt.tight_layout()
plt.show()