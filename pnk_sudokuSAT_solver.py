from z3 import *
import numpy as np

#N = 9

with open('sudoku.txt', 'r') as f:
    board = [[int(num) for num in line.split(',')] for line in f]
#print(l)


for n, i in enumerate(board):
    for k, j in enumerate(i):
        board[n][k] = int(j)

initialMatrix = []

for row in range(9):
    tempCell = []
    for col in range(9):
        tempCell.append(BoolVector("a_{}_{}".format(row, col), 4))
    initialMatrix.append(tempCell)

s = Solver()
#s.add(noZeroCell+valueWithinOneToNine+rowConstraint+columnConstraint+boxConstraint+boardConstraint)
valueWithinOneToNine = []
noZeroCell = []

for i in range(9):
    for j in range(9):
        valueWithinOneToNine.append(Or(And(Not(initialMatrix[i][j][0]),initialMatrix[i][j][1]),And(initialMatrix[i][j][0],Not(initialMatrix[i][j][1]),Not(initialMatrix[i][j][2])),And(Not(initialMatrix[i][j][0]),initialMatrix[i][j][3]),And(Not(initialMatrix[i][j][0]),initialMatrix[i][j][2])))
        noZeroCell.append(Or(initialMatrix[i][j][0],initialMatrix[i][j][1],initialMatrix[i][j][2],initialMatrix[i][j][3]))

s.add(valueWithinOneToNine)
s.add(noZeroCell)

rowElemDifferent = []
for row in range(9):
    for col in range(8):
        for k in range(col+1,9,1):
            rowElemDifferent.append(Or(
                                        Or(And(Not(initialMatrix[row][col][0]),initialMatrix[row][k][0]),And(initialMatrix[row][col][0],Not(initialMatrix[row][k][0]))),
                                        Or(And(Not(initialMatrix[row][col][1]),initialMatrix[row][k][1]),And(initialMatrix[row][col][1],Not(initialMatrix[row][k][1]))),
                                        Or(And(Not(initialMatrix[row][col][2]),initialMatrix[row][k][2]),And(initialMatrix[row][col][2],Not(initialMatrix[row][k][2]))),
                                        Or(And(Not(initialMatrix[row][col][3]),initialMatrix[row][k][3]),And(initialMatrix[row][col][3],Not(initialMatrix[row][k][3])))
                                        ))

#constraint3
rowConstraint = [And([rowElemDifferent[i] for i in range(len(rowElemDifferent))])]
s.add(rowConstraint)


colElemDifferent = []
for j in range(9):
    for i in range(9-1):
        for k in range(i+1,9,1):
            #print(initialMatrix[i][j], initialMatrix[k][j])
            colElemDifferent.append(Or(
                                        Or(And(Not(initialMatrix[i][j][0]),initialMatrix[k][j][0]),And(initialMatrix[i][j][0],Not(initialMatrix[k][j][0]))),
                                        #xorSat(initialMatrix[i][j][0], initialMatrix[k][j][0]),
                                        Or(And(Not(initialMatrix[i][j][1]),initialMatrix[k][j][1]),And(initialMatrix[i][j][1],Not(initialMatrix[k][j][1]))),
                                        #xorSat(initialMatrix[i][j][1], initialMatrix[k][j][1]),
                                        Or(And(Not(initialMatrix[i][j][2]),initialMatrix[k][j][2]),And(initialMatrix[i][j][2],Not(initialMatrix[k][j][2]))),
                                        #xorSat(initialMatrix[i][j][2], initialMatrix[k][j][2]),
                                        Or(And(Not(initialMatrix[i][j][3]),initialMatrix[k][j][3]),And(initialMatrix[i][j][3],Not(initialMatrix[k][j][3]))),
                                        #xorSat(initialMatrix[i][j][3], initialMatrix[k][j][3])
                                        ))

#constraint4
columnConstraint = [And([colElemDifferent[i] for i in range(len(colElemDifferent))])]
s.add(columnConstraint)

boxElemDifferent = []

for i0 in range(3):
    for j0 in range(3):
        boxElement = []
        for i in range(3):
            for j in range(3):
                boxElement.append(initialMatrix[3*i0 + i][3*j0 + j])
                #print(initialMatrix[3*i0 + i][3*j0 + j])
        for i in range(len(boxElement)-1):
            for j in range(i+1,len(boxElement),1):
                boxElemDifferent.append(Or(
                                            Or(And(Not(boxElement[i][0]),boxElement[j][0]),And(boxElement[i][0],Not(boxElement[j][0]))),
                                            #xorSat(boxElement[i][0], boxElement[j][0]),
                                            Or(And(Not(boxElement[i][1]),boxElement[j][1]),And(boxElement[i][1],Not(boxElement[j][1]))),
                                            #xorSat(boxElement[i][1], boxElement[j][1]),
                                            Or(And(Not(boxElement[i][2]),boxElement[j][2]),And(boxElement[i][2],Not(boxElement[j][2]))),
                                            #xorSat(boxElement[i][2], boxElement[j][2]),
                                            Or(And(Not(boxElement[i][3]),boxElement[j][3]),And(boxElement[i][3],Not(boxElement[j][3]))),
                                            #xorSat(boxElement[i][3], boxElement[j][3])
                                            ))

        boxConstraint = [And([boxElemDifferent[i] for i in range(len(boxElemDifferent))])]

s.add(boxConstraint)


boardConstraint = []

for i in range(9):
    for j in range(9):
        if board[i][j] != 0:
            binaryNumber = '{0:04b}'.format(board[i][j])
            #tempConstraint = createInstanceCanstraint(i,j,binNumber)

            constraint = []
            for k in range(4):
                if binaryNumber[k]=='1':
                    constraint.append(initialMatrix[i][j][k])
                else:
                    constraint.append(Not(initialMatrix[i][j][k]))

            tempConstraint = [And([constraint[elem] for elem in range(len(constraint))])]

            #print("tempConstraint_length ",len(tempConstraint))
            for k in range(len(tempConstraint)):
                boardConstraint.append(tempConstraint[k])

s.add(boardConstraint)


# s = Solver()
# s.add(noZeroCell+valueWithinOneToNine+rowConstraint+columnConstraint+boxConstraint+boardConstraint)

if s.check() == sat:
    m = s.model()
    #r = [ [ m.evaluate(initialMatrix[i][j][k]) for k in range(4) ]
    #      for j in range(9) for i in range(9)]
    #print_matrix(r)

    r = []

    for i in range(9):
        for j in range(9):
            tempList = []
            for k in range(4):
                tempList.append(m.evaluate(initialMatrix[i][j][k]))
            r.append(tempList)

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

    aArray = np.array(aBinToDec)
    m = aArray.reshape(9,9)
    print(m)

else:
    print("No solution found!!")
