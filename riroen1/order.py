import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


fig = plt.figure(figsize=(10,3))
ax = fig.subplots(1,3)

# A, X order

k1 = 1 # A + E -> EA
k2 = 0.1 # EA -> A + E
k3 = 1 # EA + X -> EAX
k4 = 0.1 # EAX -> EA + X
k5 = 1 # EAX -> EXX
k6 = 0.1 # EXX -> EAX
k7 = 1 # EXX -> 2X + E

k8 = 0.5 # X + G -> GX
k9 = 0.5 # GX -> X + G
k10 = 1 # GX -> Y + G



A = 100

def axorder(state,t):
    X, E, EA, EAX, EXX, G, GX = state
    dydt = np.zeros_like(state)
    dydt[0] = - k3*EA*X + k4*EAX + 2*k7*EXX - k8*X*G + k9*GX # X
    dydt[1] = - k1*A*E + k2*EA + k7*EXX # E
    dydt[2] = k1*A*E - (k2+k3*X)*EA + k4*EAX # EA
    dydt[3] = k3*EA*X - (k4+k5)*EAX + k6*EXX # EAX
    dydt[4] = k5*EAX - (k6+k7)*EXX # EXX
    dydt[5] = - k8*X*G + (k9+k10)*GX #G
    dydt[6] = k8*X*G - (k9+k10)*GX #GX
    return dydt

y0 = np.array([0.5,1.,0,0,0,1.,0])
t = np.arange(0,100,0.1)
y = odeint(axorder, y0, t)

Gtot = y0[5] + y0[6]

V_mb = k10*Gtot
K_mb = (k9+ k10)/k8

print('A = ', A)
print('V_mb = ', V_mb)
print('K_mb = ', K_mb)

lineObjects = ax[0].plot(t, y[:,0:5])
ax[0].legend(iter(lineObjects), ('X', 'E', 'EA', 'EAX', 'EXX', 'G', 'GX'))
ax[0].set_title("A, X order, A = " + str(A))

#ax[1].plot(t,y[:,1]+y[:,2]+y[:,3]+y[:,4])

print('X* = ', y[-1,0])

# X, A order

k1 = 1 # X + E -> EX
k2 = 0.1 # EX -> X + E
k3 = 1 # EX + A -> EXA
k4 = 0.1 # EXA -> EX + X
k5 = 1 # EXA -> EXX
k6 = 0.1 # EXX -> EXA
k7 = 1 # EXX -> 2X + E

k8 = 0.5 # X + G -> GX
k9 = 0.5 # GX -> X + G
k10 = 1 # GX -> Y + G

def axorder(state,t):
    X, E, EX, EXA, EXX, G, GX = state
    dydt = np.zeros_like(state)
    dydt[0] = - k1*X*E + k2*EX + k4*EXA + 2*k7*EXX - k8*X*G + k9*GX # X
    dydt[1] = - k1*X*E + k2*EX + k7*EXX # E
    dydt[2] = k1*X*E - (k2+k3*A)*EX + k4*EXA # EX
    dydt[3] = k3*EX*A - (k4+k5)*EXA + k6*EXX # EAX
    dydt[4] = k5*EXA - (k6+k7)*EXX # EXX
    dydt[5] = - k8*X*G + (k9+k10)*GX #G
    dydt[6] = k8*X*G - (k9+k10)*GX #GX
    return dydt

y0 = np.array([0.5,1.,0,0,0,1.,0])
t = np.arange(0,100,0.1)
y = odeint(axorder, y0, t)

Gtot = y0[5] + y0[6]

V_mb = k10*Gtot
K_mb = (k9+ k10)/k8

print('A = ', A)
print('V_mb = ', V_mb)
print('K_mb = ', K_mb)

lineObjects = ax[1].plot(t, y[:,0:5])
ax[1].legend(iter(lineObjects), ('X', 'E', 'EX', 'EXA', 'EXX', 'G', 'GX'))
ax[1].set_title("X, A order, A = " + str(A))

#ax[1].plot(t,y[:,1]+y[:,2]+y[:,3]+y[:,4])

print('X* = ', y[-1,0])


plt.show()