# environment
"""
in k sat (k, noOfVars, noOfClauses)
so noOfVars > k

now for each clause, there will be k vars in or
so for ksat(3, 4, 2) it will be like
(a or ~b or c) and (~a or b or d) (RANDOMLY)
"""
from random import choices, random

negationStr = '~'
orStr = ' or '
andStr = ' and '
variablePrefix = 'a'

def createClause(vars, k):
    # so we chose k random variables for a clause
    randomVars = choices(vars, k = k)
    finalArray = []
    for i in randomVars:
        # now we'll just put negation randomly
        isNegation = random() < 0.5
        # ~var if negation else var
        finalArray.append(negationStr + i if isNegation else i)
        # join vars with or
    return orStr.join(finalArray)
    
def ksat(k, noOfVars, noOfClauses = 1):
    clouses = []
    vars = [variablePrefix + str(i) for i in range(noOfVars)]
    for i in range(noOfClauses):
        clouses.append('(' + createClause(vars, k) + ')')
    # join clouses with and
    return andStr.join(clouses)

"""
if ksat(2, 5, 3) = (~a4 or ~a2) and (a2 or a3) and (~a4 or a4)
then if (a0a1..a4) = (11111) <= STATE
then heuristic will return:

(~a4 or ~a2) and (a2 or a3) and (~a4 or a4)
  0  or 0     +   1  or  1   +    0  or 1
  = 2
also max(heuristicValue) = k
"""
def getStateIndex(state):
    return int(''.join(filter(str.isdigit, state)))

def getValueFromClause(clause='(~a4 or a2)', variableValues='11111'):
    # removing ( & ) and splitting by or
    vars = clause[1:-1].split(orStr)
    final = False
    for i in vars:
        isNegation = i.startswith(negationStr)
        stateIndex = getStateIndex(i)
        value = variableValues[stateIndex] == '1'
        if isNegation:
            value = not value
#         print(value)
        final = final or value
        # if value becomes true why bother, as its x OR y
        if final:
            break
#     print(final)
    return final

def getValueFromKsat(ksat, variableValues):
#     print(variableValues)
#     print(ksat)
    clouses = ksat.split(andStr)
    finalValue = 0
    for i in clouses:
#         print(i, '=>', getValueFromClause(i, variableValues))
        if(getValueFromClause(i, variableValues)):
            finalValue+=1
    return finalValue

def isFinalState(ksat, state):
    noOfClauses = len(ksat.split(andStr))
    return getValueFromKsat(ksat, state) == noOfClauses

def randomStartState(n):
    z = ['1' if random()>0.5 else '0' for i in range(n)]
    return ''.join(z)

# so in this one we'll get possible outcomes by changing just 1 bit
# so 101 => 001, 111, 100
def getPossibleOutComes(state, valueFunction = None, ksat = None):
    stateLength = len(state)
    newStates = []
    for i in range(stateLength):
        b = list(state)
        b[i] = '0' if b[i] == '1' else '1'
        newState = ''.join(b)
        newStates.append([newState, getValueFromKsat(ksat, newState)])
    return newStates
ksat_ = ksat(k=2, noOfVars=5, noOfClauses=5)
randomState = randomStartState(5)
print(ksat_, randomState, getValueFromKsat(ksat_, randomState))
# getPossibleOutComes(randomState, ksat = ksat_)
