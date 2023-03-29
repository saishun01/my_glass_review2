import numpy as np

for u in range(2,11):
    for v in range(1,u):
        a = u**2 - v**2
        b = 2*u*v
        c = u**2 + v**2
        print('(u, v) = ({}, {}) : (a, b, c) = ({}, {}, {})'.format(u,v,a,b,c))