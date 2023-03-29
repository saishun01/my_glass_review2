import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,2, figsize=(8,4))

k = np.linspace(0.1,5, 100)
ax[0].plot(k, 1-np.power(k,-1))
ax[1].plot(k, np.power(k,-1))

ax[0].set_title(r'Captured by $z=1$')
ax[1].set_title(r'Captured by $z=0$')

for i in range(2):
    ax[i].set_xlabel(r'$k$')
    ax[i].set_ylabel(r'$c$')
    ax[i].set_xlim(0,5)

plt.tight_layout()
plt.show()