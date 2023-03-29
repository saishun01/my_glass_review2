import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,2, figsize=(8,4))

z = np.linspace(0,1)
ax[0].plot(z, 3*np.exp(-z)+np.exp(z))
ax[1].plot(z, 3*np.exp(-4*z)+np.exp(4*z))

for i in range(2):
    ax[i].set_xlabel(r'$z$')
    ax[i].set_ylabel(r'Sum of $\Psi(z)$ captured by $z = 0,\,1$')
    ax[i].set_xlim(0,1)

    ax[i].legend()

plt.tight_layout()
plt.show()