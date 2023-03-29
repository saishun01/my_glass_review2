import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
b = 1
prob = 0.95

x_list = []
x0 = 0
x_list.append(x0)
for i in range(1000):
    x = x_list[-1]
    if np.random.random() < prob:
        x += b/prob
    x_list.append(x-b)

plt.plot(x_list)
plt.show()
