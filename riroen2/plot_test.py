import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
cmap = plt.get_cmap("tab10")

X = np.arange(0,1-0.1)
f = lambda X: np.power(1-X, -1)
Y = f(X)
print(X)
print(Y)
ax.plot(X, Y)
plt.show()