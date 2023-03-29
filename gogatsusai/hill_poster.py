import numpy as np
import matplotlib.pyplot as plt

#plt.rcParams['font.family'] = "MS Gothic"
plt.rcParams['font.family'] = "Meiryo"
plt.rcParams['font.size'] = 20

def Hill(x,n,K):
    return np.power(x,n)/(np.power(K,n) + np.power(x,n))

X = np.linspace(0,2)
K = 1
"""
N = [1.0, 5.0, 10.0]
for i in range(0,len(N)):
    n = N[i]
    plt.plot(X, Hill(X,n,K), label="n = " + str(n), color='black', linestyle=(0,(i+2,i)))
"""

fig = plt.figure()
n = 1
#plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='black', linestyle='solid')
plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='black', linestyle='solid')
n = 2
#plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='black', linestyle='dashed')
plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='green', linestyle='dashed')
n = 3
#plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='black', linestyle='dashdot')
plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='orange', linestyle='dashdot')
n = 10
#plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='black', linestyle='dotted')
plt.plot(X,Hill(X,n,K),label="n = "+str(n), color='red', linestyle='dotted')

plt.xlim(0,2)
plt.ylim(0,1)
plt.xlabel(r"リガンド濃度$\,[\mathrm{X}]/K_d$")
plt.ylabel(r"占有率$\,p$")

plt.legend(fontsize=18)
fig.tight_layout()
plt.show()