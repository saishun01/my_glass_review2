import random
import numpy as np
import matplotlib.pyplot as plt

TRIAL = 10000 #試行回数
NMAX = 10000 #諦めるまでの試行回数
p = 0.5
t_list = np.array([])
STR = 'HTHH'

for j in range(TRIAL):
    S = ''
    for i in range(NMAX):
        I = random.random()
        if I < p:
            S += 'H'
        else:
            S += 'T'
        
        if i+1 < len(STR):
            continue

        #print(S) #テスト用

        if S[i+1-len(STR):i+1] == STR:
            t_list = np.append(t_list, i+1)
            break

        if i == NMAX-1:
            t_list = np.append(t_list,NMAX)
        

#print(t_list) #テスト用
t_ave = np.average(t_list)
print('Probability: ', p)
print('String:', STR)
print('T average: ', t_ave)

plt.figure()
plt.hist(t_list, bins=2*int(np.max(t_list)))
plt.show()
