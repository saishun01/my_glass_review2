import numpy as np
import matplotlib.pyplot as plt

#plt.rcParams['font.family'] = "MS Gothic"
plt.rcParams['font.family'] = "Meiryo"

f = lambda x,a: a*x
g = lambda x,y:y

fig, axes = plt.subplots(nrows=2, ncols=2, sharex=False)

XMIN = -1
XMAX = 1
X = np.linspace(XMIN,XMAX)

axes[0,0].fill_between(X,f(X,1),f(X,-0.5), facecolor='gray')
axes[0,1].set_facecolor('gray')
axes[0,1].fill_between(X,f(X,1),f(X,-0.5), facecolor='white')
axes[1,0].fill_between(X,f(X,1),f(X,2), facecolor='gray')
axes[1,1].set_facecolor('gray')
axes[1,1].fill_between(X,f(X,1),f(X,2), facecolor='white')

for i in range(2):
    for j in range(2):        
        axes[i,j].plot(X,f(X,1),color='black')
        axes[i,j].set_title('('+str(i+2*j+1)+')',loc='left')
        axes[i,j].set_xlabel(r"野生型の戦略$\,x$")
        axes[i,j].set_ylabel(r"変異型の戦略$\,x'$")
        axes[i,j].set_xlim(XMIN,XMAX)
        axes[i,j].set_ylim(XMIN,XMAX)
        axes[i,j].tick_params(labelbottom=False,labelleft=False)
        axes[i,j].tick_params(bottom=False,left=False)

fig.tight_layout()
plt.show()