import numpy as np
import matplotlib.pyplot as plt

R = 13.605693122994
A = np.array([0.063,0.22,0.64,0.025,0.095,0.204,0.012,0.049,0.094,0.007,0.029,0.048])

I = []
for n in range(3,7):
    A_1 = A[3*n-9]
    A_3 = A[3*n-8]
    A_5 = A[3*n-7]
    A_n = 1*A_1 + 3*A_3 + 5*A_5
    E_n = R*(1/4 - 1/n**2)
    I_n = E_n*A_n
    I.append(I_n)


N = np.arange(3,7)
I = np.array(I)

plt.figure()
plt.scatter(N,I)

plt.xlim(2.8,6.2)
plt.ylim(0.7,10)

plt.yscale('log')

plt.xlabel('$n$')
plt.ylabel('Intensity (eV)')

plt.xticks([3,4,5,6])
plt.grid(axis='x', which='major')
plt.grid(axis='y', which='both')
plt.show()