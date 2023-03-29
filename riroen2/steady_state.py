import numpy as np
import matplotlib.pyplot as plt

e = 0.5
k = 1
k1 = 1
k2 = 1
g = 1
phi = 1
D = 1

n = 1

F = lambda x: 1 - e*(1 + np.power(k2/k1*np.power(x,-1) + 1 + g*phi/k1, -1))

G = lambda x: phi/k/n*(1+g*x)*(1+(k+g*phi)/D*x)

y = lambda x: n/(1 + (k + g*phi)/D*x)

#F = lambda x: -k*e*y(x)/(k1*k2/(k2+g*phi*x) - (k1+g*phi))

#G = lambda x: (phi*(1+g*x)-k*(1-e)*y(x))/(k1*k2/(k2+g*phi*x) - k1)

x = np.linspace(0.01, 1)
plt.plot(x, F(x))
plt.plot(x, G(x))
#plt.xlim(0,1)
#plt.ylim(0,)
plt.show()