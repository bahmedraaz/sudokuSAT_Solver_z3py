from z3 import *
import sys

N = 9

sys.stdout = open("output.txt", "w")
# 9x9 matrix of integer variables
X = [ [ BoolVector("x_%s_%s" % (i+1, j+1), 4) for j in range(N) ] for i in range(N)]

#toDO
# for (unsigned i0 = 0; i0 < 3; i0++) {
#         for (unsigned j0 = 0; j0 < 3; j0++) {
#             expr_vector t(c);
#             for (unsigned i = 0; i < 3; i++)
#                 for (unsigned j = 0; j < 3; j++)
#                     t.push_back(x[(i0 * 3 + i) * 9 + j0 * 3 + j]);
#             s.add(distinct(t));
#         }
#     }

boxElement = []

for i0 in range(1):
    for j0 in range(1):
        for i in range(3):
            for j in range(3):
                boxElement.append(X[3*i0 + i][3*j0 + j])
                #print(X[3*i0 + i][3*j0 + j])



print(boxElement)

#print(X)
# for i in range(N):
#     for j in range(N):
#         for p in range(i,N):
#             for q in range(N):
#                 if not(p==i and q==j):
#                     print(X[i][j], X[p][q])
