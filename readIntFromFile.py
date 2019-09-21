with open('sudoku.txt', 'r') as f:
    l = [[int(num) for num in line.split(',')] for line in f]
#print(l)


for n, i in enumerate(l):
    for k, j in enumerate(i):
        l[n][k] = int(j)
print(l)
