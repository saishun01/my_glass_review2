import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
import matplotlib.cm as cm 

N = 2 # 化学種の総数（ゴミや複合体は除く）
TMAX = 10**5
dt = 0.1

phi = 1
e = 1#10

#ep = 0.1
#em = 0.001
ep = 1
#em = 0.0001
em = 1#0.01
g = 1
# f = 0.2 # N=5のうちf*N=1個が栄養分子
M = 1 # 栄養分子の数 int(f*N)のかわり
D = 1

#delta = 1 #うごかす
#K = 1

#err = 0.2 #slopeにする

def slope(x, delta, K):
    return delta/(K+x)

def calc(n, delta, s):

    # 微分方程式
    def dxdt(x,t):
        # 念のため負にならないように調整
        for i in range(len(x)):
            if x[i] < 0:
                x[i] = 0

        # エラー率を膜成分(s=0) or 栄養成分(s=1)で変える
        err = slope(x[s], delta, K)

        ddt = np.zeros_like(x)
        ddt[0] -= phi*x[0] # 膜分子x[0]
        for i in range(len(x)):
            ddt[i] -= g*phi*x[0]*x[i] # 希釈
        ddt[1] += D*(n-x[1]) # 栄養成分（膜分子ではない）が出入りする
        
        # 普通の反応とエラー反応
        ddt[0] += e*(1-err)*x[0]*x[1]
        ddt[1] -= e*x[0]*x[1]
        #ddt[j] -= e*(1-err)*x[0]*x[1]
   
        ddt[2] += e*err*x[0]*x[1] # N～N+(N-1)番目の成分はゴミ分子
        
        # タンパク（膜分子、栄養分子も含む）とゴミが複合体をつくる反応
        G = ep*x[0]*x[2] - em*x[3]
        ddt[0] -= G
        ddt[2] -= G
        ddt[3] += G # i番目のタンパクとj番目のゴミが複合体を作る

        return ddt


    x0 = np.zeros(4) # 時間発展させたい濃度
    for i in range(N):
        x0[i] = 1.0
    t = np.arange(0,TMAX,dt)
    x = odeint(dxdt, x0, t)

    return t, x 

fig = plt.figure()
ax = fig.add_subplot(111)
cmap = plt.get_cmap("tab10")


s = 1

#list_K = [0.1, 0.5, 1]
list_K = [1, 10, 100]

for K in list_K:

    #list_delta = [0,0.2,0.4,0.6,0.8,1]
    list_delta = np.linspace(0,K,50)
    #list_delta=[1]

    list_n = []

    #dn = 0.1  # s=0
    dn = 0.01 # s=1

    n = dn
    for delta in list_delta:
        n -= dn
        mu = 0
        while mu < 10**(-3):
            n += dn
            t, x = calc(n, delta, s)
            mu = g*phi*x[-1,0]
        list_n.append(n)
            
    ax.scatter(list_delta/K, list_n, label=r'$\epsilon = \epsilon(y), K={}$'.format(K))


X = np.linspace(0,0.99,1000)
f = lambda X: np.power(1-X, -1)
ax.plot(X, f(X), label=r'$\epsilon = \delta/K$')

ax.set_xlabel(r'$\delta/K$')
ax.set_ylabel(r'Threshold of external nutrient concentration $n^*$')

#ax.set_xscale('log')
#ax.set_yscale('log')
ax.legend()

ax.set_xlim(0,1)
#ax.set_ylim(0, 20) # s=0
ax.set_ylim(0, 10) # s=1
plt.grid()
plt.tight_layout()
plt.show()