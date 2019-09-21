from z3 import *
import sys

N = 9


def createInstanceCanstraint(xPosition,yPosition,binaryNumber):
    constraint = []
    for k in range(4):
        if binaryNumber[k]=='1':
            constraint.append(X[xPosition][yPosition][k])
        else:
            constraint.append(Not(X[xPosition][yPosition][k]))

    return [And([constraint[i] for i in range(len(constraint))])]



#sys.stdout = open("output.txt", "w")
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



#print(boxElement)

#print(X)
# for i in range(N):
#     for j in range(N):
#         for p in range(i,N):
#             for q in range(N):
#                 if not(p==i and q==j):
#                     print(X[i][j], X[p][q])


board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

boardConstraint = []

for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            binNumber = '{0:04b}'.format(board[i][j])
            boardConstraint.append(createInstanceCanstraint(i,j,binNumber))
            #instanceCellConstraint = [And([X[i][j][k] for k in range(4) if binNumber[k]=='1'])]
            #boardConstraint.append(instanceCellConstraint)

print(boardConstraint)
            #indexTrue = [i for i, e in enumerate(binNumber) if e=='1']
