import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

random.seed(10)

Nx = 256
Ny = 256

def neighor_spin_sum(s, x, y):
    """近接スピンの和を計算

    Parameters
    --------------------
    s : スピン配位
    x : 格子点のx座標
    y : 格子点のy座標

    Returns
    --------------------
    neighor_spin_sum : 近接スピンの和
    """
    x_right=x+1
    x_left=x-1
    y_up=y+1
    y_down=y-1

    # 周期境界条件
    if x_right>=Nx:
        x_right-=Nx
    if x_left<0:
        x_left+=Nx
    if y_up>=Ny:
        y_up-=Ny
    if y_down<0:
        y_down+=Ny

    neighor_spin_sum=s[x_right][y]+s[x_left][y]+s[x][y_up]+s[x][y_down]
    return neighor_spin_sum

def calc_energy(s, h=0.01):
    """エネルギーを計算

    Parameters
    --------------------
    s : スピン配位
    h : 外部磁場(バイアス)

    Returns
    --------------------
    energy : エネルギー
    """
    energy = 0
    for x in range(Nx):
        for y in range(Ny):
            # dobule count
            energy += - neighor_spin_sum(s, x, y)/2
    energy += h*np.sum(s)
    return energy

def metropolis(s, beta=1, h=0.001):
    """メトロポリス法

    Parameters
    --------------------
    s : スピン配位
    beta : 逆温度パラメータ
    h : 外部磁場(バイアス)

    Returns
    --------------------
    s : 更新後のスピン配位
    """
    xs=list(range(Nx))
    random.shuffle(xs)
    ys=list(range(Ny))
    random.shuffle(ys)
    for x in xs:
        for y in ys:
            k=neighor_spin_sum(s, x, y)+h
            trans_prob = np.exp(-2*beta*s[x][y]*k)
            if np.random.random()<=trans_prob:
                s[x][y] = -s[x][y]
    return s   

def gibbs_sampling(s, beta=1.0, h=0.001):
    """ギブスサンプリング

    Parameters
    --------------------
    s : スピン配位
    beta : 逆温度パラメータ
    h : 外部磁場(バイアス)

    Returns
    --------------------
    s : 更新後のスピン配位
    """
    xs=list(range(Nx))
    random.shuffle(xs)
    ys=list(range(Ny))
    random.shuffle(ys)
    for x in xs:
        for y in ys:
            k=neighor_spin_sum(s, x, y)-h
            trans_prob = np.exp(beta*k) / (np.exp(beta*k)+np.exp(-beta*k))
            if np.random.random()<=trans_prob:
                s[x][y]=1
            else:
                s[x][y]=-1
    return s

def mcmc(s, steps=1000, beta=1.0, h=0.001, method='metropolis', interval=10, burn_in=10**2, animation=True, ani_interval=10):
    """マルコフ連鎖モンテカルロ法を実行
    
    Parameters
    -------------------
    s : 初期スピン配位
    steps : モンテカルロステップ
    beta : 逆温度パラメータ
    h : 外部磁場(バイアス)
    method : モンテカルロ法の手法, メトロポリス法 : metropolis, ギブスサンプリング : gibbs
    interval : サンプルを取得するインターバル
    burn_in : バーンインタイム

    Returns
    -------------------
    ms : 各ステップの磁化のリスト
    energies : 各ステップのエネルギーのリスト
    square_energies : 各ステップのエネルギーの二乗のリスト
    """
    ms=[]
    energies=[]
    square_energies=[]
    # Metropolis 
    if method=='metropolis':
        for step in range(steps):
            s = metropolis(s, beta=beta, h=h)
            # 自己相関が切れる部分かつburn inを捨てる
            if (step%interval==0)&(step>=burn_in):
                # 磁化を計算
                m = np.sum(s) / (Nx*Ny)
                # エネルギーを計算
                energy = calc_energy(s, h=h)
                # エネルギーの二乗を計算
                square_energy = energy**2 
                ms.append(m)
                energies.append(energy)
                square_energies.append(square_energy)

    # Gibbs
    elif method=='gibbs':
        for step in range(steps):
            s = gibbs_sampling(s, beta=beta, h=h)
            if (step%interval==0)&(step>=burn_in):
                # 磁化を計算
                m = np.sum(s) / (Nx*Ny)
                # エネルギーを計算
                energy = calc_energy(s, h=h) 
                # エネルギーの二乗を計算
                square_energy = energy**2
                ms.append(m)
                energies.append(energy)
                square_energies.append(square_energy)
    return ms, energies, square_energies
"""
# 格子の大きさ
Nx = 32
Ny = 32
steps=10**4
# 初期配位
s = np.ones((Nx, Ny)).tolist()
ms, energies, square_energies=mcmc(s, steps=steps, beta=0.1, h=0.0)

# 磁化
time = np.arange(1, len(ms)+1)
fig, ax=plt.subplots()
ax.plot(time, ms)
ax.set_ylim([-1.1, 1.1])
ax.set_xlabel('MCS', fontsize=20)
ax.set_ylabel('Magnetization', fontsize=20)
plt.tick_params(axis='y', width=1, length=4, pad=5, color='k', direction='in', labelsize=15, labelcolor='k')
plt.tick_params(axis='x', width=1, length=4, pad=5, color='k', direction='in', labelsize=15, labelcolor='k')
plt.show()
"""

Nx = 256
Ny = 256
steps=100
# 初期配位
s = np.random.randint(0, 2, (Nx, Ny)).tolist()
fig, ax = plt.subplots()
ims = []
im = ax.imshow(s, animated=True)
ims.append([im])
for step in range(steps):
    s = gibbs_sampling(s, beta=0.44, h=0)
    im = ax.imshow(s, animated=True)
    ims.append([im])

# ArtistAnimationにfigオブジェクトとimsを代入してアニメーションを作成
anim = animation.ArtistAnimation(fig, ims)
# Google Colaboratoryの場合必要
#rc('animation', html='jshtml')
plt.close()
anim