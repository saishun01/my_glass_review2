import numpy as np
import matplotlib.pyplot as plt

def Adair(x,K):
    n = len(K)
    num_occ = 0
    num_all = n
    for j in range(1,n+1):
        Kj = 1.
        for i in range(0, j):
            Kj *= K[i]
        num_occ += j*Kj*np.power(x,j)
        num_all += n*Kj*np.power(x,j)
    return num_occ/num_all


K = [1,1,100]

Y = np.linspace(-3,3)
X = np.power(10, Y)
P = Adair(X,K)

plt.plot(X, P/(1-P))
plt.xscale('log')
plt.yscale('log')
plt.show()

        