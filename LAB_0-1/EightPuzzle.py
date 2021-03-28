"""
8 puzzle problem
So we can make a 3*3 state or a string state.
but 3*3 seems more logical and simple so we'll just go w/ that
"""
import numpy as np
from Agents.bestFirstSearch import bestPathAgent
from copy import deepcopy
import numpy as np
from collections import deque
from itertools import chain 

initialState = [[0, 1, 3],
                [4, 2, 5],
                [7, 8, 6]]
finalState = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

def getUpdatedState(state, rowIndex, colIndex, newRowIndex, newColIndex):
    newState = deepcopy(state)
    newState[rowIndex][colIndex] = newState[newRowIndex][newColIndex]
    newState[newRowIndex][newColIndex] = 0
    return newState

# to make things lil simpler instead of 4 if else loops
def possibleMoves(i, j):
    moves = [[i + 1, j],
            [i - 1, j],
            [i, j + 1],
            [i, j - 1]]
    # filtering not dynamic yet
    possible = list(filter(lambda x: (x[0]>=0 and x[1]>=0 and x[0]<=2 and x[1]<=2), moves))
    return possible if possible else []

# root( sigma((a-b)^2) )
# distanceFunction = lambda a, b: (np.sum((np.array(a) - np.array(b))**2))**0.5
def distanceFunction(a, b):
    return (np.sum((np.array(a) - np.array(b))**2))**0.5

def differenceFunction(a, b):
    _sum = 0
    for i in range(3):
        for j in range(3):
            if a[i][j] == b[i][j]:
                _sum += 1
    return _sum

def getPossibleOutComes(stateStr, heuristicFunction = None, finalState = None):
    state = strToArr(stateStr, 3)
    rows = len(state) # gonna be 3 but lets make dynamic so can work on any!!
    columns = len(state[0])
    # so if we have heuristic function we can return cost value as well so that it makes more sense.
    for i in range(rows):
        for j in range(columns):
            # if its 0 then bother to check, otherwise basically who cares
            if state[i][j] == 0:                
                if heuristicFunction:
                    # if heristict => [['possibleNewState', cost], ['possibleAnotherNewState', anotherCost]]
                    return [[arrToStr(getUpdatedState(state, i, j, z[0], z[1])), heuristicFunction(getUpdatedState(state, i, j, z[0], z[1]), strToArr(finalState, 3))] for z in possibleMoves(i, j)]
                return [arrToStr(getUpdatedState(state, i, j, z[0], z[1])) for z in possibleMoves(i, j)]

def arrToStr(arr):
    return ' '.join(str(item) for innerlist in arr for item in innerlist)

def strToArr(str, length):
    arr = str.split(' ')
    newArr = [[] for i in range(length)]
    count = 0
    for i in range(length):
        for j in range(length):
            newArr[i].append(int(arr[count]))
            count += 1
    return newArr

bestPathAgent(
    initialStateWithCost=[arrToStr(initialState), distanceFunction(initialState, finalState)], 
    finalState = arrToStr(finalState),
    getPossibleOutComes = getPossibleOutComes,
    heuristicFunction = distanceFunction
)