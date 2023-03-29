import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random


N = 2 # 化学種の総数（ゴミや複合体は除く）
TMAX = 10**5
dt = 0.1

eg = 1
e = 1

#ep = 0.1
#em = 0.001
ep = 1
em = 0.01
g = 1
p = 0.8
M = 1 # 栄養分子の数 
D = 1
# nを変えていく

err = 0

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

    # ランダム反応ネットを作る
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

def calc(Rlist, n, err):

    # 微分方程式
    def dxdt(x,t):
        # 念のため負にならないように調整
        for i in range(len(x)):
            if x[i] < 0:
                x[i] = 0
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

# 最後の傾き（定常かチェック）
def const_check(x):

    cost = 0
    for i in range(N):
        ddens = (x[-1,i] - x[-2,i])/dt
        #print("{:.4f}".format(ddens), end=' ')
        cost += ddens**2
    return cost



#list_err = [0, 0.01, 0.1, 0.5, 1]
#list_reac = [[[1,0,0]], [[1,0,1]], [[1,0,0],[0,1,0]], [[1,0,0],[0,1,1]], [[1,0,1],[0,1,0]],  [[1,0,1],[0,1,1]]]
list_reac = [[[1,0,0]]]#, [[1,0,0],[0,1,0]]]

#list_n = [10**(-5), 10**(-4), 10**(-3), 10**(-2), 10**(-1), 10**0, 10**1, 10**2, 10**3, 10**4, 10**5]
list_n = [10**(x/20) for x in range(20)]


fig = plt.figure()
ax = fig.add_subplot(111)
cmap = plt.get_cmap("tab10")


for j in range(len(list_reac)):
    list_x = [] # ここにnを入れる
    list_y = [] # ここに成長速度を入れる
    Rlistj = list_reac[j]
    for i in range(len(list_n)):
        ni = list_n[i]
        t, x = calc(Rlistj, ni, err)
        cost = const_check(x)

        #while cost > 10**(-8): # 発散したらやり直し
        #    t,x = calc(ni, errj)
        #    cost = const_check(x)
        #    print('diverge')
        
        # 成長率
        growth_rate = g*eg*x[-1,0]
        list_x.append(ni)
        list_y.append(growth_rate)

    ax.plot(list_x, list_y,color=cmap(j), label='reaction = {}'.format(list_reac[j]))
    print('calculating {}/{}'.format(j+1,len(list_reac)))


X = np.array([10**(x/100) for x in range(100)])
ax.plot(X, (np.sqrt(1+8*X) - 3)/4, color=cmap(j+1), label='steady state of [[1,0,0]]')
ax.set_xlabel(r'$n$')
ax.set_ylabel('Growth rate')
ax.set_xscale('log')
ax.set_yscale('log')

#ax.set_ylim(10**(-12),10**4)
ax.legend()
plt.show()