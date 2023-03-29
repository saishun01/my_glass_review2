import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.integrate._ivp.rk import RK45

#2個の細胞が資源を取り合う

v = 10
d = 1
c = 1

J1S = lambda S: S/(1+S)
J2S = lambda S: 20*S/(1+S)
J1ATP = lambda S: 10*J1S(S)
J2ATP = lambda S: J2S(S)

t_span = [0.0, 20.0]
init = [0.109,100.0,0.1]
t_eval = np.linspace(*t_span, 1000)

def atp_path_nonsp(t,N):
    #S = N[0]と考える
    dSdt = v - N[1]*J1S(N[0]) - N[2]*J2S(N[0])
    dN1dt = c*J1ATP(N[0])*N[1] - d*N[1]
    dN2dt = c*J2ATP(N[0])*N[2] - d*N[2]
    return [dSdt, dN1dt, dN2dt]

sol = solve_ivp(atp_path_nonsp, t_span, init, method='RK45', t_eval=t_eval)

#print(sol.y)
fig = plt.figure()
ax1 = fig.subplots()
ax2 = ax1.twinx()

S, N1, N2 = sol.y
ax2.plot(sol.t, S, c='black', label=r'Resource $S$')
ax1.plot(sol.t, N1, label=r'Respirators $N_1$')
ax1.plot(sol.t, N2, label=r'Fermenters $N_2$')

ax1.set_xlabel(r'Time')
ax1.set_ylabel(r'Population size')
ax2.set_ylabel(r'Resource concentration')

ax1.set_xlim(0,20.0)
ax2.set_xlim(0,20.0)
ax1.set_ylim(0,110)
ax2.set_ylim(0,0.12)
ax1.legend()
ax2.legend(loc=(0.7,0.7))
plt.show()