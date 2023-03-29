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

delta = 1

#err = 0.2 #slopeにする

#def slope(x, err):
#    return err

def calc(n, err, s):

    # 微分方程式
    def dxdt(x,t):
        # 念のため負にならないように調整
        for i in range(len(x)):
            if x[i] < 0:
                x[i] = 0

        # エラー率を膜成分(s=0) or 栄養成分(s=1)で変える
        #err = slope(x[s], err)

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


#list_reac = [[[1,0,0]]]

NMAX = 6
n_split = 50
#list_n = [0+10*delta*x/n_split for x in range(n_split//2)]
list_n = [0+x/n_split for x in range(NMAX*n_split)]

s = 0

#list_err = [1]
list_err = [0,0.2,0.4,0.6,0.8]

for j in range(len(list_err)):
    list_x = [] # ここにnを入れる
    list_y = [] # ここに成長速度を入れる
    for i in range(len(list_n)):
        ni = list_n[i]
        t, x = calc(ni, list_err[j], s)
        
        # 成長率
        growth_rate = g*phi*x[-1,0]
        list_x.append(ni)
        #list_y.append(growth_rate)
        list_y.append(x[-1,0])
    
    ax.plot(list_x, list_y,color=cmap(j), label=r'$\epsilon={}$'.format(list_err[j]))
    print('calculating {}/{}'.format(j+1,len(list_err)))


ax.set_xlabel(r'External nutrient concentration $n$')
ax.set_ylabel(r'Growth rate $\mu$')
#ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()

ax.set_xlim(0,NMAX)
ax.set_ylim(10**(-9), 10)
plt.grid()
plt.tight_layout()
plt.show()