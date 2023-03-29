import numpy as np
import matplotlib.pyplot as plt

#plt.rcParams['font.family'] = "MS Gothic"
plt.rcParams['font.family'] = "Meiryo"

def simple(x,K):
    return x/(K + x)

K = 1
XMAX = 5
X = np.linspace(0,XMAX)

plt.figure()
plt.plot(X,simple(X,K),color='black')

plt.hlines([0.5],0,1,colors='black',linestyles='dashed')
plt.vlines([1],0,0.5,colors='black',linestyles='dashed')

plt.xlim(0,XMAX)
plt.ylim(0,1)

plt.xlabel(r"リガンド濃度$\,[\mathrm{X}]/K_d$")
plt.ylabel(r"占有率$\,p$")

plt.show()