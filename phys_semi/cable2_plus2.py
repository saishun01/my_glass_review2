import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

V_mem = -90
s = 1
bq = 0.5
g_Na = 1/5
g_K = 5
V_Na = 54
V_K = -75
V_star = -40
V_mem = (g_Na*V_Na + g_K*V_K)/(g_K + g_Na)
V_0 = 50  #変更

fig = plt.figure()

nx = 400
lamb = 9.1
tau = 2
d = lamb**2/tau
x = np.linspace(-100,100,nx)
dx = x[2] - x[1]
etime = 1.5
dt = 0.0005

V = np.zeros(nx)
Vn = np.zeros(nx)
for i in range(0,nx):
    V[i] = (V_0-V_mem)*np.exp(-(x[i]/s)**2) + V_mem

plt.plot(x,V, label='0')

def f(V):
    gNa = 100/(1+np.exp(bq*(V_star-V))) + 1/5
    return gNa/g_K * (V - V_Na) + V - V_K

time = 0
V_dat = []
while(time<=etime):
    Vn[0] = V[0] - dt/tau*f(V[0]) + d*(V[1]-2*V[0]+V[nx-1]) *nx**2* dt/40000  
    Vn[nx-1] = V[nx-1] - dt/tau*f(V[nx-1]) + d*(V[0]-2*V[nx-1]+V[nx-2]) *nx**2* dt/40000   
    for i in range(1,nx-1):
        Vn[i] = V[i] - dt/tau*f(V[i]) + d*(V[i+1]-2*V[i]+V[i-1]) *nx**2* dt/40000   
    V = Vn
    time = time + dt
    if int(time*2000)%400 == 0:
        for i in range(nx):
            V_dat.append(V[i])

V_data = np.array(V_dat).reshape(7,400)
#print(V_data.shape)
#print(V_data)
#plt.plot(V_data.T)
#plt.xlim(200, 300)
df = pd.DataFrame(V_data)
df = df.rename({0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six'})
df = df.T
print(df.query('-10 < one < 10'))
