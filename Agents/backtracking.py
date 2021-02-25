def backTracking(finalNode):
    print(finalNode.state, end=' -> ')
    s = finalNode.parent
    nodes = [finalNode]
    # basically looping to parent again and again till there is no parent.
    while s:
        nodes.append(s)
        s = s.parent
    nodes.reverse()
    print('backTracking by tree', len(nodes), ' depth')
    for i in nodes:
        print(i.state, end=' -> ')