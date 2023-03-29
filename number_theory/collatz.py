import numpy as np

n = 56

def collatz(n):

    n_list = []
    n_list.append(n)

    flag = False
    while(flag==False):
        # n_listを更新
        if n_list[-1] % 2 == 0:
            n_list.append(n_list[-1]//2)
        else:
            n_list.append(3*n_list[-1]+1)
        
        # 繰り返しがないかチェック
        for i in range(len(n_list)-1):
            if n_list[i] == n_list[-1]:
                flag = True

    L = len(n_list) - 1
    T = n_list[-2]
    return L, T

# 表を作る

for n in range(1,101):
    L, T = collatz(n)
    print('n = {} : L(n) = {}, T(n) = {}'.format(n, L, T))
