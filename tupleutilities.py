
def getStringFromTuple(waypoint):
    return str(waypoint[0])+"_"+str(waypoint[1])

def cmp(tuple1,tuple2):
    if tuple1[0] == tuple2[0] and tuple1[1] == tuple2[1]:
        return 0
    else:
        return (tuple1 > tuple2) - (tuple1 < tuple2)

def getTuplesInPriorityForAction(waypoint_tuple,action):
    tuples = []

    if action=="moveLeft":
        print ("inside tupple "+action)
        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1]+1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1]-1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] +1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] +1, waypoint_tuple[1]+1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] +1, waypoint_tuple[1]-1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0], waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0], waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple)
        tuples.append(tuple)


    if action == "moveRight":
        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0], waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0], waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple)
        tuples.append(tuple)


    if action == "moveForward":
        tuple = (waypoint_tuple[0], waypoint_tuple[1]+1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0], waypoint_tuple[1]-1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0]-1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple[0]+1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple)
        tuples.append(tuple)


    if action == "moveBackward":
        tuple = (waypoint_tuple[0], waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1] - 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0], waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1] + 1)
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] - 1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple[0] + 1, waypoint_tuple[1])
        tuples.append(tuple)

        tuple = (waypoint_tuple)
        tuples.append(tuple)

    return tuples

