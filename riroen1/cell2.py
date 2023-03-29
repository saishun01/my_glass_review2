import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

k = [1, 1, 1, 1, 1, 1, 1, 1] #ribosome生成（k2）は重要（遅くすると細胞周期が最も伸びる）．
n = 0.1 #低くすると細胞周期は伸びるが，やはり死にはしない
g = 1
TMAX = 20
dt = 0.1
MAXCYCLE = 10
V0 = 30
MAXCYCLE2 = 40
np.random.seed(10) # 保存したときの値は10

def dxdt(state, t):
    V = state[0]
    x = state[1:]
    
    ddt = np.zeros_like(state)
    ddt[0] = g*k[7]*x[6] # V
    ddt[1+0] = k[0]*n - k[1]*x[0]*x[2] # x0 amino
    ddt[1+1] = k[1]*x[0]*x[2] - (k[2]+k[3])*x[1] # x1
    ddt[1+2] = (2*k[2]+k[3])*x[1] - k[1]*x[0]*x[2] # x2 ribosome
    ddt[1+3] = k[3]*x[1] - k[5]*x[3]*x[4] + k[6]*x[5] # x3 enzyme
    ddt[1+4] = k[4]*n - k[5]*x[3]*x[4] # x4
    ddt[1+5] = k[5]*x[3]*x[4] - k[6]*x[5] # x5
    ddt[1+6] = k[6]*x[5] - k[7]*x[6] #x6 phospholipid
    for i in range(6):
        ddt[1+i] -= ddt[0]*x[i]
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

# 次のプログラムを定常濃度に落ち着くまで回す
# ここから
fig = plt.figure(figsize=(12,10))
ax = fig.subplots(3,3)

x0 = np.array([1, 0, 1, 0, 0, 0, 0, 0]) #V=1は固定．ribosome以外は0でもOK．
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)
t2 = div_time(x,t)

lineObjects = ax[0,0].plot(t, x[:,0:9])
ax[0,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[0,0].set_title("1st generation")
ax[0,0].set_xlim(0,t2*dt)
ax[0,0].set_xlabel("Time")

x0 = div_state(x,t2)
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)

t2 = div_time(x,t)
lineObjects = ax[0,1].plot(t, x[:,0:9])
#ax[0,1].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[0,1].set_title("2nd generation")
ax[0,1].set_xlim(0,t2*dt)
ax[0,1].set_xlabel("Time")

x0 = div_state(x,t2)
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)

t2 = div_time(x,t)
lineObjects = ax[0,2].plot(t, x[:,0:9])
#ax[0,2].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[0,2].set_title("3rd generation")
ax[0,2].set_xlim(0,t2*dt)
ax[0,2].set_xlabel("Time")

NMAX = MAXCYCLE - 3
for i in range(NMAX):
    x0 = div_state(x,t2)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)

lineObjects = ax[1,0].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[1,0].set_title("{}th generation".format(MAXCYCLE))
ax[1,0].set_xlim(0,t2*dt)
ax[1,0].set_xlabel("Time")

# 記録用
X = x
X0 = div_state(x,t2)

#for i in range(7):
#    ddens = x[t2,i] - x[0,i]
#    print("ddens of i={} is {:.4f}".format(i,ddens))
#print(x0)

# ここまで

# ここから粒子数の初期値を二項分布で散らしながらシミュレーション
x0_list = []
x0_list.append(X0)

x0 = div_state_random(x,t2)
#print(np.array(x0)-np.array(x[t2,:]))
x0_list.append(x0)
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)    
t2 = div_time(x,t)
lineObjects = ax[1,1].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[1,1].set_title(r"(random $V_0$={}) {}th generation".format(V0,MAXCYCLE+1))
ax[1,1].set_xlim(0,t2*dt)
ax[1,1].set_xlabel("Time")

for i in range(MAXCYCLE2-1):
    x0 = div_state_random(x,t2)
    x0_list.append(x0)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)

lineObjects = ax[1,2].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[1,2].set_title(r"(random $V_0$={}) {}th generation".format(V0,MAXCYCLE+MAXCYCLE2))
ax[1,2].set_xlim(0,t2*dt)
ax[1,2].set_xlabel("Time")

for i in range(7):
    ddens = x[t2,i] - x[0,i]
    print("ddens of i={} is {:.4f}".format(i,ddens))

lineObjects = ax[2,0].plot(np.arange(MAXCYCLE+0,MAXCYCLE+len(x0_list)),x0_list[:])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[2,0].set_title(r"(random $V_0$={}) {}-{}th generetion".format(V0,MAXCYCLE+1, MAXCYCLE+MAXCYCLE2))
ax[2,0].set_xlabel("Generation")
ax[2,0].set_ylabel(r"Initial state $x_0$")
ax[2,0].set_ylim(0,1.1)

print(len(x0_list))


# （再度）ここから粒子数の初期値を二項分布で散らしながらシミュレーション
V0 = 15
x0_list = []
x0_list.append(X0)

x0 = div_state_random(X,t2)
#print(np.array(x0)-np.array(x[t2,:]))
x0_list.append(x0)
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)    
t2 = div_time(x,t)
lineObjects = ax[2,1].plot(t, x[:,0:9])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[2,1].set_title(r"(random $V_0$={}) {}th generation".format(V0,MAXCYCLE+1))
ax[2,1].set_xlim(0,t2*dt)
ax[2,1].set_xlabel("Time")

for i in range(MAXCYCLE2-1):
    x0 = div_state_random(x,t2)
    x0_list.append(x0)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)    
    t2 = div_time(x,t)

#lineObjects = ax[2,2].plot(t, x[:,0:9])
##ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
#ax[2,2].set_title(r"(random $V_0$={}) {}th generation".format(V0,MAXCYCLE+MAXCYCLE2))
#ax[2,2].set_xlim(0,t2*dt)

for i in range(7):
    ddens = x[t2,i] - x[0,i]
    print("ddens of i={} is {:.4f}".format(i,ddens))

lineObjects = ax[2,2].plot(np.arange(MAXCYCLE+0,MAXCYCLE+len(x0_list)),x0_list[:])
#ax[1,0].legend(iter(lineObjects), ('V', 'amino', 'x1', 'rib', 'enzyme', 'x4', 'x5', 'plipid'))
ax[2,2].set_title(r"(random $V_0$={}) {}-{}th generetion".format(V0,MAXCYCLE+1, MAXCYCLE+MAXCYCLE2))
ax[2,2].set_xlabel("Generation")
ax[2,2].set_ylabel(r"Initial state $x_0$")
ax[2,2].set_ylim(0,1.1)

plt.tight_layout()
plt.show()
#fig.savefig("riroen/cell2.png")