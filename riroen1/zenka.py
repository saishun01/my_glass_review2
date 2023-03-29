from termios import N_SLIP
import numpy as np
import matplotlib.pyplot as plt
Ns = 10
p_list = np.arange(0,1,0.01)
q_list = []
for i in range(len(p_list)):
    p = p_list[i]

    q = p
    for i in range(2,Ns):
        q = q*(1+(1-q)*p)
    q_list.append(q)

plt.plot(p_list,q_list)
plt.show()