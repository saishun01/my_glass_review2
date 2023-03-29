import numpy as np
import matplotlib.pyplot as plt

NLIMIT = 5000

v = 10
c = 1
d = 1
Ds = 1
Dn = 20
R = 15

dt = 0.001
dx = 1
X = 100
x = np.linspace(0,X,int(X/dx))
t = 0

J1S = lambda S: S/(1+S)
J2S = lambda S: 100*S/(100+S)
J1A = lambda S: 32*J1S(S)
J2A = lambda S: J1A(S) + 2*(J2S(S)-J1S(S))

def dif(t,i,N):
    S, N1, N2 = N
    if i == len(x)-1:
        dS = dt*(v - N1[-1]*J1S(S[-1]) - N2[-1]*J2S(S[-1]) + Ds*(S[0] + S[-2] - 2*S[-1])/dx**2)
        dN1 = dt*(c*N1[-1]*J1A(S[-1]) + Dn*(N1[0] + N1[-2] - 2*N1[-1])/dx**2)
        dN2 = dt*(c* N2[-1]*J2A(S[-1]) + Dn*(N2[0] + N2[-2] - 2*N2[-1])/dx**2)
    else:
        dS = dt*(v - N1[i]*J1S(S[i]) - N2[i]*J2S(S[i]) + Ds*(S[i+1] + S[i-1] - 2*S[i])/dx**2)
        dN1 = dt*(c*N1[i]*J1A(S[i]) + Dn*(N1[i+1] + N1[i-1] - 2*N1[i])/dx**2)
        dN2 = dt*(c*N2[i]*J2A(S[i]) + Dn*(N2[i+1] + N2[i-1] - 2*N2[i])/dx**2)
    return [dS, dN1, dN2]

S = 15*np.ones_like(x)
N1 = 1000*np.array([np.exp(-(i-len(x)//4)**2/3/dx) for i in range(len(x))])
N2 = 1000*np.array([np.exp(-(i-3*len(x)//4)**2/3/dx) for i in range(len(x))])
N = [S,N1,N2]


while(t < NLIMIT*dt):
    S_new = np.zeros_like(x)
    N1_new = np.zeros_like(x)
    N2_new = np.zeros_like(x)
    S, N1, N2 = N 
    for i in range(len(x)):
        S_new[i] = S[i] + dif(t,i,N)[0]
        N1_new[i] = N1[i] + dif(t,i,N)[1]
        N2_new[i] = N2[i] + dif(t,i,N)[2]

    N = [S_new,N1_new,N2_new]
    t += dt

plt.figure()
plt.plot(x,N[0])
plt.plot(x,N[1])
plt.plot(x,N[2])
print(N[0])
plt.show()