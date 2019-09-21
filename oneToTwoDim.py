import numpy as np
a = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]

aArray = np.array(a)
m = aArray.reshape(4,4)
print(m.T)


#rez = [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

#print(rez)
# for j in range(len(a)):
#     b.append([[a[i] for i in range(0,len(a),4)]])
#
# print(b)
#
# print(aMatrix)
