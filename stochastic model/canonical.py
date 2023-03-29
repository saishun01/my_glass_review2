import numpy as np
import random
import matplotlib.pyplot as plt

N = 4 #人数
mean = 1 #最初に各人に配る数
M = 100 #試行回数
DISTMAX = 5 #一人に注目したときの分布をどこまでとるか
state = np.ones(N)*mean
#print(state)

#up/downカウント
uu = 0
ud = 0
du = 0
dd = 0

person = [state[0]]

for i in range(M):
    x = random.randint(0,N-1)
    y = random.randint(0,N-1)

    if state[x]==0:
        person.append(state[0])
        continue

    state[x] -= 1
    state[y] += 1

    person.append(state[0])

fig = plt.figure(tight_layout=True)

#全体の分布
X = np.arange(0,DISTMAX)

phist = np.histogram(state, bins=X)
pdist = phist[0]
#print(int(np.max(state)))

if len(pdist) > DISTMAX:
    pdist = pdist[0:DISTMAX]
while len(pdist) < DISTMAX:
    pdist = np.append(pdist,0)
#print(pdist)

ax1 = fig.add_subplot(2,2,1)
#ax1.hist(state, bins=int(np.max(state))) 
ax1.scatter(X,pdist)
ax1.set_title('Final distribution')

#一人に注目したときの遷移
time = np.arange(0,M+1)
ax2 = fig.add_subplot(2,2,2)
ax2.plot(time, person) 
ax2.set_title('Path of one person')

#一人に注目したとき、各枚数持っていた累計時間
X = np.arange(0,DISTMAX)
phist = np.histogram(person, bins=X)
pdist = phist[0]

if len(pdist) > DISTMAX:
    pdist = pdist[0:DISTMAX]
while len(pdist) < DISTMAX:
    pdist = np.append(pdist,0)

ax3 = fig.add_subplot(2,2,3)
ax3.scatter(X,pdist) 
ax3.set_title('Distribution expected by the person')

plt.show()