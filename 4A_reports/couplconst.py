import numpy as np

Q_list = [10, 100, 1000]
for i in range(len(Q_list)):

    Q = Q_list[i]*10**9 # eV G=10^9, T=10^12

    a = 1/(137-1/3/np.pi*np.log((Q/511*10**3)**2))

    a_S = 0.119/(1+0.119*23/12/np.pi*np.log((Q/91.2*10**9)**2))

    print('Q = {} GeV'.format(Q/10**9))
    print('a = {}'.format(a))
    print('a_S = {}'.format(a_S))