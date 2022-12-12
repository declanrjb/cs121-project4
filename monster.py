import random
import updater

class Monster:
    def __init__(self, name, health, room):
        self.name = name
        self.health = health
        self.room = room
        room.addMonster(self)
        updater.register(self)
    def update(self):
        if random.random() < .5:
            self.moveTo(self.room.randomNeighbor())
    def moveTo(self, room):
        self.room.removeMonster(self)
        self.room = room
        room.addMonster(self)
    def die(self):
        self.room.removeMonster(self)
        updater.deregister(self)
    def findPlayer(self):
        """Detects where the player is if the player is in the same
        or an adjacent room."""
        if self.room.playerHere:
            return self.room
        for room in self.room.exits:
            if room[1].playerHere:
                return room[1]
    #Basic pathfinding
    def player_path(self,start):
        i = 0
        path = []
        currRoom = start
        while (i < 100) and (currRoom.playerHere != True):
            j = 0
            numExits = len(currRoom.exits)
            targetExit = currRoom.exits[j][1]
            while (targetExit in path) and (j < numExits):
                targetExit = currRoom.exits[j][1]
                j += 1
            currRoom = targetExit
            path.append(currRoom)
            i += 1
        return path
    #Function to find the shortest path from one room to another
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

    #Helper function that translates paths from navigate into exit directions
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

class Assignment(Monster):
    def __init__(self, name, health, room, damage, speed):
        super().__init__(name, health, room)
        self.damage = damage
        self.speed = speed
        self.cooldown = 0
        
    def update(self):
        if (random.randint(0,4) < 2) and (self.room.playerHere != True):
            path = self.player_path(self.room)
            #If there's more path than speed, move along the path up to my speed. Else, immediately move to 
            # the end of the path, without overshooting it.
            if self.speed <= len(path):
                self.moveTo(path[(self.speed - 1)])
            else:
                self.moveTo(path[(len(path) - 1)])

class Leisure(Monster):
    monsterType = "Leisure"
    def __init__self(self, name, health, room, cost, buff):
        Monster.__init___(self, name, health, room)
        self.cost = cost #The time it takes to do the activity
        self.buff = buff #The amount of mental health healed

class Essay(Assignment):
    monsterType = "Essay"

class Test(Assignment):
    monsterType = "Test"

class Presentation(Assignment):
    monsterType = "Presentation"

class ProblemSet(Assignment):
    monsterType = "Problem Set"

class Guard(Monster):
    def __init__(self,name,room):
        Monster.__init__(self,name,0,room)
    
    def interact(self,interaction):
        print(interaction)