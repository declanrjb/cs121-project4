import random

def navigate(self,start,destination,prepath):
    if start == destination:
        return [destination]
    else:
        path = prepath + [start]
        currRoom = start
        while currRoom != destination:
            shortestPath = None
            targetExit = None
            for exit in currRoom.exits:
                exitRoom = exit[1]
                if (exitRoom in path) != True:
                    testPath = self.navigate(exit[1],destination,path)
                    if (shortestPath == None) or (len(testPath) < len(shortestPath)):
                        shortestPath = testPath
                        targetExit = exit[1]
            if targetExit == None:
                targetExit = currRoom.exits[random.randint(0,(len(currRoom.exits)-1))][1]
            currRoom = targetExit
            path.append(currRoom)
    return path

def directions(self,path):
    i = 0
    pathLength = len(path)
    directions = []
    while i < (pathLength-1):
        currRoom = path[i]
        for checkExit in currRoom.exits:
            if checkExit[1] == path[i+1]:
                directions.append(checkExit[0])
        i += 1
    return directions