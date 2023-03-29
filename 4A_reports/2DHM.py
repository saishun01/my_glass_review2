import numpy as np
import matplotlib.pyplot as plt

e = lambda x,y: -2*(np.cos(x) + np.cos(y))

x = np.linspace(-np.pi, np.pi, 1000)
y = np.linspace(-np.pi, np.pi, 1000)

X, Y = np.meshgrid(x, y)
Z = e(X,Y)

cont = plt.contour(X, Y, Z, levels=[-3.9, -3.5, -3, -2, -0.5, 0, 0.5, 3])
cont.clabel(fmt='%1.1f', fontsize=10)
plt.gca().set_aspect('equal')

plt.xlabel(r'$k_x a$')
plt.ylabel(r'$k_y a$')
plt.show()