import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

s = 0.5
q0 = 0.005
t_max = 40


def q_next(q):
    return q + s*q*(1-q)/(1+2*s*q)
Q = [q0]
t = 0
while(t < t_max):
    q = Q[t]
    q_ = q_next(q)
    Q.append(q_)
    t += 1

def q_exact(t):
    return 1/(1 + (1-q0)/q0*np.exp(-s*t))

plt.figure()
T = np.arange(0, t+1)
plt.plot(T, Q, label=r'$q_{t+1} - q_{t} = s q_t (1-q_t) / w_t$')
plt.plot(T, q_exact(T), label=r'Exact solution of logistic equation')

plt.xlim(0,t_max)
plt.ylim(0,1)
plt.legend()
plt.show()