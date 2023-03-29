import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = "MS Gothic"

def mwc(X, n, K, L0, c):
    x = K*X
    y = c*x
    return (x*np.power(1+x, n-1) + L0*y*np.power(1+y,n-1))/(np.power(1+x,n)+L0*np.power(1+y,n))

def hill(x,n,K):
    return np.power(x,n)/(np.power(K,n) + np.power(x,n))

n = 4
K = 0.1
L0 = 1000
c = 0.01

fig = plt.figure(figsize=(7,3))#figsize=(6,2))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
#fig.subplots_adjust(hspace=0.6, wspace=0.4)

XMAX = 100
X = np.linspace(0, XMAX)
ax1.plot(X, mwc(X,n,K,L0,c), color='black')

ax1.set_xlim(0,XMAX)
ax1.set_ylim(0,1)

ax1.set_title('(1)',loc='left')
ax1.set_xlabel(r"リガンド濃度$\,[\mathrm{X}]$")
ax1.set_ylabel(r"占有率$\,p$")

#YMIN = 0
#YMAX = 3
YMIN = -3
YMAX  = 5
Y = np.linspace(YMIN,YMAX)
X = np.power(10, Y)
P = mwc(X,n,K,L0,c)

def mwc2(X,n,K,L0,c):
    a = K*X
    y = (1+c*a)/(1+a)
    k = (1+L0*c*np.power(y,n-1))/(1+L0*np.power(y,n-1))
    return k*a/(1+k*a)

def simple(X,K,k):
    a = K*X
    return k*a/(1+k*a)

P2 = mwc(X,n,K,L0,c)
#QR = simple(X,K,(1+L0*c)/(1+L0))
#QT = simple(X,K,(1+L0*np.power(c,n))/(1+L0*np.power(c,n-1)))
QR = simple(X,K,1)
QT = simple(X,K*c,1)
#ax2.plot(X, P/(1-P), color='black', linestyle='solid')
ax2.plot(X, P2/(1-P2), color='black', linestyle='solid')
ax2.plot(X,QR/(1-QR), color='black', linestyle='dashed')
ax2.plot(X,QT/(1-QT), color='black', linestyle='dotted')


#ax2.set_xlim(10**YMIN,10**YMAX)
#ax2.set_ylim(0.001,100)

ax2.set_title('(2)',loc='left')
ax2.set_xlabel(r"リガンド濃度$\,[\mathrm{X}]$")
ax2.set_ylabel(r"占有率の高さ$\,\frac{p}{1-p}$")

ax2.set_xscale('log')
ax2.set_yscale('log')

fig.tight_layout()
plt.show()