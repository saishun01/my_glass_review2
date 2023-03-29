import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

MAXCYCLE = 10
MAXCYCLE2 = 40
V0 = 5
TMAX = 1.3
dt = 0.01
np.random.seed(10) # 保存したときの値は10

g = 1
kg = 1

n1 = 1
n2 = 1

k1 = 10
k2 = 10
k3 = 15
k4 = 15

k13 = 0 # k1,k2=10, k3,k4=1としたとき，ここが0だとx3,x4はなくなるが，正の値だと残る．
k14 = 0 # 同じく
k23 = 0 # 同じく
k24 = 0 # 同じく
k31 = 0 # k1,k2=10, k3,k4=11としたとき，ここが0だとx3,x4は（勝手に）発散するが，正の値だと留まる．
k32 = 0
k41 = 0
k42 = 0


def dxdt(x,t):
    ddt = np.zeros_like(x)
    ddt[0] = g*kg*x[1] # x[1]が膜を作る
    ddt[1] = 2*k2*x[2] - k1*n1*x[1] - k14*x[1] - k13*x[1] + k31*x[3] + k41*x[4] - kg*x[1]
    ddt[2] = k1*n1*x[1] - k2*x[2] + k32*x[3] + k42*x[4] - k23*x[2] - k24*x[2]
    ddt[3] = 2*k4*x[4] - k3*n2*x[3] - k32*x[3] - k31*x[3] + k13*x[1] + k23*x[2]
    ddt[4] = k3*n2*x[3] - k4*x[4] + k14*x[1] + k24*x[2] - k41*x[4] - k42*x[4]
    for i in range(len(x)-1):
        ddt[1+i] -= ddt[0]*x[1+i]
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

def div_state_random(x,t2):
    x0 = []
    x0.append(x[t2,0]/2)
    for i in range(len(x[0,:])-1):
        new_X0 = np.random.binomial(int(x[t2,1+i]*2*V0), 0.5)
        x0.append(new_X0/V0)
    return x0    

#fig = plt.figure(figsize=(8,6))
#ax = fig.subplots(2,2)

fig = plt.figure(figsize=(8,3))
ax = fig.subplots(1,2)

x0 = [1, 0.1, 0.1, 0.1, 0.1]
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)
t2 = div_time(x,t)
print(t2, x[t2,0])
'''
lineObjects = ax[0,0].plot(t, x[:,0:5])
ax[0,0].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4'))
ax[0,0].set_title("1st generation")
ax[0,0].set_xlim(0,t2*dt)
ax[0,0].set_xlabel("Time")
'''
lineObjects = ax[0].plot(t, x[:,0:5])
ax[0].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4'))
ax[0].set_title("1st generation")
ax[0].set_xlim(0,t2*dt)
ax[0].set_xlabel("Time")

NMAX = MAXCYCLE - 1
for i in range(NMAX):
    x0 = div_state(x,t2)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)
    print(t2, x[t2,0])
'''
lineObjects = ax[0,1].plot(t, x[:,0:5])
#ax[0,1].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4'))
ax[0,1].set_title("{}th generation".format(MAXCYCLE))
ax[0,1].set_xlim(0,t2*dt)
ax[0,1].set_xlabel("Time")
'''
lineObjects = ax[1].plot(t, x[:,0:5])
#ax[0,1].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4'))
ax[1].set_title("{}th generation".format(MAXCYCLE))
ax[1].set_xlim(0,t2*dt)
ax[1].set_ylim(0,max(x[t2,:])*1.1)
ax[1].set_xlabel("Time")
# 記録用
X = x
X0 = div_state(x,t2)
'''
# ここから粒子数の初期値を二項分布で散らしながらシミュレーション
x0_list = []
x0_list.append(X0)

x0 = div_state_random(x,t2)
#print(np.array(x0)-np.array(x[t2,:]))
x0_list.append(x0)
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)    
t2 = div_time(x,t)
lineObjects = ax[1,0].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[1,0].set_title(r"(random $V_0$={}) {}th generation".format(V0,MAXCYCLE+1))
ax[1,0].set_xlim(0,t2*dt)
ax[1,0].set_xlabel("Time")

for i in range(MAXCYCLE2-1):
    x0 = div_state_random(x,t2)
    x0_list.append(x0)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)

lineObjects = ax[1,1].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[1,1].set_title(r"(random $V_0$={}) {}th generation".format(V0,MAXCYCLE+MAXCYCLE2))
ax[1,1].set_xlim(0,t2*dt)
ax[1,1].set_xlabel("Time")
'''
plt.tight_layout()
plt.show()
fig.savefig("riroen/couple_pure_k31={}.png".format(k31))