import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

g = 1
b = 5
k = [1, 1, 1, 1, 1]
k_ = [0.5, 0.5, 0.1, 0.5, 0.5]
n = 1

TMAX = 5
dt = 0.01
MAXCYCLE = 20

np.random.seed(100)
prob = 0.05

def dxdt(x, t):
    ddt = np.zeros_like(x)
    ddt[0] = g*k[0]*x[4] 
    ddt[1] = -k[1]*n*x[1] + (k_[1] + 2*k[2])*x[2] - k_[2]*x[1]**2
    ddt[2] = k[1]*n*x[1] - (k_[1] + k[2])*x[2] + k_[2]*x[1]**2
    ddt[3] = k[3]*n*x[1] - (k_[3] + k[4])*x[3] - k_[4]*x[1]*x[4]
    ddt[4] = k[4]*x[3] - k_[4]*x[1]*x[4] - k[0]*x[4] 
    for i in range(len(x)-1):
        ddt[1+i] -= ddt[0]*x[1+i]#/x[0]

    return ddt

def dxdt_random(x, t):
    ddt = np.zeros_like(x)
    ddt[0] = g*k[0]*x[4] 
    ddt[1] = -k[1]*n*x[1] + (k_[1] + 2*k[2])*x[2] - k_[2]*x[1]**2 -b
    ddt[2] = k[1]*n*x[1] - (k_[1] + k[2])*x[2] + k_[2]*x[1]**2
    ddt[3] = k[3]*n*x[1] - (k_[3] + k[4])*x[3] - k_[4]*x[1]*x[4]
    ddt[4] = k[4]*x[3] - k_[4]*x[1]*x[4] - k[0]*x[4] 
    for i in range(len(x)-1):
        ddt[1+i] -= ddt[0]*x[1+i]#/x[0]
    
    if np.random.random() < prob:
        ddt[1] += b/prob
    
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

x0 = np.array([1, 1, 0, 0, 0])
t = np.arange(0, TMAX, dt)
x = odeint(dxdt, x0, t)
t2 = div_time(x,t)

lineObjects = ax[0,0].plot(t, x[:,0:5])
ax[0,0].legend(iter(lineObjects), ('V', 'x1(E)', 'x2(NE)',"x3(N'E)", 'x4(M)'))
ax[0,0].set_title("1st generation")
ax[0,0].set_xlim(0,t2*dt)
ax[0,0].set_xlabel("Time")


NMAX = MAXCYCLE - 1
for i in range(NMAX):
    x0 = div_state(x,t2)
    t = np.arange(0, TMAX, dt)
    x = odeint(dxdt, x0, t)   
    t2 = div_time(x,t)
    print("{:.2f}".format(t2*dt))

lineObjects = ax[0,1].plot(t, x[:,0:5])
#ax[0,1].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4'))
ax[0,1].set_title("{}th generation".format(MAXCYCLE))
ax[0,1].set_xlim(0,t2*dt)
ax[0,1].set_xlabel("Time")

for i in range(len(x[0,:])):
    ddens = x[t2,i] - x[0,i]
    print("ddens of i={} is {:.4f}".format(i,ddens))

# ここからランダム
def calc(x0,TMAX,dt):
    x = []
    x_tmp = x0
    t_count = 0
    T = []
    for i in range(len(t)):
        #print(dxdt(x_tmp,t))
        x_next = x_tmp + dt*dxdt_random(x_tmp,t)
        #print(x_next)
        if x_next[1] < 0:
            x_next[1] = 0
        x.append(x_next)
        x_tmp = x_next
    x = np.array(x)
    return x

x = calc(x0,TMAX,dt)

t2 = div_time(x,t)

lineObjects = ax[1,0].plot(t, x[:,0:5])
#ax[1,0].legend(iter(lineObjects), ('V', 'x1(E)', 'x2(NE)',"x3(N'E)", 'x4(M)'))
ax[1,0].set_title("(random) {}th generation".format(MAXCYCLE+1))
ax[1,0].set_xlim(0,t2*dt)
ax[1,0].set_xlabel("Time")


NMAX = MAXCYCLE - 1
for i in range(NMAX):
    x0 = div_state(x,t2)
    t = np.arange(0, TMAX, dt)
    #x = odeint(dxdt, x0, T) 
    x = calc(x0,TMAX,dt)   
    t2 = div_time(x,t)
    print('{:.2f}'.format(t2*dt))

lineObjects = ax[1,1].plot(t, x[:,0:5])
#ax[0,1].legend(iter(lineObjects), ('V', 'x1', 'x2', 'x3', 'x4'))
ax[1,1].set_title("(random) {}th generation".format(MAXCYCLE+MAXCYCLE))
ax[1,1].set_xlim(0,t2*dt)
ax[1,1].set_xlabel("Time")

for i in range(len(x[0,:])):
    ddens = x[t2,i] - x[0,i]
    print("ddens of i={} is {:.4f}".format(i,ddens))

plt.tight_layout()
plt.show()