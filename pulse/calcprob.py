import numpy as np

#計測時間
t = 1434.4

#カウントされた回数
N1 = 24970
N2 = 17935055

#Widthはns単位
W1 = 60.0
W2 = 59.2

p1 = W1*10**(-9)*N1/t
p2 = W2*10**(-9)*N2/t

print(p1*p2)