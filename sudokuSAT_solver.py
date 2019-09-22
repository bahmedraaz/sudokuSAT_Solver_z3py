import numpy as np
from z3 import *

N = 9

#####Function to reads the input from the text file######
def extractInput(fileName):
    readFile = open(fileName, 'r')
    board = [[int(num) for num in line.split(',')] for line in readFile]

    for n, i in enumerate(board):
        for k, j in enumerate(i):
            board[n][k] = int(j)
    return board


########Function to performs XOR operation with only And, Not and Or######
def xorSat(param1, param2):
    return Or(And(Not(param1),param2),And(param1,Not(param2)))


#######Function to create constraint for the given board #########
#### This constraint ensures that the given value of differnt position in the board is unchanged#######
def createInstanceCanstraint(xPosition,yPosition,binaryNumber):
    constraint = []
    for k in range(4):
        if binaryNumber[k]=='1':
            constraint.append(X[xPosition][yPosition][k])
        else:
            constraint.append(Not(X[xPosition][yPosition][k]))
    return [And([constraint[i] for i in range(len(constraint))])]


### Function to print Matrix####
# def printMatrix(aList):
#     aArray = np.array(aList)
#     m = aArray.reshape(N,N)
#     print(m.T)


def printBoard(board):
    for row in range(len(board)):
        if row % 3 == 0 and row != 0:
            print("-------------------------------")
        for column in range(len(board[row])):
            if column % 3 == 0 and column != 0:
                print(" | ",end = "")

            if column == 8:
                print(board[row][column])
            else:
                print(str(board[row][column]) + " ", end=" ")


if __name__=="__main__":

    fileName = input("Please Enter The Input File Name: ")
    #fileName = "sudoku.txt"
    board = extractInput(fileName)


    # 9x9 matrix in which every element contains 4 propositional variable
    X = [ [ BoolVector("x_%s_%s" % (i+1, j+1), 4) for j in range(N) ] for i in range(N)]

    #constraint1: No cell should contain the value zero.
    noZeroCell = []
    for i in range(N):
        for j in range(N):
            noZeroCell.append(Or(X[i][j][0],X[i][j][1],X[i][j][2],X[i][j][3]))


    #constraint2: Every cell should contain the value in between 1 to 9 inclusive (1<= cellValue <=9)
    valueWithinOneToNine = []
    for i in range(N):
        for j in range(N):
            valueWithinOneToNine.append(Or(And(Not(X[i][j][0]),X[i][j][1]),
                                           And(X[i][j][0],Not(X[i][j][1]),Not(X[i][j][2])),
                                           And(Not(X[i][j][0]),X[i][j][3]),
                                           And(Not(X[i][j][0]),X[i][j][2])
                                           ))

    rowElemDifferent = []
    for i in range(N):
        for j in range(N-1):
            for k in range(j+1,N,1):
                rowElemDifferent.append(Or(xorSat(X[i][j][0], X[i][k][0]),
                                           xorSat(X[i][j][1], X[i][k][1]),
                                           xorSat(X[i][j][2], X[i][k][2]),
                                           xorSat(X[i][j][3], X[i][k][3])
                                           ))

    #constraint3: Every element in a row should hold different value
    rowConstraint = [And([rowElemDifferent[i] for i in range(len(rowElemDifferent))])]



    colElemDifferent = []
    for j in range(N):
        for i in range(N-1):
            for k in range(i+1,N,1):
                #print(X[i][j], X[k][j])
                colElemDifferent.append(Or(xorSat(X[i][j][0], X[k][j][0]),
                                           xorSat(X[i][j][1], X[k][j][1]),
                                           xorSat(X[i][j][2], X[k][j][2]),
                                           xorSat(X[i][j][3], X[k][j][3])
                                           ))

    #constraint4: Every element in a column should hold different value
    columnConstraint = [And([colElemDifferent[i] for i in range(len(colElemDifferent))])]

    #constraint5: Every element in the 3x3 box should hold different value
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
                    boxElemDifferent.append(Or(xorSat(boxElement[i][0], boxElement[j][0]),
                                               xorSat(boxElement[i][1], boxElement[j][1]),
                                               xorSat(boxElement[i][2], boxElement[j][2]),
                                               xorSat(boxElement[i][3], boxElement[j][3])
                                               ))

            boxConstraint = [And([boxElemDifferent[i] for i in range(len(boxElemDifferent))])]


    #constraint6: The given value in the board should not change
    boardConstraint = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                binNumber = '{0:04b}'.format(board[i][j])
                tempConstraint = createInstanceCanstraint(i,j,binNumber)
                for k in range(len(tempConstraint)):
                    boardConstraint.append(tempConstraint[k])

    s = Solver()
    ###add al the 6 constraints to the solver
    s.add(noZeroCell+valueWithinOneToNine+rowConstraint+columnConstraint+boxConstraint+boardConstraint)


    if s.check() == sat:
        m = s.model()
        r = [ [ m.evaluate(X[i][j][k]) for k in range(4) ]
              for j in range(9) for i in range(9)]

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

        #printMatrix(aBinToDec)
        #def printMatrix(aList):
        aArray = np.array(aBinToDec)
        m = aArray.reshape(N,N)
        #print(m.T)
        print("\n******* Before Solution ********\n")
        printBoard(board)

        print("\n******* After Solution ********\n")
        printBoard(m.T)

    else:
        print("failed to solve")
