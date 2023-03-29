def calc_mod(a, k, m):

    b = 1
    while(k >= 1):
        if k % 2 == 1:
            b = a*b % m
        a = a**2 % m
        k = k // 2
    return b

print(calc_mod(2,9990,9991))