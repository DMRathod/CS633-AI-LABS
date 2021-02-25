from heapq import heappush, heappop

def beamSearchAgent(initialStateWithValue, kst, getPossibleOutComes, finalCheckFunction, costFunction, beams):
    [initialState, initialCostValue] = initialStateWithValue
    if finalCheckFunction(kst, initialState):
        print('reached goal state')
        return
    # can be implemented as hash table instead of array -> O(n) => O(1)
    foundStates = []
    rootNode = Node(state = initialState, cost = initialCostValue, parent = None)
    maxCost = initialCostValue
    currentNodes = []
    heappush(currentNodes, (initialCostValue, id(rootNode), rootNode))
    while len(currentNodes)>0:
        currentNode = heappop(currentNodes)
        print('exploring ', currentNode[2].state, ' with cost ', currentNode[2].cost)
        foundStates.append(currentNode[2].state)
        newStates = getPossibleOutComes(currentNode[2].state, valueFunction = costFunction, ksat = kst)
        print(newStates)
        # now finding max of all
        maxStates = []
        for state in newStates:
            if finalCheckFunction(kst, state[0]):
                print('final state is ', state[0])
                return
            if state[1] >= maxCost and state[0] not in foundStates:
                maxStates.append(Node(state = state[0], cost = state[1], parent = currentNode))
        # so we found bigger states, now sort them out
        maxStates.sort(key=lambda _: _.cost, reverse=True)
        # just taking first n states HERE BEAMS IS NUMBER OF BEAMS WE SPECIFY
        maxStates = maxStates[:beams]
        # finally updating max value for next iteration
        maxCost = maxStates[-1].cost
        for i in maxStates:
            heappush(currentNodes, (i.cost, id(i), i))
    print("no solN found")