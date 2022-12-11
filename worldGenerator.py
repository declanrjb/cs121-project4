from room import *
import random
def createWorld():

    #Helper list and function for directional operations
    directions = ["North", "South", "East", "West", "Up", "Down"]
    def oppositeDirection(direction):
        for i in range(6):
            if directions[i] == direction:
                if i%2 == 0:
                    return directions[i+1]
                return directions[i-1]

    def buildRandomRooms(parentRoom, parentDirection, depth, usedNames):
        roomNamePrefixes = ["a", "b", "c", "d", "e", "f"]
        roomNames = ["a", "b", "c", "d", "e", "f"]
        roomNameSuffixes = ["a", "b", "c", "d", "e", "f"]
        descriptions = ["a", "b", "c", "d", "e", "f"]
        name = None
        while name in usedNames:
            name = random.choice(roomNamePrefixes)+random.choice(roomNames)+random.choice(roomNameSuffixes)
        Room.connectRooms(parentRoom, parentDirection, Room(name, random.choice(descriptions)), oppositeDirection(parentDirection))
        usedNames.append(name)
        world.append(parentRoom.exits[len(parentRoom.exits)-1][1])
        if depth > 0:
            for direction in directions:
                if direction != parentDirection and random.random() < depth/18:
                    buildRandomRooms(parentRoom.exits[len(parentRoom.exits)-1][1], direction, depth-1, usedNames)
        print(name+str(len(usedNames)-1)+parentRoom.name)

    def findOpenDirectionsOfRandomRoom():
        randomRoom = cPU
        while len(randomRoom.exits)>5:
            randomRoom = random.choice(world)
        openDirections = directions + []
        for exits in randomRoom.exits:
            openDirections.remove(exits[0])
        print([openDirections, randomRoom])
        return [openDirections, randomRoom]

    def connectToRandomRoom(room):
        randomRoom = findOpenDirectionsOfRandomRoom()
        direction = random.choice(randomRoom[0])
        Room.connectRooms(room, oppositeDirection(direction), randomRoom[1], direction)

    def constructNonEuclidianPassages(n):
        for passages in range(n):
            connectionFound = False
            while not connectionFound:
                randomRoom1 = findOpenDirectionsOfRandomRoom()
                randomRoom2 = findOpenDirectionsOfRandomRoom()
                openDirections1 = randomRoom1[0]
                openDirections2 = randomRoom2[0]
                for direction in openDirections2:
                    direction = oppositeDirection(direction)
                openDirections = list(set(openDirections1) and set(openDirections2))
                if len(openDirections) > 0:
                    connectionFound = True
            direction = random.choice(openDirections)
            Room.connectRooms(randomRoom1[1], direction, randomRoom2[1], oppositeDirection(direction))

    #Build the key rooms. 
    cPU = Room("CPU Pun Here", "Enthralling Description Here")
    puzzle1 = Room("p1", "p1")
    puzzle2 = Room("p2", "p2")
    puzzle3 = Room("p3", "p3")
    puzzle4 = Room("p4", "p4")
    puzzle5 = Room("p5", "p5")
    puzzle6 = Room("p6", "p6")
    world = [cPU, puzzle1, puzzle2, puzzle3, puzzle4, puzzle5, puzzle6]

    #Build random pathways off of the cPU.
    usedNames = [None]
    for direction in directions:
        buildRandomRooms(cPU, direction, 6, usedNames)

    connectToRandomRoom(puzzle1)
    connectToRandomRoom(puzzle2)
    connectToRandomRoom(puzzle3)
    connectToRandomRoom(puzzle4)
    connectToRandomRoom(puzzle5)
    connectToRandomRoom(puzzle6)
    constructNonEuclidianPassages(random.randint(6,13))