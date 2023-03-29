import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

k1 = 1 # A + E -> EA
k2 = 0.1 # EA -> A + E
k3 = 1 # EA -> X + F
k4 = 0.01 # X + F -> EA # これをいじると振る舞いがかなり変わる
k5 = 1 # X + F -> FX
k6 = 0.1 # FX -> X + F
k7 = 1 # FX -> X + E

k8 = 0.2 # X + G -> GX
k9 = 0.1 # GX -> X + G
k10 = 0.2 # GX -> Y + G

fig = plt.figure(figsize=(10,3))
ax = fig.subplots(1,3)

# 1つ目のグラフ
A = 0.01

def pinpon(state,t):
    X, E, EA, F, FX, G, GX = state
    dydt = np.zeros_like(state)
    dydt[0] = k3*EA - (k4 + k5)*X*F + (k6+k7)*FX - k8*X*G + k9*GX # X
    dydt[1] = - k1*A*E + k2*EA + k7*FX # E
    dydt[2] = k1*A*E - (k2+k3)*EA # EA
    dydt[3] = k3*EA - (k4+k5)*X*F + k6*FX # F
    dydt[4] = k5*X*F - (k6+k7)*FX # FX
    dydt[5] = - k8*X*G + (k9+k10)*GX #G
    dydt[6] = k8*X*G - (k9+k10)*GX #GX
    return dydt

y0 = np.array([0.5,1.,0,0,0,1.,0])
t = np.arange(0,100,0.1)
y = odeint(pinpon, y0, t)

Gtot = y0[5] + y0[6]

V_mb = k10*Gtot
K_mb = (k9+ k10)/k8

print('A = ', A)
print('V_mb = ', V_mb)
print('K_mb = ', K_mb)

lineObjects = ax[0].plot(t, y[:,0:5])
ax[0].legend(iter(lineObjects), ('X', 'E', 'EA', 'F', 'FX', 'G', 'GX'))
ax[0].set_title("A = " + str(A))

print('X* = ', y[-1,0])

# 2つ目のグラフ
A = 0.1

y = odeint(pinpon, y0, t)

Gtot = y0[5] + y0[6]

V_mb = k10*Gtot
K_mb = (k9+ k10)/k8

print('A = ', A)
print('V_mb = ', V_mb)
print('K_mb = ', K_mb)

lineObjects = ax[1].plot(t, y[:,0:5])
ax[1].legend(iter(lineObjects), ('X', 'E', 'EA', 'F', 'FX', 'G', 'GX'))
ax[1].set_title("A = " + str(A))

print('X* = ', y[-1,0])

# 3つ目のグラフ
A = 0.5

y = odeint(pinpon, y0, t)

Gtot = y0[5] + y0[6]

V_mb = k10*Gtot
K_mb = (k9+ k10)/k8

print('A = ', A)
print('V_mb = ', V_mb)
print('K_mb = ', K_mb)

lineObjects = ax[2].plot(t, y[:,0:5])
ax[2].legend(iter(lineObjects), ('X', 'E', 'EA', 'F', 'FX', 'G', 'GX'))
ax[2].set_title("A = " + str(A))

print('X* = ', y[-1,0])
plt.show()