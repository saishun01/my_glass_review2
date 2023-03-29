import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

import sys
sys.setrecursionlimit(10**7) # 再起回数の設定

N = 120 # 化学種の総数（ゴミや複合体も含む）
TMAX = 200
dt = 0.1

eg = 1
de = 0.001
e = 1 - de
ep = 0.1
em = 0.001
g = 1
p = 0.1
f = 0.1 # N=10のうちf*N個が栄養分子
D = 1
n = 1

def random_net(): # このNは「普通の反応」に寄与する分子数なので，N=10とはちがう

    # ランダム反応作る
    Rlist = []
    chem = np.arange(N-2)
    for i in range(N-2):
        for j in range(N-2):
            if i == j:
                continue
            else:
                if np.random.rand() < p:
                    Rlist.append([i,j,random.choice(chem)])


    #print(Rlist)

    # 連結か判定
    def next(Rlist):
        result = []
        for v in range(N-2):
            list = []
            for j in range(len(Rlist)):
                if Rlist[j][0] == v:
                    list.append(Rlist[j][1])
            result.append(list)
        return result

    G = next(Rlist)
    print(G)
    seen = np.zeros(N-2)
    for i in range(int(f*N)):
        seen[i+1] = 1


    def dfs(G, v):
        seen[v] = 1
        #print(v, end='')
        for next_v in range(len(G[v])):
            if seen[G[v][next_v]]:
                continue
            dfs(G, G[v][next_v])      

    con_list = []
    for i in range(int(f*N)):
        dfs(G,1+i)
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

# connectedな反応が来るまで作り直す
Rlist, is_con = random_net()
while is_con==False:
    Rlist, is_con = random_net()

# 微分方程式
def dxdt(x,t):
    for i in range(len(x)):
        if x[i] < 0:
            x[i] = 0
    ddt = np.zeros_like(x)
    ddt[0] -= eg*x[0] # 膜分子x[0]
    for i in range(len(x)):
        ddt[i] -= g*eg*x[0]*x[i] # 希釈
    for i in range(int(len(x)*f)):
        ddt[1+i] += D*(n-x[1+i]) # 全成分のうちfの割合が出入りする（膜分子は除く）
    
    # 普通の反応とエラー反応
    for r in range(len(Rlist)):
        i,j,k = Rlist[r]
        ddt[j] += (e-de)*x[i]*x[k]
        ddt[i] -= (e-de)*x[i]*x[k]
        ddt[-2] += de*x[i]*x[k] # 最後から2番目の成分はゴミ分子
    
    # タンパクとゴミが複合体をつくる反応
    for i in range(int(len(x)*f),len(x)-2):
        G = ep*x[-2]*x[i] - em*x[-1]
        ddt[i] -= G
        ddt[-2] -= G
        ddt[-1] += G

    return ddt


x0 = np.ones(N) # 時間発展させたい濃度
t = np.arange(0,TMAX,dt)
x = odeint(dxdt, x0, t)

'''
# 生死判定（いらない？）
print(x[-1,0])
if float(x[-1,0]) > 10**(-6):
    print('survive')
else:
    print('dead')
'''

# 成長率
growth_rate = g*eg*x[-1,0]
print(growth_rate)

# print(x[-1,:]) # ゴミが溜まってたりする

plt.plot(t,x)
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.show()