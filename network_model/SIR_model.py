import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def SIR_EQ(v,t,beta,gamma):
    return [-beta*v[0]*v[1], beta*v[0]*v[1]-gamma*v[1], gamma*v[1]]

t_max = 120
dt = 0.01
beta_const = 0.001
gamma_const = 0.3

S_0 = 499
I_0 = 1
R_0 = 0
ini_state = [S_0, I_0, R_0]

times = np.arange(0,t_max,dt)
args = (beta_const, gamma_const)

result = odeint(SIR_EQ, ini_state, times, args)

plt.plot(times, result)
plt.legend(['Susceptible', 'Infections', 'Removed'])
plt.show()