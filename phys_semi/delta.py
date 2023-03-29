import numpy as np
import matplotlib.pyplot as plt

lamb = 9.1
tau = 2
v = lamb/tau
D = lamb**2/tau

t_int = np.linspace(3,6)
t = 10**(-t_int)
plt.plot(t, v*t, label='$\Delta x = v\Delta t$')
plt.plot(t, np.sqrt(2*D*t), label='$\Delta x = \sqrt{2D\Delta t}$')
plt.fill_between(t,np.sqrt(2*D*t),1,facecolor='y',alpha=0.5)

T = [10**(-4),2*10**(-5),5*10**(-5)]
X = [0.5,0.1,0.2]
plt.scatter(T,X,color='red')

plt.xlim(10**(-6),10**(-3))
plt.ylim(10**(-3),1)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('$\Delta t$')
plt.ylabel('$\Delta x$')
plt.grid(which='major',alpha=1.0)
plt.grid(which='minor',alpha=0.5)
plt.legend()
plt.show()