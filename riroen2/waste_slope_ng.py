import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
import itertools
import matplotlib.cm as cm 
#import sys
#sys.setrecursionlimit(10**7) # 再起回数の設定

N = 2 # 化学種の総数（ゴミや複合体は除く）
TMAX = 10**5
dt = 0.1

eg = 1
e = 1

#ep = 0.1
#em = 0.001
ep = 1
#em = 0.0001
em = 0.01
g = 1
p = 0.8
# f = 0.2 # N=5のうちf*N=1個が栄養分子
M = 1 # 栄養分子の数 int(f*N)のかわり
D = 1

delta = 0.7
#s = 1
#n = 1 #+ delta  # n=10でないと生きられないネットも

#err = 1 #slopeにする


#Rlist = [[0, 1, 0], [1, 0, 0]] # err=0でべき減衰
#Rlist = [[1, 0, 0]]

#Rlist = [[1, 0, 1]] # err=0で生存


def slope(x, delta):
    return delta/(1+x)

def next(Rlist):
    result = []
    for v in range(N):
        list = []
        for j in range(len(Rlist)):
            if Rlist[j][0] == v:
                list.append(Rlist[j][1])
        result.append(list)
    return result

def dfs(G, v, seen):
    seen[v] = 1
    #print(v, end='')
    for next_v in range(len(G[v])):
        if seen[G[v][next_v]]:
            continue
        dfs(G, G[v][next_v], seen)

def random_net():

    # ランダム反応作る
    Rlist = []
    chem = np.arange(N)
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            else:
                if np.random.rand() < p:
                    Rlist.append([i,j,random.choice(chem)])


    print(Rlist)

    # 連結か判定
    G = next(Rlist)
    #print(G)
    seen = np.zeros(N)
    for i in range(M):
        seen[i+1] = 1

    con_list = []
    for i in range(M):
        dfs(G,1+i,seen)
        #print(seen)
        con = False
        if seen[0]==1:
            con = True
        con_list.append(con)

    is_con = False
    for i in range(len(con_list)):
        if con_list[i] == True:
            is_con = True
            break

    print(is_con)
    return Rlist, is_con

def calc(Rlist, n, delta, s):

    # connectedな反応が来るまで作り直す
    #Rlist, is_con = random_net()
    #while is_con==False:
    #    Rlist, is_con = random_net()
    
    

    # 微分方程式
    def dxdt(x,t):
        # 念のため負にならないように調整
        for i in range(len(x)):
            if x[i] < 0:
                x[i] = 0

        # エラー率を膜成分(s=0) or 栄養成分(s=1)で変える
        err = slope(x[s], delta)

        ddt = np.zeros_like(x)
        ddt[0] -= eg*x[0] # 膜分子x[0]
        for i in range(len(x)):
            ddt[i] -= g*eg*x[0]*x[i] # 希釈
        for i in range(M):
            ddt[1+i] += D*(n-x[1+i]) # 栄養成分（膜分子ではない）が出入りする
        
        # 普通の反応とエラー反応
        for r in range(len(Rlist)):
            j,i,k = Rlist[r]
            ddt[i] += e*(1-err)*x[j]*x[k]
            ddt[j] -= e*(1-err)*x[j]*x[k]
   
            ddt[N+i] += e*err*x[j]*x[k] # N～N+(N-1)番目の成分はゴミ分子
        
        # タンパク（膜分子、栄養分子も含む）とゴミが複合体をつくる反応
        for i in range(N):
            for j in range(N):
                G = ep*x[i]*x[N+j] - em*x[2*N+N*i+j]
                ddt[i] -= G
                ddt[N+j] -= G
                ddt[2*N+N*i+j] += G # i番目のタンパクとj番目のゴミが複合体を作る

        return ddt


    x0 = np.zeros(2*N+N**2) # 時間発展させたい濃度
    for i in range(N):
        x0[i] = 1.0
    t = np.arange(0,TMAX,dt)
    x = odeint(dxdt, x0, t)

    return t, x 

# 最後の傾き（定常かcheck）
def const_check(x):

    cost = 0
    for i in range(len(x[0,0:N])):
        ddens = (x[-1,i] - x[-2,i])/dt
        #print("{:.4f}".format(ddens), end=' ')
        cost += ddens**2
    return cost


#fig, ax = plt.subplots(1, 2, figsize=(10,4))
#cmap = plt.get_cmap("tab10")
#fig.suptitle('Reaction = {}'.format(Rlist))

fig = plt.figure()
ax = fig.add_subplot(111)
cmap = plt.get_cmap("tab10")


#list_reac = [[[1,0,1]], [[1,0,1],[0,1,0]],  [[1,0,1],[0,1,1]], [[1,0,0]],  [[1,0,0],[0,1,0]], [[1,0,0],[0,1,1]]]
list_reac = [[[1,0,0]],  [[1,0,0],[0,1,0]]]#, [[1,0,0],[0,1,1]]]

#n_split = 20
#list_n = [10**(x/n_split) for x in range(-n_split,n_split+1)]
n_split = 100
list_n = [1+10*delta*x/n_split for x in range(n_split//2)]
#list_n = [1+0.01*x/n_split for x in range(n_split//2)] # delta=0用
#list_n = [1+30*x/n_split for x in range(n_split//2)] # delta=1用

for s in range(2):

    for j in range(len(list_reac)):
        index = len(list_reac)*s + j
        list_x = [] # ここにnを入れる
        list_y = [] # ここに成長速度を入れる
        Rlistj = list_reac[j]
        for i in range(len(list_n)):
            ni = list_n[i]
            t, x = calc(Rlistj, ni, delta, s)
            
            # 成長率
            growth_rate = g*eg*x[-1,0]
            list_x.append(ni)
            list_y.append(growth_rate)

        #ax.plot(list_x, list_y,color=cmap(index), lw=(2*len(list_reac)-index) ,label=r'$x=x_{}$, reaction={}'.format(s,list_reac[j])) # delta=0用
        
        ax.plot(list_x, list_y,color=cmap(index), label=r'$x=x_{}$, reaction={}'.format(s,list_reac[j]))
        print('calculating {}/{}'.format(index+1,2*len(list_reac)))


ax.set_xlabel(r'$n$')
ax.set_ylabel('Growth rate')
#ax.set_xscale('log')
ax.set_yscale('log')
ax.legend()

plt.grid()
plt.tight_layout()
plt.show()