from z3 import *
from sudokuSAT_solver import *

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


def createInstanceCanstraint(xPosition,yPosition,binaryNumber):
    constraint = []
    for k in range(4):
        if binaryNumber[k]=='1':
            constraint.append(X[xPosition][yPosition][k])
        else:
            constraint.append(Not(X[xPosition][yPosition][k]))
    return [And([constraint[i] for i in range(len(constraint))])]
