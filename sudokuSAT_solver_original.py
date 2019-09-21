from z3 import *
import sys
import numpy as np
#
#sys.stdout = open("output.txt", "w")


N = 9

fileName = input("Please Enter The Input File Name: ")

# board = [
#     [7,8,0,4,0,0,1,2,0],
#     [6,0,0,0,7,5,0,0,9],
#     [0,0,0,6,0,1,0,7,8],
#     [0,0,7,0,4,0,2,6,0],
#     [0,0,1,0,5,0,9,3,0],
#     [9,0,4,0,6,0,0,0,5],
#     [0,7,0,3,0,0,0,1,2],
#     [1,2,0,0,0,7,4,0,0],
#     [0,4,9,2,0,6,0,0,7]
# ]


board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

def xorSat(param1, param2):
    return Or(And(Not(param1),param2),And(param1,Not(param2)))


def createInstanceCanstraint(xPosition,yPosition,binaryNumber):
    constraint = []
    for k in range(4):
        if binaryNumber[k]=='1':
            constraint.append(X[xPosition][yPosition][k])
        else:
            constraint.append(Not(X[xPosition][yPosition][k]))

    #print("binaryNumber: ", binaryNumber)
    #print()
    return [And([constraint[i] for i in range(len(constraint))])]


def printMatrix(aList):
    aArray = np.array(aList)
    m = aArray.reshape(N,N)
    print(m.T)


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
        #valueWithinOneToNine.append(Or(And(X[i][j][3], Not(X[i][j][2]), Not(X[i][j][1])), And(Not(X[i][j][3]), Or(X[i][j][2],X[i][j][0],X[i][j][1]))))
        #valueWithinOneToNine.append(Or(And(X[i][j][0], Not(X[i][j][3])), And(X[i][j][2], Not(X[i][j][3])), And(Not(X[i][j][2]), X[i][j][3], Not(X[i][j][1])), And(X[i][j][1]),Not(X[i][j][3])))
        valueWithinOneToNine.append(Or(And(Not(X[i][j][0]),X[i][j][1]),And(X[i][j][0],Not(X[i][j][1]),Not(X[i][j][2])),And(Not(X[i][j][0]),X[i][j][3]),And(Not(X[i][j][0]),X[i][j][2])))



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
            colElemDifferent.append(Or(xorSat(X[i][j][0], X[k][j][0]),xorSat(X[i][j][1], X[k][j][1]),xorSat(X[i][j][2], X[k][j][2]),xorSat(X[i][j][3], X[k][j][3])))

#constraint4
columnConstraint = [And([colElemDifferent[i] for i in range(len(colElemDifferent))])]


boxElemDifferent = []

for i0 in range(3):
    for j0 in range(3):
        boxElement = []
        for i in range(3):
            for j in range(3):
                boxElement.append(X[3*i0 + i][3*j0 + j])
                #print(X[3*i0 + i][3*j0 + j])

        for i in range(len(boxElement)-1):
            for j in range(i+1,len(boxElement),1):
                boxElemDifferent.append(Or(xorSat(boxElement[i][0], boxElement[j][0]),xorSat(boxElement[i][1], boxElement[j][1]),xorSat(boxElement[i][2], boxElement[j][2]),xorSat(boxElement[i][3], boxElement[j][3])))

        boxConstraint = [And([boxElemDifferent[i] for i in range(len(boxElemDifferent))])]


# instanseConstraint_1 = [And(Not(X[0][0][0]), Not(X[0][0][1]), X[0][0][2], X[0][0][3])]
# #instanseConstraint_2 = [And(Not(X[0][1][0]), Not(X[0][1][1]), Not(X[0][1][2]), X[0][1][3])]
# instanseConstraint_2 = [And(Not(X[4][0][0]), X[4][0][1], X[4][0][2], X[4][0][3])]


boardConstraint = []

for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            binNumber = '{0:04b}'.format(board[i][j])
            tempConstraint = createInstanceCanstraint(i,j,binNumber)
            for k in range(len(tempConstraint)):
                boardConstraint.append(tempConstraint[k])
            #boardConstraint.append(createInstanceCanstraint(i,j,binNumber))
            #instanceCellConstraint = [And([X[i][j][k] for k in range(4) if binNumber[k]=='1'])]
            #boardConstraint.append(instanceCellConstraint)

#print(boardConstraint)
#print(boxConstraint)



#print(X)
#print(X[0][0][0])
s = Solver()
s.add(noZeroCell+valueWithinOneToNine+rowConstraint+columnConstraint+boxConstraint+boardConstraint)
#s.add(noZeroCell+rowConstraint+columnConstraint+boxConstraint+boardConstraint)
#s.add(boardConstraint+valueWithinOneToNine)


if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j][k]) for k in range(4) ]
          for j in range(9) for i in range(9)]
    #print_matrix(r)


    aBin = []
    for i in range(len(r)):
        temp = ""
        for j in range(len(r[i])):
            if r[i][j]==True:
                temp = temp+"1"
            else:
                temp = temp+"0"
        aBin.append(temp)

    aBinToDec = []
    for i in range(len(aBin)):
        aBinToDec.append(int(aBin[i],2))
        #print(int(aBin[i],2))

    printMatrix(aBinToDec)
    #print(int(aBin[0],2))

else:
    print("failed to solve")
