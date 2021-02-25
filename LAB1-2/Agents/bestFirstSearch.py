from heapq import heappush, heappop
from .backtracking import backTracking

class Node:
    def __init__(self, state, cost=1, parent = None, children = []):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.children = children

"""
params: 
initialStateWithCost: [initial state string, cost to final state]
finalState: final state string
getPossibleOutComes: function from environment to return new states
heuristicFunction: heuristic function to get costs
finalCheckFunction: if there are more than one final strings, environment can supply function to check if state is final or not.
"""
def bestPathAgent(initialStateWithCost, finalState, getPossibleOutComes, heuristicFunction = None, finalCheckFunction=None):
    initialState, cost = initialStateWithCost
    if initialState == finalState:
        print('don\'t joke around!!')
    foundStates = []
    initialNode = Node(state = initialState, cost = cost, parent = None)
    prioQueue = []
    heappush(prioQueue, (cost, id(initialNode), initialNode))
    while prioQueue:
        # getting closest possible solN(depending upon heruristic of course xO )
        z = heappop(prioQueue)
        foundStates.append(z[2].state)
        newStates = getPossibleOutComes(z[2].state, heuristicFunction, finalState)
        print(newStates)
        print(z[2].state, '->', newStates)
        for newStateWithCost in newStates:
            newState, newCost = newStateWithCost
            newNode = Node(state = newState, parent = z[2], cost = newCost)
            if finalCheckFunction:
                if finalCheckFunction(newState):
                    print('Found Soln')
                    print('total explored ', len(foundStates))
                    backTracking(newNode)
                    return
            elif newState == finalState:
                print('Found Soln')
                print('total explored ', len(foundStates))
                backTracking(newNode)
                return
            if newState not in foundStates:
                foundStates.append(newState)
                heappush(prioQueue, (newCost, id(newNode),  newNode))
                