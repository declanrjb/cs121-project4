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

    def randomRooms(parentRoom, parentDirection, depth, usedNames):
        roomNamePrefixes = ["a", "b", "c", "d", "e", "f"]
        roomNames = ["a", "b", "c", "d", "e", "f"]
        roomNameSuffixes = ["a", "b", "c", "d", "e", "f"]
        descriptions = ["a", "b", "c", "d", "e", "f"]
        name = None
        while name in usedNames:
            name = random.choice(roomNamePrefixes)+random.choice(roomNames)+random.choice(roomNameSuffixes)
        Room.connectRooms(parentRoom, parentDirection, Room(name, random.choice(descriptions)), oppositeDirection(parentDirection))
        usedNames.append(name)
        if depth > 0:
            for direction in directions:
                
                if direction != parentDirection and random.random() < depth/18:
                    randomRooms(parentRoom.exits[len(parentRoom.exits)-1][1], direction, depth-1, usedNames)
        print(name+str(len(usedNames)-1)+parentRoom.name)

    #Build the key rooms. 
    cPU = Room("CPU Pun Here", "Enthralling Description Here")
    puzzle1 = Room("p1", "p1")
    puzzle2 = Room("p2", "p2")
    puzzle3 = Room("p3", "p3")
    puzzle4 = Room("p4", "p4")
    puzzle5 = Room("p5", "p5")
    puzzle6 = Room("p6", "p6")

    #Build random pathways off of the cPU.
    usedNames = [None]
    for direction in directions:
        randomRooms(cPU, direction, 6, usedNames)

    puzzleRooms = [puzzle1, puzzle2, puzzle3, puzzle4, puzzle5, puzzle6]
    puzzleChoice = random.choice(puzzleRooms)
    puzzleRooms.remove(puzzleChoice)
    puzzleChoice = random.choice(puzzleRooms)
    puzzleRooms.remove(puzzleChoice)
    puzzleChoice = random.choice(puzzleRooms)
    puzzleRooms.remove(puzzleChoice)
    puzzleChoice = random.choice(puzzleRooms)
    puzzleRooms.remove(puzzleChoice)
    puzzleChoice = random.choice(puzzleRooms)
    puzzleRooms.remove(puzzleChoice)