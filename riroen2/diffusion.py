import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

a = 1
b = 5
c = 10
TMAX = 10
dt = 0.01

def dXdt(X, t):
    x, y = X
    dxdt = a*x*(b*(y-1)-x)
    dydt = c-(x+1)*y
    return [dxdt, dydt]

X0 = [1,2]
t = np.arange(0,TMAX,dt)
X = odeint(dXdt, X0, t)

#plt.plot(t, X[:])
plt.plot(X[:,0], X[:,1])

X0 = [2,1]
t = np.arange(0,TMAX,dt)
X = odeint(dXdt, X0, t)

#plt.plot(t, X[:])
plt.plot(X[:,0], X[:,1])

X0 = [5,5]
t = np.arange(0,TMAX,dt)
X = odeint(dXdt, X0, t)

#plt.plot(t, X[:])
plt.plot(X[:,0], X[:,1])
plt.show()