from room import *
import random
from monster import *
def createRandWorld():

    #Helper list and function for directional operations.
    directions = ["north", "south", "east", "west", "up", "down"]
    def oppositeDirection(direction):
        for i in range(6):
            if directions[i] == direction:
                if i%2 == 0:
                    return directions[i+1]
                return directions[i-1]

    #Core function that builds a random network of rooms, branching out from a given starting room.
    def buildRandomRooms(parentRoom, parentDirection, depth, usedNames):
        roomNamePrefixes = ["", "Studious ", "Creepy ", "Austentatious ", "Sactified ", "Abundant ", "Swag "]
        roomNames = ["Hall of ", "Archipelago of ", "Place of ", "Escalator to ", "Sanctum of ", "Forest of "]
        roomNameSuffixes = ["Suffering", "Time", "Sanctuary", "Jellyfish", "Factoids", "Capitalism"]
        name = None
        while name in usedNames:
            name = random.choice(roomNamePrefixes)+random.choice(roomNames)+random.choice(roomNameSuffixes)
        description = "You are now in the " + name
        descriptions = [description]
        currRoom = Room(name, random.choice(descriptions))
        Room.connectRooms(parentRoom, parentDirection, currRoom, oppositeDirection(parentDirection))
        usedNames.append(name)
        world.append(parentRoom.exits[len(parentRoom.exits)-1][1])
        if depth > 0 and (findOpenDirectionsOfRoom(currRoom) != None):
            for direction in findOpenDirectionsOfRoom(currRoom):
                if direction != parentDirection:
                    buildRandomRooms(parentRoom.exits[len(parentRoom.exits)-1][1], direction, depth-1, usedNames)

    #Helper function that finds a random room with open directions and lists those directions.
    def findOpenDirectionsOfRandomRoom():
        randomRoom = center_brain
        while len(randomRoom.exits)>5:
            randomRoom = random.choice(world)
        openDirections = directions + []
        for exits in randomRoom.exits:
            if exits[0] in openDirections:
                openDirections.remove(exits[0])
        if len(openDirections) > 3:
            openDirections = openDirections[0:2]
        return [openDirections, randomRoom]

    #Find all the open directions of a given room and return a list of them
    def findOpenDirectionsOfRoom(room):
        if len(room.exits) < 3:
            openDirections = directions + []
            for exits in room.exits:
                if exits[0] in openDirections:
                    openDirections.remove(exits[0])
            numToReturn = 3 - len(room.exits)
            returnDirections = openDirections[0:(numToReturn)]
            return returnDirections
        else:
            return None

    #Helper function that returns a random room as long as that room has the given direction available
    def pickRandomRoomWithDirection(direction):
        currChoice = findOpenDirectionsOfRandomRoom()
        openDirections = currChoice[0]
        chosenRoom = currChoice[1]
        i = 0
        while (direction not in openDirections):
            currChoice = findOpenDirectionsOfRandomRoom()
            openDirections = currChoice[0]
            chosenRoom = currChoice[1]
            i += 1
            if i > 1000:
                return None
        return chosenRoom
        

    #Helper function that connects in a given room to a random place.
    def connectToRandomRoom(room):
        if findOpenDirectionsOfRoom(room) != None:
            outgoingDirection = random.choice(findOpenDirectionsOfRoom(room))
            randomRoom = pickRandomRoomWithDirection(oppositeDirection(outgoingDirection))
            if randomRoom != None:
                Room.connectRooms(room, outgoingDirection, randomRoom, oppositeDirection(outgoingDirection))

    #Helper function that randomly connects two rooms to each other.
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

    #Helper function that populates an arbitrary number of monsters into the world
    def populateMonsters(numAssignments,numLeisures,world):
        monsterNames = ["HUM 110 Paper 1",
        "HUM 110 Paper 2",
        "HUM 110 Paper 3",
        "HUM 110 Paper 4",
        "CS Midterm",
        "The Dread Lord Math 112",
        "CS Lab Assignment",
        "HUM 110 Reading"]
        for n in range(numAssignments):
            #Selects a unique name from the list while scrolling through the range. Currently supports only up to eight assignments.
            name = monsterNames[n]
            health = random.randint(1,20)
            place = random.randint(0,(len(world)-1))
            monstRoom = world[place]
            damage = random.randint(1,10)
            speed = random.randint(1,3)
            Assignment(name,health,monstRoom,damage,speed)

    #Build the key rooms. 
    center_brain = Room("center_brain","You are now in the center of the brain.")
    useful_programming = Room("useful_programming","You are now in the chamber of useful programming knowledge, a hallowed space filled mostly with CSC1 121 lecture notes.")
    lazy_hacks = Room("lazy_hacks","You are now in the room of lazy hacks. Every surface, from floor to walls to ceiling, is a chalkboard - but most of the notes you've taken there are covered up by the shelves of Stack Overflow comments.")
    programmer_humor = Room("programmer_humor","You have entered the sanctum of programmer humor, a place of many memes stolen from many subreddits.")
    bad_jokes = Room("bad_jokes","You are now in the room of bad jokes. And I mean *really* bad jokes. Abandon hope, all ye who enter here.")
    sci_fi = Room("sci_fi","You are now in the vault of out of place sci-fi references, a room strangely larger than any other in this brain.")
    productive_thought = Room("productive_thought","You are now in the room of productive academic thought. Sadly, there's quite a lot of dust here.")
    distractions = Room("distractions","You are now in the room of distractions - Hey, did you know the new NK Jemisin book just came out?")
    excuses = Room("excuses","Listen, it's not your fault you've entered the room of excuses. Somebody else made you do it.")
    world = [center_brain,useful_programming,lazy_hacks,programmer_humor,bad_jokes,sci_fi,productive_thought,distractions,excuses]
    keyRooms = [useful_programming,lazy_hacks,programmer_humor,bad_jokes,sci_fi,productive_thought,distractions,excuses]

    

    #Connect in the key rooms.

    #Build center_brain connections
    Room.connectRooms(center_brain,"north",useful_programming,"south")
    Room.connectRooms(center_brain,"east",productive_thought,"west")

    #Build useful_programming connections
    Room.connectRooms(useful_programming,"east",lazy_hacks,"west")
    Room.connectRooms(useful_programming,"west",programmer_humor,"east")

    #Build programmer_humor connections
    Room.connectRooms(programmer_humor,"west",bad_jokes,"east")
    Room.connectRooms(programmer_humor,"south",sci_fi,"north")

    #Build distractions connections
    Room.connectRooms(distractions,"south",excuses,"north")
    Room.connectRooms(distractions,"north",sci_fi,"south")

    #Build random pathways off of the center_brain.
    usedNames = [None]
    for direction in findOpenDirectionsOfRoom(center_brain):
        buildRandomRooms(center_brain, direction, 4, usedNames)

    #for keyRoom in keyRooms:
        #connectToRandomRoom(keyRoom)

    #Add some random shortcuts.
    #constructNonEuclidianPassages(random.randint(6,13))

    return world