import numpy as np
import matplotlib.pyplot as plt
import cmath

f1 = lambda x: 1/2 + np.sqrt(1/4 - 1/np.tanh(x)/x + 1/x**2)
f2 = lambda x: 1/2 - np.sqrt(1/4 - 1/np.tanh(x)/x + 1/x**2)

k1 = 1.6 + 0j 
c1 = f1(k1)
c2 = f2(k1)

z = np.linspace(0,1)
Psi1 = np.sinh(k1*z) - c1*k1*np.cosh(k1*z)
Psi2 = np.sinh(k1*z) - c2*k1*np.cosh(k1*z)

k2 = 4.0 + 0j
c3 = f1(k2)
c4 = f2(k2)
Psi3 = np.sinh(k2*z) - c3*k2*np.cosh(k2*z)
Psi4 = np.sinh(k2*z) - c4*k2*np.cosh(k2*z)

APsi1 = [abs(Psi1[i]) for i in range(len(z))]
APsi2 = [abs(Psi2[i]) for i in range(len(z))]
APsi3 = [abs(Psi3[i]) for i in range(len(z))]
APsi4 = [abs(Psi4[i]) for i in range(len(z))]

PPsi1 = [cmath.phase(Psi1[i]) for i in range(len(z))]
PPsi2 = [cmath.phase(Psi2[i]) for i in range(len(z))]
PPsi3 = [cmath.phase(Psi3[i]) for i in range(len(z))]
PPsi4 = [cmath.phase(Psi4[i]) for i in range(len(z))]

fig, ax = plt.subplots(2,2, figsize=(8,6))
ax[0,0].plot(z, APsi1)
ax[0,1].plot(z, PPsi1)
ax[0,0].plot(z, APsi2)
ax[0,1].plot(z, PPsi2)

ax[1,0].plot(z, APsi3)
ax[1,1].plot(z, PPsi3)
ax[1,0].plot(z, APsi4)
ax[1,1].plot(z, PPsi4)


ax[0,0].set_xlabel(r'$z$')
ax[0,1].set_xlabel(r'$z$')
ax[0,0].set_ylabel(r'Absolute value of $\Psi(z)$')
ax[0,1].set_ylabel(r'Phase of $\Psi(z)$')

ax[1,0].set_xlabel(r'$z$')
ax[1,1].set_xlabel(r'$z$')
ax[1,0].set_ylabel(r'Absolute value of $\Psi(z)$')
ax[1,1].set_ylabel(r'Phase of $\Psi(z)$')

for i in range(2):
    for j in range(2):
        ax[i,j].set_xlim(0,1)


ax[0,0].set_ylim(0,1)
ax[0,1].set_ylim(-3,3)
ax[1,0].set_ylim(0,60)
ax[1,1].set_ylim(3.0,3.3)

ax[0,0].set_title(r'$k = 1.6$')
ax[0,1].set_title(r'$k = 1.6$')
ax[1,0].set_title(r'$k = 4$')
ax[1,1].set_title(r'$k = 4$')

plt.tight_layout()
plt.show()