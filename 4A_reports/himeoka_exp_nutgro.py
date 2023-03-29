import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
random.seed(12345) # 123/12345
np.random.seed(12345) # 123/12345

N = 4 # 10 # number of spiecies
M = 2 # 2 # number of spiecies for growth
NANS = 4 # 8 # number of ansamble

NPLT = 10**5

TMAX = 10**9 # 10**10
div = 10**6 # 10**6でもODE errorになることがある(N=5).
dt = TMAX//div # 10**(-5)*TMAX # 10**(-4)*TMAX -> ansamble error


p = 0.3 # 0.3 # prob of connection

v = 0.1 # 0.1
K = 1 # 1
Kt = 10 # 10
kp = 1 # 1
km = 10**(-6) # 10**(-6)
dA = 10**(-5) # 10**(-5)
dB = 10**(-5) # 10**(-5)
dC = 10**(-12) # 10**(-12) 
#Sext = 10**(-2) # 10**(1)

# create random net
def next(Rlist): 
    result = []
    for v in range(N):
        list = []
        for j in range(len(Rlist)):
            if Rlist[j][1] == v: # if a(jth) reaction prod vth protein
                list.append(Rlist[j][0]) # list name of subs of the(jth) reac
        result.append(list)
    return result

def dfs(G, v, seen): # connected判定用．再帰.
    seen[v] = 1
    #print(v, end='')
    for next_v in range(len(G[v])):
        if seen[G[v][next_v]]:
            continue
        dfs(G, G[v][next_v], seen)

def random_net():
    Rlist = []
    chem = np.arange(N) 
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            else:
                if np.random.rand() < p:
                    k = random.choice(chem)
                    while(k == 0):
                        k = random.choice(chem)
                    Rlist.append([i,j,k]) # Rlist = set of [ini,fin,cat]
    print(Rlist)

    # 連結か（growthに関わる分子がnutに繋がるか）判定
    G = next(Rlist)
    # print(G)
    # seen[1~M] = 1 (connect with growth)
    seen = np.zeros(N)
    for i in range(M):
        seen[i+1] = 1

    con_list = []
    for i in range(M):
        dfs(G,1+i,seen)
        #print(seen)
        con = False
        if seen[0]==1:
            con = True # nut is connected with growth 
        con_list.append(con)

    is_con = False
    for i in range(len(con_list)):
        if con_list[i] == True:
            is_con = True
            break

    print(is_con)
    return Rlist, is_con



# define functions
def FA(S):
    return v*S/(K+S)*S/(Kt+S)

def FB(S):
    return v*S/(K+S)*Kt/(Kt+S)

def G(A,B,C):
    return kp*A*B-km*C

# def diff eq and calc it
def calc(Rlist,Sext):

    #Rlist, is_con = random_net()
    #while is_con==False:
    #    Rlist, is_con = random_net()

    # define differential equation
    # x = [S, Ai, Bi, Ci]
    def dxdt(x, t):
        # non-negative
        for i in range(len(x)):
            if x[i] < 0:
                x[i] = 0
        ddt = np.zeros_like(x)
        
        # diffusion
        ddt[0] += x[1]*(Sext - x[0]) # i = 1 is transporter
        #ddt[0] += 1*(Sext - x[0]) # constant diffusion

        # chemical reactions (random)
        mu = 0
        for r in range(len(Rlist)):
            i, j, k = Rlist[r]
            ddt[i] -= FA(x[i])*x[k]
            ddt[j] += FA(x[i])*x[k]
            ddt[N+j] += FB(x[i])*x[k]
            if 1<= j and j <= M:
                mu += FA(x[i])*x[k] # growth rate
        """
        # ith spe and jth gab create comp
        for i in range(N):
            for j in range(N):
                if i != j:
                    continue # compound exists only i=j
                ddt[i] -= G(x[i],x[N+j],x[2*N+N*i+j])
                ddt[N+j] -= G(x[i],x[N+j],x[2*N+N*i+j])
                ddt[2*N+N*i+j] += G(x[i],x[N+j],x[2*N+N*i+j]) 
        """
        # ith spe and jth gab create comp
        for i in range(N):
            ddt[i] -= G(x[i],x[N+i],x[2*N+i])
            ddt[N+i] -= G(x[i],x[N+i],x[2*N+i])
            ddt[2*N+i] += G(x[i],x[N+i],x[2*N+i]) 

        # dilution and decay
        d = []
        for i in range(len(x)):
            if i == 0:
                d.append(0) # decay of nutrient
            elif 1 <= i and i <= N:
                d.append(dA) # decay of spiecies
            elif N+1 <= i and i <= 2*N:
                d.append(dB) # decay of gabage
            else:
                d.append(dC) # decay of compound
        for i in range(len(x)):
            ddt[i] += - mu*x[i] - d[i]*x[i]


        return ddt

    # initial state
    #x0 = np.zeros(2*N+N**2) 
    x0 = np.zeros(3*N)
    for i in range(N):
        if i == 0:
            x0[0] = Sext # nutrient
        else:
            x0[i] = 1. # spiecies
    #print('x0 = ', x0)

    # calculation
    t_list = np.arange(0,TMAX,dt)
    x_list = odeint(dxdt, x0, t_list)

    return t_list, x_list



#list_reac = [[[1,0,0]]]


# plot
fig, axes = plt.subplots(1, 1, tight_layout=True, squeeze=False,figsize=(6,4))
#fig, axes = plt.subplots(1, NANS, tight_layout=True, squeeze=False,figsize=(5*NANS,4)) # for debag
cmap = plt.get_cmap("tab10")


Sext_indices = np.arange(-4,3,0.2)
#Sext_indices = np.arange(-4,3,0.1)

#Rlists = [[[0,1,1]],[[0,1,1],[1,0,1]]] # for N=2
for ans in range(NANS):

    # create random net
    Rlist, is_con = random_net()
    while is_con==False:
        Rlist, is_con = random_net()
    #Rlist = Rlists[ans]
    print('Rlist={}'.format(Rlist))

    
    # set Sext
    Sext_list = [] # [Sext,Sext,...]
    mu_list = []
    for Si in range(len(Sext_indices)):
        Sext = 10**Sext_indices[Si]
        Sext_list.append(Sext)
        
        
        t_list, x_list = calc(Rlist,Sext)
        #print(x_list[-1,0:2])
        mu = 0
        for r in range(len(Rlist)):
            i, j, k = Rlist[r]
            if 1<= j and j <= M:
                mu += FA(x_list[-1,i])*x_list[-1,k] # growth rate
        mu_list.append(mu)
        print('\t {}th/{} Sext is done.'.format(Si,len(Sext_indices)))
    
    axes[0,0].scatter(Sext_list, mu_list, color=cmap(ans), label='{}'.format(Rlist),s=50*1.5**(-ans))
    #axes[0,0].scatter(Sext_list, mu_list, color=cmap(ans), label='{}'.format(Rlist),s=(-ans+2)*20)
    #axes[0,ans].scatter(Sext_list, mu_list, color=cmap(ans), label='{}'.format(Rlist)) # for debag

    print('ansamble {}/{} is done.'.format(ans+1,NANS))

axes[0,0].legend()
axes[0,0].set_xscale('log')
axes[0,0].set_yscale('log')
axes[0,0].set_xlabel('Sext')
axes[0,0].set_ylabel('mu')

"""
# for debag
for ans in range(NANS):

    axes[0,ans].legend()
    axes[0,ans].set_xscale('log')
    axes[0,ans].set_yscale('log')

"""
plt.show()