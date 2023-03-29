import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,np.pi, 10000)
y = -np.cos(x)**2 *np.log(np.cos(x)**2) -np.sin(x)**2 *np.log(np.sin(x)**2)

plt.plot(x,y)
plt.show()