import numpy as np

#単位はmV
lv = 8
hv = 1060
volt_10 = lv + (hv-lv)*0.1
volt_90 = lv + (hv-lv)*0.9
print(volt_10,volt_90)

#単位はns
t_disp = 2.72
f_osc = 200
t_osc = 350 / f_osc
t_pulse = np.sqrt(t_disp**2 - t_osc**2)
print(t_pulse)

v = (501.9 - 101.7)/(26.8 - 5.28)
print(v)

c = 29.9792458
print(v/c)