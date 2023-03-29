import numpy as np

a = 34
b = 0

# a >= bとなるようにする
if b > a:
    tmp = a
    a = b
    b = tmp

# a = 0, b = 0のときは回さないように
if a != 0 and b != 0:
    r_ = a
    r = b
    while(r != 0):
        r_tmp = r_ % r
        r_ = r
        r = r_tmp
    print('gcd({}, {}) = {}'.format(a, b, r_))

else:
    print('Error')