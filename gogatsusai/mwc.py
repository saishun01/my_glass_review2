import numpy as np
import matplotlib.pyplot as plt

#plt.rcParams['font.family'] = "MS Gothic"
plt.rcParams['font.family'] = "Meiryo"

def mwc(X, n, K, L0, c):
    x = K*X
    y = c*x
    return (x*np.power(1+x, n-1) + L0*y*np.power(1+y,n-1))/(np.power(1+x,n)+L0*np.power(1+y,n))

def simple(X,K):
    x = K*X
    return x/(1+x)

n = 4
K = 0.1
L0 = 1000
c = 0.01

fig = plt.figure(figsize=(9,4))#figsize=(6,2))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
#fig.subplots_adjust(hspace=0.6, wspace=0.4)

XMAX = 100
X = np.linspace(0, XMAX)
ax1.plot(X, mwc(X,n,K,L0,c), color='black', linestyle='solid')
#ax1.plot(X, simple(X,K), color='black', linestyle='dashed')
#ax1.plot(X, simple(X,K*c), color='black', linestyle='dotted')

ax1.set_xlim(0,XMAX)
ax1.set_ylim(0,1)

ax1.set_title('(1)',loc='left')
ax1.set_xlabel(r"リガンド濃度$\,[\mathrm{X}]$")
ax1.set_ylabel(r"占有率$\,p$")

YMIN = 0
YMAX = 3

Y = np.linspace(YMIN,YMAX)
X = np.power(10, Y)
P = mwc(X,n,K,L0,c)


QR = simple(X,K)
QT = simple(X,K*c)
ax2.plot(X, P/(1-P), color='black', linestyle='solid', label=r'MWC')
ax2.plot(X,QR/(1-QR), color='black', linestyle='dashed', label=r'Hill,$\,(n,K_d)=(1,K_R^{-1})$')
ax2.plot(X,QT/(1-QT), color='black', linestyle='dotted', label=r'Hill,$\,(n,K_d)=(1,K_T^{-1})$')

ax2.set_xlim(10**YMIN,10**YMAX)
ax2.set_ylim(0.001,100)

ax2.set_title('(2)',loc='left')
ax2.set_xlabel(r"リガンド濃度$\,[\mathrm{X}]$")
ax2.set_ylabel(r"占有率の高さ$\,\frac{p}{1-p}$")

ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.legend(fontsize='small')

fig.tight_layout()
plt.show()