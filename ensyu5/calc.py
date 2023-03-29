def N(n):
    return (n+3)*(n+2)*(n+1)/3

def E(n):
    return (n+3)*(n+2)**2*(n+1)/4

for n in range(0,6):
    print(n, N(n), E(n))