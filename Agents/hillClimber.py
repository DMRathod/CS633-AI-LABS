from collections import deque

def hillClimber(initialStateWithValue, kst, getPossibleOutComes, finalCheckFunction, costFunction):
    [initialState, initialCostValue] = initialStateWithValue
    if finalCheckFunction(kst, initialState):
        print('reached goal state')
        return
    # can be implemented as hash table instead of array -> O(n) => O(1)
    foundStates = []
    rootNode = Node(state = initialState, cost = initialCostValue, parent = None)
    maxCost = initialCostValue
    currentNode = rootNode
    while currentNode:
        print('exploring ', currentNode.state, ' with cost ', currentNode.cost)
        foundStates.append(currentNode.state)
        newStates = getPossibleOutComes(currentNode.state, valueFunction = costFunction, ksat = kst)
        print(newStates)
        # now finding max of all
        maxState = [None, 0]
        for state in newStates:
            if finalCheckFunction(kst, state[0]):
                print('final state is ', state[0])
                return
            # if cost higher than max and not yet found
            if state[1] >= maxState[1] and state[0] not in foundStates:
                maxState = state
        if maxState[0] and maxState[1]>=maxCost:
            maxCost = maxState[1]
            currentNode = Node(state = maxState[0], cost = maxState[1], parent = currentNode)
        else:
            currentNode = None
            print("no solution found by hill climbing!")
