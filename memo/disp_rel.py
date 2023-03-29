import numpy as np
import matplotlib.pyplot as plt
import cmath

fig, ax = plt.subplots(1,2, figsize=(8,4))

f1 = lambda x: 1/2 + np.sqrt(1/4 - 1/np.tanh(x)/x + 1/x**2)
f2 = lambda x: 1/2 - np.sqrt(1/4 - 1/np.tanh(x)/x + 1/x**2)

x = np.linspace(0.1,5, 1000)
x = [x[i]+0j for i in range(len(x))]
x = np.array(x)

y1_real = [f1(x[i]).real for i in range(len(x))]
y2_real = [f2(x[i]).real for i in range(len(x))]
y1_imag = [f1(x[i]).imag for i in range(len(x))]
y2_imag = [f2(x[i]).imag for i in range(len(x))]

ax[0].plot(x, y1_real)
ax[0].plot(x, y2_real)

ax[1].plot(x, y1_imag)
ax[1].plot(x, y2_imag)

#ax[0].plot(x, np.zeros_like(x), color='black')
ax[0].set_xlim(0,5)

#ax[1].plot(x, np.zeros_like(x), color='black')
ax[1].set_xlim(0,5)

ax[0].set_xlabel(r'$k$')
ax[0].set_ylabel(r'Real part of $c$')

ax[1].set_xlabel(r'$k$')
ax[1].set_ylabel(r'Imaginary part of $c$')

plt.tight_layout()
plt.show()