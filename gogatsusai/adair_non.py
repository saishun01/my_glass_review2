import numpy as np
import matplotlib.pyplot as plt

def Adair_non(x,n):
    return (n*np.power(x,n+1) + 1)/(np.power(x,n+1) - 1) - 1/(x-1)

X = np.linspace(0,2)
for n in range(1,5):
    plt.plot(X, Adair_non(X, n),label="n = "+str(n))
plt.legend()
plt.show()