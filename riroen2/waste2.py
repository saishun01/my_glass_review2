import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

import sys
#sys.setrecursionlimit(10**7) # 再起回数の設定

N = 5 # 化学種の総数（ゴミや複合体は除く）
TMAX = 10#1000
dt = 0.1

eg = 1
e = 1
err = 0#0.001
ep = 0.1
em = 0.001
g = 1
p = 0.1
# f = 0.2 # N=5のうちf*N=1個が栄養分子
M = 1 # 栄養分子の数 int(f*N)のかわり
D = 1
n = 1


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

def calc():

    # connectedな反応が来るまで作り直す
    #Rlist, is_con = random_net()
    #while is_con==False:
    #    Rlist, is_con = random_net()

    Rlist=[[1,0,0],[1,2,2],[0,3,4],[3,4,0],[2,0,4]]

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
        '''
        # タンパク（膜分子、栄養分子も含む）とゴミが複合体をつくる反応
        for i in range(N):
            for j in range(N):
                G = ep*x[i]*x[N+j] - em*x[2*N+N*i+j]
                ddt[i] -= G
                ddt[N+j] -= G
                ddt[2*N+N*i+j] += G # i番目のタンパクとj番目のゴミが複合体を作る
        '''
        return ddt


    x0 = np.ones(2*N+N**2) # 時間発展させたい濃度
    x0[0] = 1
    x0[1] = 1
    x0[2] = 1
    x0[3] = 1
    x0[4] = 1
    for i in range(len(x0)):
        if i > 4:
            x0[i] = 0
    t = np.arange(0,TMAX,dt)
    x = odeint(dxdt, x0, t)

    return t, x 

t, x = calc()

# 最後の傾き（定常かcheck）
def const_check(x):

    cost = 0
    for i in range(len(x[0,:])):
        ddens = (x[-1,i] - x[-2,i])/dt
        print("{:.4f}".format(ddens), end=' ')
        if (1+i) % 10 == 0 or i == len(x[0,:])-1:
            print('')
        cost += ddens**2
    return cost


cost = const_check(x)
'''
while cost > 10**(-8): # 発散したらやり直し
    t,x = calc()
    cost = const_check(x)
'''
print(x[-1,:])
# 成長率
growth_rate = g*eg*x[-1,0]
print('growth rate : ', growth_rate)

plt.plot(t,x)
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()