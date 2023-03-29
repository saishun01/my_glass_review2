import numpy as np
import matplotlib.pyplot as plt

#plt.rcParams['font.family'] = "MS Gothic"
plt.rcParams['font.family'] = "Meiryo"

def Hill(x,n,K):
    return np.power(x,n)/(np.power(K,n) + np.power(x,n))


Y = np.linspace(-3,3)
X = np.power(10, Y)

n, K = 1, 1
P = Hill(X,n,K)
plt.plot(X, P/(1-P),label=r"$(n, K_d) = ($"+str(n)+r"$,$"+str(K)+"$)$", color='black', linestyle='solid')
n, K = 5, 1
P = Hill(X,n,K)
plt.plot(X, P/(1-P),label=r"$(n, K_d) = ($"+str(n)+r"$,$"+str(K)+"$)$", color='black', linestyle='dashed')
n, K = 1, 10
P = Hill(X,n,K)
plt.plot(X, P/(1-P),label=r"$(n, K_d) = ($"+str(n)+r"$,$"+str(K)+"$)$", color='black', linestyle='dotted')

plt.xlim(0.1,100)
plt.ylim(0.1,10)

plt.xlabel(r"リガンド濃度$\,[\mathrm{X}]$")
plt.ylabel(r"占有率の高さ$\,\frac{p}{1-p}$")

plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.legend()
plt.show()