
a = [[None for i in range(5)] for j in range(5)]

for j in range(5):
    if j == 0:
        for i in range(5):
            a[j][i] = i
    elif j>0 and (j%2) != 0:
        for i in range(5):
            a[j][4 - i] =  5*j + i
            # 5*(j+1) - 1 - i
    elif j>0 and (j%2) == 0:
        for i in range(5):
            a[j][i] = 5*j + i



print(a)
