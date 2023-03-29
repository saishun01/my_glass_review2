import numpy as np
import random 
import matplotlib.pyplot as plt

NUM = 4

a = 1
u = lambda x,k: a*np.cos(k*x)
s = 0
X = np.linspace(-20,20,10000)

fig = plt.figure(tight_layout=True)
axes = fig.subplots(2,2)

for i in range(NUM):
    N = 10**i
    for j in range(N):
        k = random.gauss(1,0.3)
        #k = 1
        s += u(X,k)
        #plt.plot(T, u(T,w), color='grey')
    
    x = i//2
    y = i%2 
    axes[x,y].plot(X,s)
    axes[x,y].set_title('N = {}'.format(N))
    axes[x,y].set_xlabel('Position')
    axes[x,y].set_ylabel('Electric field')

plt.show()