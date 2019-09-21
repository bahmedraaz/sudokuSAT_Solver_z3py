a = [[True, False],[True, True]]
aBin = []


for i in range(len(a)):
    temp = ""
    for j in range(len(a[i])):
        if a[i][j]==True:
            temp = temp+"1"
        else:
            temp = temp+"0"
    aBin.append(temp)

for i in range(len(aBin)):
    print(int(aBin[i],2))
