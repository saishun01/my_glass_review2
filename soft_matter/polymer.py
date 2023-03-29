import numpy as np
import matplotlib.pyplot as plt

L = 100
n = 64
T = 5000

K = 0

M = np.zeros((L,L))

monomers = np.zeros(n)


for k in range(n):
    i = int(99*k/100) + 1
    j = int((k-1)/100) + 1
    M[i,j] = 1

