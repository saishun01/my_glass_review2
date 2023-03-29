import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-np.pi,np.pi)
y = 2*np.cos(x/2)
plt.plot(x,y)
plt.xlim(-np.pi,np.pi)
plt.ylim(-0.1,2.1)
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], ["$-\pi$", "$-\pi/2$", "$0$", "$\pi/2$", "$\pi$"])
plt.xlabel("Phase difference $\delta$")
plt.ylabel("Amplitude")
plt.grid()
plt.title("Interference of sine waves")
plt.show()