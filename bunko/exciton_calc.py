import numpy as np

#me_,mh_,mu_はmeを1とする単位
me_ = 0.99
mh_ = 0.58
mu_ = 1/(1/me_ + 1/mh_)

N = 5
n = np.arange(1, N+1)
er = 7.3
E = 13.605693
E_ex = lambda n: mu_/er**2*E/n**2*1000
wl_ex = lambda e: 1239.8/e*1000

Eg = 2170
k_B = 8.6217*10**(-2)

a_H = 0.053
a_B = er*a_H/mu_

R = 13.605693
R_ = mu_*R/er**2

print('mass(/me): ', mu_)
print('Bohr radius(nm): ', a_B)
print('R: ', R_)

for i in range(0, N):
    print('n:', n[i])
    print('\t Energy(meV): ', E_ex(n[i]))
    print('\t Trans Energy(eV): ', 2.17-E_ex(n[i])*0.001)
    print('\t Wavelength(nm): ', wl_ex(2170-E_ex(n[i])))
    print('\t Temperature(K): ', E_ex(n[i])/k_B)