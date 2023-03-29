import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,2, figsize=(8,4))
z = np.linspace(0,1)
ax[0].plot(z, np.exp(-z), label=r'$k = 1$')
ax[1].plot(z, np.exp(z), label=r'$k = 1$')
ax[0].plot(z, np.exp(-4*z), label=r'$k = 4$')
ax[1].plot(z, np.exp(4*z), label=r'$k = 4$')

ax[0].set_title(r'Captured by $z = 0$')
ax[1].set_title(r'Captured by $z = 1$')

for i in range(2):
    ax[i].set_xlabel(r'$z$')
    ax[i].set_ylabel(r'$\Psi(z)$')
    ax[i].set_xlim(0,1)

    ax[i].legend()

plt.tight_layout()
plt.show()