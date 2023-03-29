import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

TMAX = 10**10 # T(A=0)=2*10^9 if Sext=10^(-2)
dt = 10**(-6)*TMAX

v = 0.1 # 0.1
K = 1 # 1
Kt = 10 # 10
kp = 1 # 1
km = 10**(-6) # 10**(-6)
dA = 10**(-5) # 10**(-5)
dB = 10**(-5) # 10**(-5)
dC = 10**(-12) # 10**(-12) 
Sext = 10**(-1.5) # 10**(-1.46)と10**(-1.45)の間に何かある？

# define functions
def FA(S):
    return v*S/(K+S)*S/(Kt+S) # himeoka error
    #return v*S # riroen error

def FB(S):
    return v*S/(K+S)*Kt/(Kt+S) # himeoka error
    #return v*S*Kt/(Kt+S) # riroen error

def G(A,B,C):
    return kp*A*B-km*C

# define differential equation
# x = [S, A, B, C]
def dxdt(x, t):
    # non-negative
    for i in range(len(x)):
        if x[i] < 0:
            x[i] = 0
    ddt = np.zeros_like(x)

    # dilution and decay
    mu = FA(x[0])*x[1]
    d = [0, dA, dB, dC]
    for i in range(len(x)):
        ddt[i] += - mu*x[i] - d[i]*x[i]
    
    # diffusion
    ddt[0] += x[1]*(Sext - x[0]) # A is transporter
    #ddt[0] += 1*(Sext - x[0]) # constant diffusion

    # chemical reaction
    ddt[0] += - FA(x[0])*x[1] - FB(x[0])*x[1]
    ddt[1] += FA(x[0])*x[1] - G(x[1],x[2],x[3])
    ddt[2] += FB(x[0])*x[1] - G(x[1],x[2],x[3])
    ddt[3] += G(x[1],x[2],x[3])

    return ddt

# initial state
x0 = np.zeros(4)
x0[0] = Sext
x0[1] = 1.
print('x0 = ', x0)

# calculation
t_list = np.arange(0,TMAX,dt)
x_list = odeint(dxdt, x0, t_list)

# plot
fig = plt.figure()
ax = fig.add_subplot(111)

# plot of chemicals
for i in range(len(x_list[0,:])):
    #if i != 3:
    #    continue
    ax.plot(t_list,x_list[:,i], label='{}'.format(i))

# plot of growth rate
mu_list = []
for i in range(len(x_list)):
    mu_list.append(FA(x_list[i,0])*x_list[i,1])
ax.plot(t_list,mu_list, label='mu')
"""
# plot of functions
FA_list = []
FB_list = []
G_list = []
for i in range(len(x_list)):
    FA_list.append(FA(x_list[i,0]))
    FB_list.append(FB(x_list[i,0]))
    G_list.append(G(x_list[i,1],x_list[i,2],x_list[i,3]))
ax.plot(t_list, FA_list, label='FA')
ax.plot(t_list, FB_list, label='FB')
ax.plot(t_list, G_list, label='G')
"""
"""
# plot of differentiation of A. Don't confuse with d_A.
DA_list = []
for i in range(len(x_list)):
    DA = FA(x_list[i,0])*x_list[i,1] - G(x_list[i,1],x_list[i,2],x_list[i,3]) -mu_list[i]*x_list[i,1] -dA*x_list[i,1]
    DA_list.append(DA)
ax.plot(t_list, DA_list, label='DA')


# check A+C=1
AC_list=[]
for i in range(len(x_list)):
    if i==0:
        AC_list.append(0)
        continue
    AC_list.append(x_list[i,1]+x_list[i,3])
ax.plot(t_list,AC_list,label='A+C')
print(min(AC_list), AC_list.index(min(AC_list)), max(AC_list), AC_list.index(max(AC_list)))

#ax.set_ylim(min(AC_list),max(AC_list))
"""
"""
# dead or steady 判定．無理そうなので，TMAXまで計算してからA<10**(-20)になったことがあるかで判定する？
for i in range(len(x_list)):

    if i <= 10**3:
        continue
    else:

        diff = 0
        for j in range(len(x_list[0])):
            diff += (x_list[i,1] - x_list[i-1,1])**2

        if x_list[i,1] < 10**(-20):
            print('dead at t = {}'.format(i*dt))
            break
        elif diff < 10**(-20):
            print('steady at t = {}'.format(i*dt))
            break
        else:
            if i==len(x_list)-1:
                print('No idea')
            else:
                continue
"""
ax.legend()

ax.set_xscale('log')
ax.set_yscale('log')

plt.show()

"""
# compound check
t = 0
print(x_list[t,0],x_list[t,1],x_list[t,2],x_list[t,3])
print(v*x_list[t,0]/(K+x_list[t,0]),FA(x_list[t,0]),FB(x_list[t,0]),G(x_list[t,1],x_list[t,2],x_list[t,3]))

"""
# とりあえず複合体が形成されないバグは解消．しかし代謝物Aがどうも消費されず，death phaseが見られない．

# なぜかA+Cが1でなく初期値に依存した値になる．
# 理由は準定常だからだった．TMAX=10^8まで計算すればうまくいく，というかA=0になってA+C=1が成り立たなくなる．