from z3 import *
import sys
sys.stdout = open("output.txt", "w")


N = 3

def xorSat(param1, param2):
    return Or(And(Not(param1),param2),And(param1,Not(param2)))


# 9x9 matrix of integer variables
X = [ [ BoolVector("x_%s_%s" % (i+1, j+1), 4) for j in range(N) ] for i in range(N)]

#cols_c   = [ Distinct([ X[i][j] for i in range(9) ]) for j in range(9) ]
#cols_c   = [ Or([ X[0][0][k] for k in range(9) ])]
#consNoZeroCell = [Or([X[0][0][k]for k in range(N))]

#print(X[0][0])

#constraint1
noZeroCell = []

for i in range(N):
    for j in range(N):
        noZeroCell.append(Or(X[i][j][0],X[i][j][1],X[i][j][2],X[i][j][3]))


#constraint2
valueWithinOneToNine = []

for i in range(N):
    for j in range(N):
        valueWithinOneToNine.append(Or(And(X[i][j][3], Not(X[i][j][2]), Not(X[i][j][1])), And(Not(X[i][j][3]), Or(X[i][j][2],X[i][j][0],X[i][j][1]))))



#print(X)

rowElemDifferent = []
# for i in range(N):
#     for j in range(N):
#         for k in range(j+1,N,1):
#             print(X[i][j], X[i][k])


for i in range(N):
    for j in range(N-1):
        for k in range(j+1,N,1):
            rowElemDifferent.append(Or(xorSat(X[i][j][0], X[i][k][0]),xorSat(X[i][j][1], X[i][k][1]),xorSat(X[i][j][2], X[i][k][2]),xorSat(X[i][j][3], X[i][k][3])))

#constraint3
rowConstraint = [And([rowElemDifferent[i] for i in range(len(rowElemDifferent))])]



colElemDifferent = []
for j in range(N):
    for i in range(N-1):
        for k in range(i+1,N,1):
            #print(X[i][j], X[k][j])
            colElemDifferent.append(Or(xorSat(X[i][j][0], X[k][j][0]),xorSat(X[i][j][1], X[i][k][1]),xorSat(X[i][j][2], X[i][k][2]),xorSat(X[i][j][3], X[i][k][3])))

#constraint4
columnConstraint = [And([colElemDifferent[i] for i in range(len(colElemDifferent))])]


print(columnConstraint)
#print(X)
#print(rowElemDifferent)
#print(rowConstraint)


# s = Solver()
# s.add(noZeroCell+valueWithinOneToNine+rowConstraint)
# print(s.check())
