import numpy as np
import matplotlib.pyplot as plt

s = 1
bq = 0.5
g_Na = 1/5
g_K = 5
V_Na = 54
V_K = -75
V_star = -40
V_mem = (g_Na*V_Na + g_K*V_K)/(g_K + g_Na)
V_0 = 0

fig = plt.figure()

nx = 1000
lamb = 9.1
tau = 2
d = lamb**2/tau
x = np.linspace(-50,50,nx)
dx = x[2] - x[1]
etime = 0.2002
dt = 0.0001

V = np.zeros(nx)
Vn = np.zeros(nx)
for i in range(0,nx):
    V[i] = (V_0-V_mem)*np.exp(-(x[i]/s)**2) + V_mem

def f(V):
    gNa = 100/(1+np.exp(bq*(V_star-V))) + 1/5
    return gNa/g_K * (V - V_Na) + V - V_K

time = 0

plt.plot(x,V, label='t = ' + '{:.3f}'.format(time) + ' ms')

while(time<=etime):
    Vn[0] = V[0] - dt/tau*f(V[0]) + d*(V[1]-2*V[0]+V[nx-1]) *nx**2* dt/10000  
    Vn[nx-1] = V[nx-1] - dt/tau*f(V[nx-1]) + d*(V[0]-2*V[nx-1]+V[nx-2]) *nx**2* dt/10000   
    for i in range(1,nx-1):
        Vn[i] = V[i] - dt/tau*f(V[i]) + d*(V[i+1]-2*V[i]+V[i-1]) *nx**2* dt/10000   
    V = Vn
    time = time + dt
    if 0.00799 <= time < 0.00801:
        plt.plot(x,V,label='t = ' + '{:.3f}'.format(time) + ' ms')
    elif 0.01999 <= time < 0.02001:
        plt.plot(x,V,label='t = ' + '{:.3f}'.format(time) + ' ms')
    elif 0.09999 <= time < 0.10001:
        plt.plot(x,V, label='t = ' + '{:.3f}'.format(time) + ' ms')
    elif 0.19999 <= time < 0.20001:
        plt.plot(x,V, label='t = ' + '{:.3f}'.format(time) + ' ms')

print(dx, V_mem)
plt.xlim(0,5)
plt.ylim(-75,V_0+40)
plt.xlabel('Position (mm)')
plt.ylabel('Voltage (mV)')
plt.legend()
plt.grid()
plt.show()
